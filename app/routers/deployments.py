from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query
from app.schemas.deployment import Deployment, DeploymentCreate, DeploymentStatus

router = APIRouter(prefix="/deployments", tags=["deployments"])

fake_db: list[Deployment] = []
next_id = 1


@router.get("/", response_model=list[Deployment])
def list_deployments(
    service_id: int | None = None,
    environment: str | None = None,
    status: DeploymentStatus | None = None,
    skip: int = 0,
    limit: int = 20,
):
    results = fake_db

    if service_id is not None:
        results = [d for d in results if d.service_id == service_id]
    if environment is not None:
        results = [d for d in results if d.environment == environment]
    if status is not None:
        results = [d for d in results if d.status == status]

    return results[skip: skip + limit]


@router.post("/", response_model=Deployment, status_code=201)
def create_deployment(deployment: DeploymentCreate):
    global next_id
    new_deployment = Deployment(
        id=next_id,
        timestamp=datetime.now(timezone.utc),
        **deployment.model_dump(),
    )
    fake_db.append(new_deployment)
    next_id += 1
    return new_deployment


@router.get("/{deployment_id}", response_model=Deployment)
def get_deployment(deployment_id: int):
    for d in fake_db:
        if d.id == deployment_id:
            return d
    raise HTTPException(status_code=404, detail="Deployment not found")
