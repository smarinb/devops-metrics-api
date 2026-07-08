"""
Creates the initial admin user. Run once after setting up a fresh database:
    python -m app.seed
"""
from app.db.database import SessionLocal
from app.models.user import UserModel
from app.core.security import hash_password


def create_initial_admin():
    db = SessionLocal()
    try:
        existing = db.query(UserModel).filter(UserModel.username == "admin").first()
        if existing:
            print("Admin user already exists, skipping.")
            return

        admin = UserModel(
            username="admin",
            email="admin@example.com",
            role="admin",
            hashed_password=hash_password("changeme123"),
        )
        db.add(admin)
        db.commit()
        print("Initial admin user created: username='admin', password='changeme123'")
        print("IMPORTANT: change this password immediately in production.")
    finally:
        db.close()


if __name__ == "__main__":
    create_initial_admin()
