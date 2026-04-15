from sqlalchemy.orm import Session
from database.models import ExtractionResult


def get_result_by_document_id(db: Session, document_id: int):
    return (
        db.query(ExtractionResult)
        .filter(ExtractionResult.document_id == document_id)
        .first()
    )


def get_all_results(db: Session):
    return db.query(ExtractionResult).order_by(
        ExtractionResult.created_at.desc()
    ).all()