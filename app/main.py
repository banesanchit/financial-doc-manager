from fastapi import FastAPI
from app.database import Base, engine

from app.models import user
from app.models import role
from app.models import document
from app.routers.auth_router import router as auth_router
from app.routers.document_router import router as document_router
from app.routers.rag_router import router as rag_router
from app.routers.role_router import router as role_router

from app.routers.user_router import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Financial Document Manager"
)
app.include_router(auth_router)
app.include_router(document_router)
app.include_router(rag_router)
app.include_router(role_router)
app.include_router(user_router)

@app.get("/")
def home():
    return {
        "message": "Financial Document API Running"
    }