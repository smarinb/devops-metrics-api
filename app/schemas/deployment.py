from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class DeploymentStatus(str, Enum):
    success = "success"
    failed = "failed"
    in_progress = "in_progress"


class DeploymentBase(BaseModel):
    service_id: int
    version: str
    environment: str
    status: DeploymentStatus
    duration_seconds: float


class DeploymentCreate(DeploymentBase):
    pass


class Deployment(DeploymentBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
