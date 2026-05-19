from pydantic import BaseModel

class DocumentResponse(BaseModel):

    id: int
    title: str
    company_name: str
    document_type: str
    file_path: str

    class Config:
        from_attributes = True