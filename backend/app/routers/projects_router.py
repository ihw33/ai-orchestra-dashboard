"""
Projects Router
Issue #14: 프로젝트 CRUD 엔드포인트 + 모니터링 훅
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.services.data_collector import MultiProjectMonitor
from app.database import get_db
from app import models
from app.schemas import ProjectCreate, ProjectUpdate, ProjectOut
import asyncio

router = APIRouter(prefix="/api/projects", tags=["Projects"])

# In-memory monitor handle
monitor: Optional[MultiProjectMonitor] = None


# -----------------
# CRUD: Projects
# -----------------

@router.post("/", response_model=ProjectOut)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> ProjectOut:
    exists = db.query(models.Project).filter(models.Project.name == payload.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Project with the same name already exists")
    project = models.Project(
        name=payload.name,
        description=payload.description,
        github_repo=payload.github_repo,
        slug=payload.slug,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/", response_model=List[ProjectOut])
def list_projects(db: Session = Depends(get_db)) -> List[ProjectOut]:
    return db.query(models.Project).order_by(models.Project.created_at.desc()).all()


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectOut:
    project = db.query(models.Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)) -> ProjectOut:
    project = db.query(models.Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)) -> dict:
    project = db.query(models.Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"status": "deleted", "id": project_id}


# -----------------
# Monitoring Hooks
# -----------------

@router.post("/monitor/start")
async def start_monitoring(db: Session = Depends(get_db)):
    """실시간 모니터링 시작"""
    global monitor
    if monitor and monitor.is_streaming:
        raise HTTPException(status_code=400, detail="Monitoring is already running")

    projects = db.query(models.Project).all()
    if not projects:
        raise HTTPException(status_code=400, detail="No projects configured for monitoring")

    repo_names = [p.github_repo for p in projects if p.github_repo]
    if not repo_names:
        raise HTTPException(status_code=400, detail="Projects do not have github_repo configured")

    monitor = MultiProjectMonitor(repo_names)
    asyncio.create_task(monitor.start_streaming())
    return {"status": "monitoring_started", "repositories": repo_names}


@router.post("/monitor/stop")
async def stop_monitoring():
    """실시간 모니터링 중지"""
    global monitor
    if not monitor or not monitor.is_streaming:
        raise HTTPException(status_code=400, detail="Monitoring is not running")
    
    monitor.stop_streaming()
    monitor = None
    return {"status": "monitoring_stopped"}


@router.get("/monitor/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    """현재 집계된 메트릭 반환"""
    global monitor
    if not monitor:
        projects = db.query(models.Project).all()
        repo_names = [p.github_repo for p in projects if p.github_repo]
        if not repo_names:
            raise HTTPException(status_code=400, detail="No projects configured for monitoring")
        monitor = MultiProjectMonitor(repo_names)

    return monitor.get_aggregated_metrics()
