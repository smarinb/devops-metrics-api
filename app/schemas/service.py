from pydantic import BaseModel


class ServiceBase(BaseModel):
    name: str
    repository: str
    owner: str


class ServiceCreate(ServiceBase):
    pass


class Service(ServiceBase):
    id: int

    class Config:
        from_attributes = True
