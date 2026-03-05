from datetime import date
from typing import Dict, Any
import re

from app.parsing import parse_date
from app.schemas import Currency


# -----------------------------
# Configuration / constants
# -----------------------------

ALLOWED_CURRENCIES = {"EUR", "USD", "INR", "GBP"}

MAX_INVOICE_NUMBER_LENGTH = 50
MAX_VENDOR_NAME_LENGTH = 100
MAX_TOTAL_AMOUNT = 1_000_000


# -----------------------------
# Helper: standard invalidation
# -----------------------------

def invalidate(field: Dict[str, Any], reason: str) -> Dict[str, Any]:
    field["valid"] = False
    field["reason"] = reason
    return field


# -----------------------------
# Field Validators
# -----------------------------

def validate_invoice_number(field: Dict[str, Any]) -> Dict[str, Any]:
    value = field.get("value")

    if value is None:
        return field

    if not isinstance(value, str):
        return invalidate(field, "invoice_number_not_string")

    if len(value) > MAX_INVOICE_NUMBER_LENGTH:
        return invalidate(field, "invoice_number_too_long")

    return field


def validate_invoice_date(field: Dict[str, Any]) -> Dict[str, Any]:
    value = field.get("value")

    if value is None:
        return field

    if not isinstance(value, str):
        return invalidate(field, "invoice_date_not_string")

    parsed = parse_date(value)

    if parsed is None:
        return invalidate(field, "invoice_date_invalid_format")

    parsed_date = parsed.parsed
    today = date.today()

    if parsed_date > today:
        return invalidate(field, "invoice_date_in_future")

    if parsed_date.year < 2000:
        return invalidate(field, "invoice_date_too_old")

    # Store normalized ISO date for consistency
    field["value"] = parsed_date.isoformat()
    field["valid"] = True

    # Optional: mark ambiguity for confidence layer
    if parsed.ambiguous:
        field["reason"] = "invoice_date_ambiguous_format_assumed_default"

    return field


def normalize_amount(value: str) -> float | None:
    if not isinstance(value, str):
        return None

    value = value.strip()

    # If both comma and dot exist → decide by last occurrence
    if "," in value and "." in value:
        if value.rfind(",") > value.rfind("."):
            # European style
            value = value.replace(".", "")
            value = value.replace(",", ".")
        else:
            # US style
            value = value.replace(",", "")
    else:
        if "," in value:
            value = value.replace(".", "")
            value = value.replace(",", ".")
        else:
            value = value.replace(",", "")

    try:
        return float(value)
    except ValueError:
        return None


def validate_total_amount(field: Dict[str, Any]) -> Dict[str, Any]:
    value = field.get("value")

    if value is None:
        return field

    if isinstance(value, str):
        parsed = normalize_amount(value)
        if parsed is None:
            return invalidate(field, "total_amount_invalid_format")
        value = parsed

    if not isinstance(value, (int, float)):
        return invalidate(field, "total_amount_not_number")

    if value <= 0:
        return invalidate(field, "total_amount_non_positive")

    if value > MAX_TOTAL_AMOUNT:
        return invalidate(field, "total_amount_exceeds_max")

    field["value"] = float(value)
    field["valid"] = True
    return field


def validate_currency(field: Dict[str, Any]) -> Dict[str, Any]:
    value = field.get("value")

    if value is None:
        return field

    if not isinstance(value, str):
        return invalidate(field, "currency_not_string")

    if value not in ALLOWED_CURRENCIES:
        return invalidate(field, "currency_not_allowed")

    field["value"] = Currency(value)
    field["valid"] = True
    return field


def validate_vendor_name(field: Dict[str, Any]) -> Dict[str, Any]:
    value = field.get("value")

    if value is None:
        return field

    if not isinstance(value, str):
        return invalidate(field, "vendor_name_not_string")

    if len(value) > MAX_VENDOR_NAME_LENGTH:
        return invalidate(field, "vendor_name_too_long")

    if re.fullmatch(r"\d+", value):
        return invalidate(field, "vendor_name_only_numbers")

    field["valid"] = True
    return field


# -----------------------------
# Orchestrator
# -----------------------------

def validate_extraction(data: Dict[str, Any]) -> Dict[str, Any]:

    validators = {
        "invoice_number": validate_invoice_number,
        "invoice_date": validate_invoice_date,
        "total_amount": validate_total_amount,
        "currency": validate_currency,
        "vendor_name": validate_vendor_name,
    }

    validated = {}

    for field_name, field_value in data.items():
        validator = validators.get(field_name)

        if validator:
            validated[field_name] = validator(field_value)
        else:
            validated[field_name] = field_value

    return validated