from sqlalchemy import Column, Integer, String
from app.db.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False, default="viewer")
    hashed_password = Column(String, nullable=False)
