from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=True)

    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # uploaded | processing | completed | failed
    status = Column(String, default="uploaded")

    # relationships
    ocr_texts = relationship("OCRText", back_populates="document")
    extraction_results = relationship("ExtractionResult", back_populates="document")


class OCRText(Base):
    __tablename__ = "ocr_text"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        index=True,
        nullable=False
    )

    raw_text = Column(Text)

    ocr_engine = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relationship
    document = relationship("Document", back_populates="ocr_texts")


class ExtractionResult(Base):
    __tablename__ = "extraction_results"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        index=True,
        nullable=False
    )

    extraction_json = Column(JSON)

    confidence_score = Column(Float)

    # pending | validated | failed | needs_review
    validation_status = Column(String, default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)

    # relationship
    document = relationship("Document", back_populates="extraction_results")