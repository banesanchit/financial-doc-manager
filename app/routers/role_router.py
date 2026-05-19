from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models.role import Role

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

@router.post("/create")

def create_role(
    name: str,
    db: Session = Depends(get_db)
):

    role = Role(name=name)

    db.add(role)

    db.commit()

    db.refresh(role)

    return role