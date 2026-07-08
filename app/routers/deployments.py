from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.deployment import DeploymentModel
from app.schemas.deployment import Deployment, DeploymentCreate, DeploymentStatus
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/deployments", tags=["deployments"])


@router.get("/", response_model=list[Deployment])
def list_deployments(
    service_id: int | None = None,
    environment: str | None = None,
    status: DeploymentStatus | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    query = db.query(DeploymentModel)

    if service_id is not None:
        query = query.filter(DeploymentModel.service_id == service_id)
    if environment is not None:
        query = query.filter(DeploymentModel.environment == environment)
    if status is not None:
        query = query.filter(DeploymentModel.status == status.value)

    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=Deployment, status_code=201)
def create_deployment(deployment: DeploymentCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    data = deployment.model_dump()
    data["status"] = data["status"].value
    new_deployment = DeploymentModel(**data)
    db.add(new_deployment)
    db.commit()
    db.refresh(new_deployment)
    return new_deployment


@router.get("/{deployment_id}", response_model=Deployment)
def get_deployment(deployment_id: int, db: Session = Depends(get_db)):
    deployment = db.query(DeploymentModel).filter(DeploymentModel.id == deployment_id).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return deployment
