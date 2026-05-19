from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models.user import User

from app.models.role import Role

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

@router.post("/assign-role")

def assign_role(

    user_id: int,

    role_id: int,

    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    role = db.query(Role).filter(
        Role.id == role_id
    ).first()

    if not user or not role:

        return {
            "message": "User or Role not found"
        }

    user.role_id = role.id

    db.commit()

    return {
        "message": "Role Assigned Successfully"
    }

@router.get("/{user_id}/roles")

def get_user_role(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        return {
            "message": "User not found"
        }

    role = db.query(Role).filter(
        Role.id == user.role_id
    ).first()

    return {
        "user": user.username,
        "role": role.name if role else None
    }
@router.get("/")

def get_all_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    result = []

    for user in users:

        role = db.query(Role).filter(
            Role.id == user.role_id
        ).first()

        result.append({

            "id": user.id,

            "username": user.username,

            "email": user.email,

            "role": role.name if role else None
        })

    return result
@router.delete("/{user_id}")

def delete_user(

    user_id: int,

    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        return {
            "message": "User Not Found"
        }

    db.delete(user)

    db.commit()

    return {
        "message": "User Deleted Successfully"
    }
@router.put("/change-role")

def change_role(

    user_id: int,

    role_id: int,

    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    role = db.query(Role).filter(
        Role.id == role_id
    ).first()

    if not user or not role:

        return {
            "message": "User or Role Not Found"
        }

    user.role_id = role.id

    db.commit()

    return {
        "message": "Role Updated Successfully"
    }