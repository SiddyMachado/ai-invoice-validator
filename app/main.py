from pathlib import Path
from app.ocr import ocr_pdf, ocr_image
from app.config import INPUT_FOLDER

OUTPUT_FOLDER = r"C:\Users\Siddarth\aiDocumentExtraction\output"
POPPLER_PATH = r"C:\Users\Siddarth\aiDocumentExtraction\.venv\poppler_bin"

PDF_EXTENSIONS = (".pdf",)
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".tiff", ".bmp")

input_path = Path(INPUT_FOLDER)

for file_path in input_path.iterdir():
    if not file_path.is_file():
        continue

    suffix = file_path.suffix.lower()

    if suffix in PDF_EXTENSIONS:
        ocr_pdf(
            pdf_path=str(file_path),
            output_dir=OUTPUT_FOLDER,
            poppler_path=POPPLER_PATH
        )

    elif suffix in IMAGE_EXTENSIONS:
        ocr_image(
            image_path=str(file_path),
            output_dir=OUTPUT_FOLDER
        )
