from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
from io import BytesIO


def ocr_pdf(pdf_bytes: bytes, poppler_path: str = None) -> str:

    if poppler_path:
        images = convert_from_bytes(
            pdf_bytes,
            poppler_path=poppler_path
        )
    else:
        images = convert_from_bytes(pdf_bytes)

    full_text = ""

    for page_num, image in enumerate(images, start=1):
        page_text = pytesseract.image_to_string(image)
        full_text += f"\n--- Page {page_num} ---\n{page_text}"

    return full_text


def ocr_image(image_bytes: bytes) -> str:
    image = Image.open(BytesIO(image_bytes))
    image = image.convert("RGB")
    text = pytesseract.image_to_string(image)
    return text


def run_ocr(file_bytes: bytes, suffix: str, poppler_path: str = None) -> str:

    if suffix == ".pdf":
        return ocr_pdf(
            pdf_bytes=file_bytes,
            poppler_path=poppler_path
        )
    else:
        return ocr_image(
            image_bytes=file_bytes
        )