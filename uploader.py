import sys
import os
import mimetypes
from typing import Optional
import boto3
from utils.logger import Logger
from utils.progress import TqdmProgress

logger = Logger('upload').get_logger()

class S3Uploader:
    def __init__(self, endpoint_url: str, access_key: str, secret_key: str, region: str = "auto"):
        self.logger = logger
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.s3_client = self._create_client()

    def _create_client(self):
        if self.region == "auto":
            self.logger.warning("Region set to 'auto'. Routing requests automatically.")
            self.region = None
        else:
            self.logger.info(f"Using region: {self.region}")
        self.logger.info("Creating S3 client...")
        return boto3.client(
            service_name='s3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region,
        )

    def upload_file(self, filename: str, bucket_name: str, object_key: Optional[str] = None) -> None:
        if not os.path.isfile(filename):
            self.logger.error(f"File not found: {filename}")
            sys.exit(1)
        if not object_key:
            self.logger.warning("Object key not provided. Using filename as object key.")
            object_key = os.path.basename(filename)
        mime_type, _ = mimetypes.guess_type(filename)
        if not mime_type:
            self.logger.warning(f"Could not determine MIME type for {filename}. Defaulting to 'application/octet-stream'.")
            mime_type = "application/octet-stream"
        self.logger.info(f"Uploading '{filename}' to '{bucket_name}/{object_key}' with MIME type '{mime_type}'.")
        progress_callback = TqdmProgress(filename, action="upload", logger=self.logger)

        try:
            with open(filename, 'rb') as file:
                self.s3_client.upload_fileobj(
                    file,
                    bucket_name,
                    object_key,
                    ExtraArgs={'ContentType': mime_type},
                    Callback=progress_callback
                )
            self.logger.info(f"File '{filename}' uploaded to '{bucket_name}/{object_key}'.")
        except Exception as e:
            self.logger.error(f"Error uploading file: {e}")
            sys.exit(1)
        finally:
            progress_callback.close()
