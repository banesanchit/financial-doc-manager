from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from datetime import datetime

from app.database import Base

class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

    title = Column(String)

    company_name = Column(String)

    document_type = Column(String)

    file_path = Column(String)

    extracted_text = Column(Text)

    uploaded_by = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )