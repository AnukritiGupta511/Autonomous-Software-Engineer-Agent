import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Integer, Float
from sqlalchemy.orm import relationship
from db.database import Base

class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_type = Column(String, nullable=False)
    workflow_id = Column(String(36), ForeignKey("workflows.id"), nullable=True)
    repository_id = Column(String(36), ForeignKey("repositories.id"), nullable=True)
    status = Column(String, default="pending") # pending, running, completed, failed
    input_data = Column(JSON, nullable=False)
    output_data = Column(JSON, nullable=True)
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

    workflow = relationship("Workflow", back_populates="agent_runs")
    repository = relationship("Repository", back_populates="agent_runs")
