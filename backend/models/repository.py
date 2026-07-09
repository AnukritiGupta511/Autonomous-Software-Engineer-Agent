import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from db.database import Base

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    github_url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    default_branch = Column(String, default="main")
    description = Column(Text, nullable=True)
    technologies = Column(JSON, nullable=True)
    file_structure = Column(JSON, nullable=True)
    is_indexed = Column(Boolean, default=False)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="repositories")
    chats = relationship("Chat", back_populates="repository")
    agent_runs = relationship("AgentRun", back_populates="repository")
