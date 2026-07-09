import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from db.database import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    workflow_type = Column(String, nullable=False) # repo_analysis, bug_resolution, feature_development
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    repository_id = Column(String(36), ForeignKey("repositories.id"), nullable=True)
    status = Column(String, default="pending")
    input_data = Column(JSON, nullable=False)
    output_data = Column(JSON, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="workflows")
    agent_runs = relationship("AgentRun", back_populates="workflow")
