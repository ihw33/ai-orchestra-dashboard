"""
Database models for AI Orchestra Dashboard
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    github_repo = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tasks = relationship("Task", back_populates="project")
    ai_sessions = relationship("AISession", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    github_issue_number = Column(Integer)
    title = Column(String)
    description = Column(Text)
    status = Column(String, default="pending")  # pending, in_progress, completed
    assigned_ai = Column(String)  # Which AI is handling this
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    ai_actions = relationship("AIAction", back_populates="task")

class AISession(Base):
    __tablename__ = "ai_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    ai_type = Column(String)  # claude, gpt, gemini, etc.
    session_type = Column(String)  # discussion, development, review
    status = Column(String, default="active")  # active, completed, failed
    context = Column(JSON)  # Store conversation context
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="ai_sessions")
    actions = relationship("AIAction", back_populates="session")

class AIAction(Base):
    __tablename__ = "ai_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("ai_sessions.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    action_type = Column(String)  # github_comment, code_generation, review, etc.
    action_data = Column(JSON)  # Store action details
    result = Column(JSON)  # Store action results
    status = Column(String, default="pending")  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("AISession", back_populates="actions")
    task = relationship("Task", back_populates="ai_actions")

class GitHubEvent(Base):
    __tablename__ = "github_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String)  # issue, pull_request, push, etc.
    event_action = Column(String)  # opened, closed, merged, etc.
    payload = Column(JSON)  # Full webhook payload
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)