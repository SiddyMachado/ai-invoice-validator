from pathlib import Path
import json

from litellm import completion
from app.validate import validate_extraction
from app.utils import strip_markdown
from app.confidence import compute_confidence
from app.confidence import compute_document_confidence

DEBUG = False

BASE_DIR = Path(__file__).parent
ocr_path = BASE_DIR / "output" / "batch1-0001.txt"

ocr_text = ocr_path.read_text(encoding="utf-8")

FIELD_KEYWORDS = {
    "invoice_number": ["invoice number", "invoice no", "inv no"],
    "invoice_date": ["invoice date", "date", "date of issue"],
    "total_amount": ["total amount", "amount due", "total"],
    "currency": ["currency", "eur", "usd", "inr", "gbp", "$", "€", "£", "₹"],
    "vendor_name": ["vendor", "seller", "from"]
}


PROMPT = f"""
You are an information extraction system.

Extract the following fields and return JSON ONLY.
Do not infer. Do not normalize unless explicit.

Schema:
{{
  "invoice_number": {{ "value": string | null, "confidence": number | null }},
  "invoice_date": {{ "value": string | null, "confidence": number | null }},
  "total_amount": {{ "value": number | null, "confidence": number | null }},
  "currency": {{ "value": "EUR" | "USD" | "INR" | "GBP" | null, "confidence": number | null }},
  "vendor_name": {{ "value": string | null, "confidence": number | null }}
}}

OCR Text:
<<<
{ocr_text}
>>>
"""


response = completion(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": PROMPT}],
    temperature=0
)

raw_output = response["choices"][0]["message"]["content"]

if DEBUG:
    print(raw_output)

cleaned_output = strip_markdown(raw_output)

extracted_json = json.loads(cleaned_output)

validated_json = validate_extraction(extracted_json)

# ----- Per-field confidence -----
for field_name in FIELD_KEYWORDS.keys():
    field_data = validated_json.get(field_name)

    if not field_data:
        continue

    confidence_dict = compute_confidence(
        field_name=field_name,
        field_data=field_data,
        ocr_text=ocr_text,
        keywords=FIELD_KEYWORDS.get(field_name, [])
    )

    field_data["confidence"] = confidence_dict
    field_data["valid"] = bool(field_data.get("valid", True))


# ----- Document-level confidence (AFTER loop) -----
document_confidence = compute_document_confidence(validated_json)

validated_json["metadata"] = {
    "document_confidence": document_confidence
}

print(json.dumps(validated_json, indent=2))