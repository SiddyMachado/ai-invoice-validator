# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

STORAGE_TYPE = os.getenv("STORAGE_TYPE", "railway_bucket")

# ---- S3 / Railway bucket config ----
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
S3_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_REGION = os.getenv("S3_REGION", "auto")


if STORAGE_TYPE == "railway_bucket":
    required = [
        S3_ENDPOINT_URL,
        S3_ACCESS_KEY_ID,
        S3_SECRET_ACCESS_KEY,
        S3_BUCKET_NAME,
    ]
    if not all(required):
        raise ValueError("Missing S3 configuration in .env")

POPPLER_PATH = os.getenv("POPPLER_PATH")