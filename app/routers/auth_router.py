from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user_schema import (
    UserRegister,
    UserLogin
)

from app.utils.jwt_handler import (
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

@router.post("/register")
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {

        "message": "User Registered Successfully",

        "user_id": new_user.id,

        "username": new_user.username,

        "email": new_user.email
    }
@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        return {
            "message": "User not found"
        }

    if db_user.password != user.password:
        return {
            "message": "Incorrect Password"
        }

    token = create_access_token(
        {"sub": db_user.email}
    )

    role_name = None

    if db_user.role_id == 1:
        role_name = "Admin"

    elif db_user.role_id == 2:
        role_name = "Financial Analyst"

    elif db_user.role_id == 3:
        role_name = "Auditor"

    elif db_user.role_id == 4:
        role_name = "Client"

    return {
        "access_token": token,
        "token_type": "bearer",
        "email": db_user.email,
        "username": db_user.username,
        "role": role_name
    }
