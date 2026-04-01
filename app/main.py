from fastapi import FastAPI
from app.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers.records import router as records_router
from app.routers.dashboard import router as dashboard_router
from app.routers.user import router as user_router
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.core.hashing import hash_password
from app.core.config import ADMIN_EMAIL, ADMIN_PASSWORD


from app.models import *

app = FastAPI()


Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Finance API is running "}



app.include_router(auth_router)
app.include_router(records_router)
app.include_router(dashboard_router)
app.include_router(user_router)


def create_first_admin():
    db: Session = SessionLocal()

    admin = db.query(User).filter(User.role == "admin").first()

    if not admin:
        new_admin = User(
            email="ADMIN_EMAIL",
            password=hash_password("ADMIN_PASSWORD"),
            role="admin"
        )
        db.add(new_admin)
        db.commit()
        print("✅ First admin created: admin@example.com / admin123")

    db.close()


create_first_admin()