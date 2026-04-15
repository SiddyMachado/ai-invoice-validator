from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path

from app.extract import run_extraction
from app.ocr import run_ocr
from database.database import get_db
from database.models import Document, OCRText, ExtractionResult
from app.crud import get_result_by_document_id
from app.services.storage_factory import get_storage
from app.config import POPPLER_PATH

router = APIRouter()

PDF_EXTENSIONS = (".pdf",)
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".tiff", ".bmp")


# -------------------------------
# RESPONSE SHAPE (CONSISTENT)
# -------------------------------
def build_document_response(document, result=None):
    return {
        "document_id": document.id,
        "status": document.status,
        "result": result
    }


# -------------------------------
# UPLOAD DOCUMENT
# -------------------------------
@router.post("/documents")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    document = None

    try:
        suffix = Path(file.filename).suffix.lower()

        if suffix not in PDF_EXTENSIONS + IMAGE_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type"
            )

        # Create document
        document = Document(
            filename=file.filename,
            status="uploaded"
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        # Save file
        storage = get_storage()
        content = await file.read()

        file_key = storage.save_file(
            file_bytes=content,
            filename=f"{document.id}{suffix}"
        )

        document.file_path = file_key
        document.status = "processing"
        db.commit()

        # OCR
        text = run_ocr(
            file_bytes=content,
            suffix=suffix,
            poppler_path=POPPLER_PATH
        )

        db.add(OCRText(
            document_id=document.id,
            raw_text=text,
            ocr_engine="tesseract"
        ))
        db.commit()

        # Extraction
        extracted_json = run_extraction(text)

        db.add(ExtractionResult(
            document_id=document.id,
            extraction_json=extracted_json,
            confidence_score=extracted_json.get("metadata", {}).get("document_confidence"),
            validation_status="pending"
        ))

        document.status = "completed"
        db.commit()

        return build_document_response(document, extracted_json)

    except Exception as e:
        if document:
            document.status = "failed"
            db.commit()

        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# GET SINGLE DOCUMENT RESULT
# -------------------------------
@router.get("/documents/{document_id}/result")
def get_document_result(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    result = db.query(ExtractionResult).filter(
        ExtractionResult.document_id == document_id
    ).first()

    return build_document_response(
        document,
        result.extraction_json if result else None
    )


# -------------------------------
# GET ALL DOCUMENT RESULTS
# -------------------------------
@router.get("/documents/results")
def get_all_document_results(
    db: Session = Depends(get_db),
):
    documents = db.query(Document).all()
    response = []

    for doc in documents:
        result = get_result_by_document_id(db, doc.id)

        response.append(
            build_document_response(
                doc,
                result.extraction_json if result else None
            )
        )

    return response