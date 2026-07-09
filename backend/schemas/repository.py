import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Any

class RepositoryCreate(BaseModel):
    github_url: str
    project_id: uuid.UUID | None = None

class RepositoryResponse(BaseModel):
    id: uuid.UUID
    github_url: str
    name: str
    owner: str
    default_branch: str
    description: str | None
    technologies: dict | list | None
    is_indexed: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class RepositoryAnalysis(BaseModel):
    overview: str
    technologies: list[str]
    file_structure: dict[str, Any]
    dependencies: dict[str, Any]
    architecture_summary: str
