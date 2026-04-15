import boto3
from uuid import uuid4
from app.config import (
    S3_ENDPOINT_URL,
    S3_ACCESS_KEY_ID,
    S3_SECRET_ACCESS_KEY,
    S3_BUCKET_NAME,
)


class S3Storage:
    def __init__(self):
        self.bucket = S3_BUCKET_NAME

        self.client = boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT_URL,
            aws_access_key_id=S3_ACCESS_KEY_ID,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY,
        )

    def save_file(self, file_bytes: bytes, filename: str) -> str:
        key = f"uploads/{uuid4()}_{filename}"

        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=file_bytes
        )

        return key

    def read_file(self, key: str) -> bytes:
        obj = self.client.get_object(
            Bucket=self.bucket,
            Key=key
        )
        return obj["Body"].read()