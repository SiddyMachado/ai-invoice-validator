from app.config import STORAGE_TYPE
from app.services.storage import S3Storage

def get_storage():
    if STORAGE_TYPE == "railway_bucket":
        return S3Storage()

    raise ValueError(f"Unsupported storage type: {STORAGE_TYPE}")