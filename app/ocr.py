from pathlib import Path
from PIL import Image
import pytesseract
from pdf2image import convert_from_path


def ocr_pdf(pdf_path: str, output_dir: str, poppler_path: str):
    """
    Converts a PDF into text using OCR.
    Each PDF page is converted to an image, then OCR is applied.
    """
    images = convert_from_path(pdf_path, poppler_path=poppler_path)

    full_text = ""

    for page_num, image in enumerate(images, start=1):
        page_text = pytesseract.image_to_string(image)
        full_text += f"\n--- Page {page_num} ---\n{page_text}"

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    output_file = Path(output_dir) / f"{Path(pdf_path).stem}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_text)


def ocr_image(image_path: str, output_dir: str):
    """
    Converts a single image into text using OCR.
    """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    output_file = Path(output_dir) / f"{Path(image_path).stem}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
