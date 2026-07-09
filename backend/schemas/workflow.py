import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Any

class WorkflowCreate(BaseModel):
    name: str
    workflow_type: str
    repository_id: uuid.UUID | None = None
    input_data: dict[str, Any]

class AgentRunResponse(BaseModel):
    id: uuid.UUID
    agent_type: str
    status: str
    input_data: dict | None
    output_data: dict | None
    tokens_used: int
    cost: float
    started_at: datetime
    completed_at: datetime | None
    error_message: str | None

    model_config = ConfigDict(from_attributes=True)

class WorkflowResponse(BaseModel):
    id: uuid.UUID
    name: str
    workflow_type: str
    status: str
    input_data: dict | None
    output_data: dict | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    agent_runs: list[AgentRunResponse] = []

    model_config = ConfigDict(from_attributes=True)
