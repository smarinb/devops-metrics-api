from fastapi import APIRouter, HTTPException
from app.schemas.user import User, UserCreate

router = APIRouter(prefix="/users", tags=["users"])

fake_db: list[User] = []
next_id = 1


@router.get("/", response_model=list[User])
def list_users():
    return fake_db


@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate):
    global next_id
    user_data = user.model_dump(exclude={"password"})
    new_user = User(id=next_id, **user_data)
    fake_db.append(new_user)
    next_id += 1
    return new_user


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    for u in fake_db:
        if u.id == user_id:
            return u
    raise HTTPException(status_code=404, detail="User not found")
