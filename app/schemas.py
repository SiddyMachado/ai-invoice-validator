from typing import Optional, Generic, TypeVar, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import date, datetime
import copy

BASE_FIELD_TEMPLATE = {
    "value": None,
    "confidence": {
        "ocr": None,
        "llm": None,
        "validation": None,
        "overall": None
    },
    "valid": None
}

def create_base_field():
    return copy.deepcopy(BASE_FIELD_TEMPLATE)

def create_invoice_schema():
    return {
        "invoice_number": create_base_field(),
        "invoice_date": create_base_field(),
        "vendor_name": create_base_field(),
        "total_amount": create_base_field(),
        "currency": create_base_field(),

        "warnings": [],

        "metadata": {
            "ocr_quality_score": None,
            "processing_time_ms": None,
            "document_confidence": None
        }
    }

T = TypeVar("T")

class ExtractedField(BaseModel, Generic[T]):
    value: Optional[T] = Field(default=None)
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)

class Currency(str, Enum):
    EUR = "EUR"
    USD = "USD"
    INR = "INR"
    GBP = "GBP"

class InvoiceSchema(BaseModel):
    invoice_number: ExtractedField[str]
    invoice_date: ExtractedField[date]
    total_amount: ExtractedField[float]
    currency: ExtractedField[Currency]
    vendor_name: ExtractedField[str]


class DocumentResultResponse(BaseModel):
    id: int
    document_id: int
    extraction_json: Optional[Dict[str, Any]]
    confidence_score: Optional[float]
    validation_status: str
    created_at: datetime

    class Config:
        orm_mode = True

