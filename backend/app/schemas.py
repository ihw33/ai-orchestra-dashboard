"""
Pydantic schemas (v2) for API I/O models
Issue #12: 프로젝트 모델 스키마 정의
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


# -----------------
# Project Schemas
# -----------------

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    github_repo: Optional[str] = Field(None, pattern=r"^[^/\s]+/[^/\s]+$")
    slug: Optional[str] = Field(None, min_length=1, max_length=200)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    github_repo: Optional[str] = Field(None, pattern=r"^[^/\s]+/[^/\s]+$")
    slug: Optional[str] = Field(None, min_length=1, max_length=200)


class ProjectOut(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# -----------------
# Task Schemas (optional for future work)
# -----------------

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    description: Optional[str] = None
    status: Optional[str] = Field("pending", pattern=r"^(pending|in_progress|completed)$")
    assigned_ai: Optional[str] = None
    github_issue_number: Optional[int] = None


class TaskCreate(TaskBase):
    project_id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern=r"^(pending|in_progress|completed)$")
    assigned_ai: Optional[str] = None
    github_issue_number: Optional[int] = None


class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

