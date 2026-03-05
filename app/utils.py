import re


def clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    return max(min_value, min(max_value, value))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def normalize_number_string(s: str) -> str:
    return re.sub(r"[^\d.]", "", s)

def strip_markdown(text: str) -> str:
    """
    Removes Markdown code fences like ``` or ```json
    and returns clean JSON text.
    """
    text = text.strip()

    if text.startswith("```"):
        # Remove the first and last fence
        text = text.strip("`")

        # Split into lines
        lines = text.splitlines()

        # If first line is a language label like 'json', drop it
        if lines and lines[0].lower() in {"json", "javascript"}:
            lines = lines[1:]

        text = "\n".join(lines)

    return text.strip()
