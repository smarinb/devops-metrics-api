from fastapi import APIRouter, HTTPException
from app.schemas.service import Service, ServiceCreate

router = APIRouter(prefix="/services", tags=["services"])

# Temporary in-memory storage (will be replaced by PostgreSQL in Phase 2)
fake_db: list[Service] = []
next_id = 1


@router.get("/", response_model=list[Service])
def list_services():
    return fake_db


@router.post("/", response_model=Service, status_code=201)
def create_service(service: ServiceCreate):
    global next_id
    new_service = Service(id=next_id, **service.model_dump())
    fake_db.append(new_service)
    next_id += 1
    return new_service


@router.get("/{service_id}", response_model=Service)
def get_service(service_id: int):
    for service in fake_db:
        if service.id == service_id:
            return service
    raise HTTPException(status_code=404, detail="Service not found")


@router.delete("/{service_id}", status_code=204)
def delete_service(service_id: int):
    global fake_db
    for i, service in enumerate(fake_db):
        if service.id == service_id:
            fake_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Service not found")
