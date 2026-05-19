from app.services.rag_service import extract_text_from_pdf
from app.services.rag_service import store_embeddings

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    Query
)

from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models.document import Document

import shutil
import os

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

@router.post("/upload")
async def upload_document(

    title: str = Form(...),

    company_name: str = Form(...),

    document_type: str = Form(...),

    uploaded_by: str = Form(...),

    file: UploadFile = File(...),

    db: Session = Depends(get_db)
):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)

    new_document = Document(

        title=title,

        company_name=company_name,

        document_type=document_type,

        file_path=file_path,

        uploaded_by=uploaded_by,

        extracted_text=extracted_text
    )

    db.add(new_document)

    db.commit()

    db.refresh(new_document)

    store_embeddings(
        new_document.id,
        extracted_text
    )

    return {
        "message": "Document Uploaded Successfully",
        "file_name": file.filename
    }

@router.get("/")
def get_documents(
    db: Session = Depends(get_db)
):

    documents = db.query(Document).all()

    return documents

@router.get("/search")

def search_documents(

    company_name: str = Query(None),

    document_type: str = Query(None),

    title: str = Query(None),

    db: Session = Depends(get_db)
):

    query = db.query(Document)

    if company_name:

        query = query.filter(
            Document.company_name.ilike(
                f"%{company_name}%"
            )
        )

    if document_type:

        query = query.filter(
            Document.document_type.ilike(
                f"%{document_type}%"
            )
        )

    if title:

        query = query.filter(
            Document.title.ilike(
                f"%{title}%"
            )
        )

    documents = query.all()

    return documents

@router.get("/{document_id}")

def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    return document


@router.delete("/{document_id}")

def delete_document(

    document_id: int,

    db: Session = Depends(get_db)
):

    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:

        return {
            "message": "Document Not Found"
        }

    # DELETE PDF FILE

    if os.path.exists(document.file_path):

        os.remove(document.file_path)

    # DELETE DATABASE RECORD

    db.delete(document)

    db.commit()

    return {
        "message": "Document Deleted Successfully"
    }