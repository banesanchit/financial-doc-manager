from fastapi import APIRouter

from pydantic import BaseModel

from app.services.rag_service import (
    semantic_search
)

router = APIRouter(
    prefix="/rag",
    tags=["RAG Search"]
)

class SearchQuery(BaseModel):

    query: str

@router.post("/search")

def search_documents(
    data: SearchQuery
):

    results = semantic_search(
        data.query
    )

    return {
        "results": results
    }