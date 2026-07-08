from sqlalchemy import Column, Integer, String
from app.db.database import Base


class ServiceModel(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    repository = Column(String, nullable=False)
    owner = Column(String, nullable=False)
