from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.service import ServiceModel
from app.schemas.service import Service, ServiceCreate
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/", response_model=list[Service])
def list_services(db: Session = Depends(get_db)):
    return db.query(ServiceModel).all()


@router.post("/", response_model=Service, status_code=201)
def create_service(service: ServiceCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    new_service = ServiceModel(**service.model_dump())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service


@router.get("/{service_id}", response_model=Service)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(ServiceModel).filter(ServiceModel.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.delete("/{service_id}", status_code=204)
def delete_service(service_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = db.query(ServiceModel).filter(ServiceModel.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(service)
    db.commit()
