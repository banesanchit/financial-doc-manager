from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String, unique=True)

    email = Column(String, unique=True)

    password = Column(String)

    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=True
    )