from typing import Optional, Dict


def compute_ocr_confidence(field_name, value, ocr_text, keywords):
    if value is None:
        return 0.0

    text_lower = ocr_text.lower()
    value_str = str(value).lower()

    keyword_hit = any(k in text_lower for k in keywords)
    value_hit = value_str in text_lower

    # ---- Currency special handling ----
    if field_name == "currency":
        symbol_map = {
            "EUR": "€",
            "USD": "$",
            "GBP": "£",
            "INR": "₹"
        }

        currency_code = value.value if hasattr(value, "value") else value
        symbol = symbol_map.get(currency_code)

        symbol_hit = symbol in ocr_text if symbol else False

        if symbol_hit:
            value_hit = True

    # ---- Scoring logic ----
    if keyword_hit and value_hit:
        return 1.0
    elif value_hit:
        return 0.7
    elif keyword_hit:
        return 0.5
    else:
        return 0.0


def compute_confidence(
    field_name: str,
    field_data: dict,
    ocr_text: str,
    keywords: list
) -> dict:

    value = field_data.get("value")

    ocr_score = compute_ocr_confidence(field_name, value, ocr_text, keywords)
    llm_score = compute_llm_confidence(field_data)

    conf = build_confidence(
        ocr=ocr_score,
        llm=llm_score
    )

    conf["overall"] = compute_overall(conf)

    return conf

def build_confidence(
    ocr: Optional[float] = None,
    llm: Optional[float] = None,
) -> Dict[str, Optional[float]]:

    scores = {
        "ocr": ocr,
        "llm": llm,
        "overall": None
    }

    return scores

def compute_validation_confidence(field_data: dict) -> float:
    is_valid = field_data.get("valid", False)
    return 1.0 if is_valid else 0.0

def compute_llm_confidence(field_data: dict) -> float:

    score = 1.0

    penalties = {
        "corrected": 0.15,      # minor auto-fix applied
        "fallback_used": 0.3,   # heuristic or rule-based fallback used
    }

    for flag, penalty in penalties.items():
        if field_data.get(flag, False):
            score -= penalty

    # Prevent confidence from collapsing too low
    score = max(0.4, score)

    return round(score, 3)


def compute_overall(conf: dict) -> float:
    weights = {
        "ocr": 0.5,
        "llm": 0.5,
    }

    total = 0
    weight_sum = 0

    for key, weight in weights.items():
        value = conf.get(key)
        if value is not None:
            total += value * weight
            weight_sum += weight

    if weight_sum == 0:
        return 0.0

    return round(total / weight_sum, 3)

# ----------------------------------
# Document-Level Confidence
# ----------------------------------

CRITICAL_FIELDS = {
    "invoice_number": 0.3,
    "invoice_date": 0.2,
    "total_amount": 0.5
}


def compute_document_confidence(invoice: dict) -> float:
    """
    Aggregates overall confidence of critical fields.
    """

    weighted_sum = 0.0
    total_weight = 0.0

    for field, weight in CRITICAL_FIELDS.items():
        field_conf = invoice[field]["confidence"]["overall"]

        if field_conf is not None:
            weighted_sum += field_conf * weight
            total_weight += weight

    if total_weight == 0:
        return 0.0

    return round(weighted_sum / total_weight, 4)

