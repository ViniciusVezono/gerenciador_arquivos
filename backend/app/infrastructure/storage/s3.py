from typing import BinaryIO
import boto3
from botocore.exceptions import ClientError
from loguru import logger

from app.infrastructure.storage.base import StorageClient
from app.core.config import settings
from app.core.exceptions import StorageException

class S3StorageClient(StorageClient):
    def __init__(self):
        self.bucket = settings.S3_BUCKET_NAME
        self.client = boto3.client(
            "s3", 
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            endpoint_url=settings.AWS_ENDPOINT_URL
        )
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try: 
            self.client.create_bucket(Bucket=self.bucket)
            logger.info(f"Bucket '{self.bucket}' verificado/criado.")
        except ClientError as e: 
            if e.response['Error']['Code'] not in ['BucketAlreadyExists', 'BucketAlreadyOwnedByYou']:
                logger.error(f"Erro ao criar bucket: {e}")

    def upload(self, file: BinaryIO, key: str, content_type: str) -> bool:
        try: 
            self.client.upload_fileobj(
                file,
                self.bucket,
                key,
                ExtraArgs={"ContentType": content_type}
            )
            return True
        except ClientError as e:
            logger.error(f"Erro ao fazer upload no S3: {e}")
            raise StorageException(message="Erro interno ao fazer upload no storage.")

    def delete(self, key: str) -> bool:
        try:
            self.client.delete_object(
                Bucket=self.bucket,
                Key=key
            )
            return True
        except ClientError as e:
            logger.error(f"Erro ao deletar do S3: {e}")
            raise StorageException(message="Erro interno ao deletar do storage.")

    def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        try:
            url = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": key},
                ExpiresIn=expires_in
            )
            # WORKAROUND LocalStack
            return url.replace("http://ministack:4566", "http://localhost:4566")
        except ClientError as e:
            logger.error(f"Erro ao gerar URL no S3: {e}")
            return ""
