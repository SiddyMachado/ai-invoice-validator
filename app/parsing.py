import re
from dataclasses import dataclass
from datetime import datetime, date
from app.schemas import Currency

DEFAULT_DATE_REGION = "EU"

@dataclass
class ParsedDate:
    raw: str
    parsed: date
    ambiguous: bool

def parse_date(text: str | None, region: str = DEFAULT_DATE_REGION):
    if not text:
        return None

    region = region.upper()
    if region not in ("EU", "US"):
        raise ValueError("Invalid region")

    patterns = re.findall(
    r"\d{1,2}\s*[-/.]\s*\d{1,2}\s*[-/.]\s*\d{4}",
    text
)

    for date_str in patterns:
        parts = re.split(r"[-/.]", date_str)

        first = int(parts[0])
        second = int(parts[1])

        ambiguous = False

        # Normalize separators
        normalized = date_str.replace("-", "/").replace(".", "/")

        # Auto-detect unambiguous cases
        if first > 12:
            fmt = "%d/%m/%Y"
        elif second > 12:
            fmt = "%m/%d/%Y"
        else:
            ambiguous = True
            if region == "EU":
                fmt = "%d/%m/%Y"
            else:
                fmt = "%m/%d/%Y"

        try:
            parsed = datetime.strptime(normalized, fmt).date()
            return ParsedDate(raw=date_str, parsed=parsed, ambiguous=ambiguous)
        except ValueError:
            continue

    return None


def parse_currency(text: str | None) -> Currency | None:
    if not text:
        return None

    text = text.strip().upper()

    symbol_map = {
        "€": Currency.EUR,
        "EUR": Currency.EUR,
        "$": Currency.USD,
        "USD": Currency.USD,
        "₹": Currency.INR,
        "INR": Currency.INR,
        "£": Currency.GBP,
        "GBP": Currency.GBP,
    }

    if text in symbol_map:
        return symbol_map[text]

    # Symbol inside string
    for symbol, currency in symbol_map.items():
        if symbol in text:
            return currency

    return None

def parse_amount(text: str | None):
    if not text:
        return None

    # Remove currency symbols and letters
    cleaned = re.sub(r"[^\d,.\s]", "", text)

    # Remove internal spaces
    cleaned = cleaned.replace(" ", "")

    # European format handling
    if "," in cleaned and "." in cleaned:
        cleaned = cleaned.replace(".", "")
        cleaned = cleaned.replace(",", ".")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", ".")

    try:
        return float(cleaned)
    except ValueError:
        return None