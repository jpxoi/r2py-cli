import sys
import os
import mimetypes
import argparse
from typing import Optional
from dotenv import load_dotenv
import boto3
from tqdm import tqdm
from logger import Logger

logger = Logger('upload').get_logger()

class TqdmProgress:
    """Progress bar callback for S3 uploads."""
    def __init__(self, filename: str):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._tqdm = tqdm(
            total=self._size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc=os.path.basename(filename),
            leave=True,
            dynamic_ncols=True
        )
        self._seen_so_far = 0
        self.logger = logger
        self.logger.info(f"Starting upload for {self._filename} ({self._size / (1024 * 1024):.2f} MB)")
        self.logger.info(f"Progress bar initialized for {self._filename}")
        self.logger.info(f"File size: {self._size / (1024 * 1024):.2f} MB")

    def __call__(self, bytes_amount: int) -> None:
        self._seen_so_far += bytes_amount
        self._tqdm.update(bytes_amount)
        self.logger.debug(f"Uploaded {self._seen_so_far / (1024 * 1024):.2f} MB of {self._filename}")

    def close(self) -> None:
        self._tqdm.close()

class S3Uploader:
    def __init__(self, endpoint_url: str, access_key: str, secret_key: str, region: str = "auto"):
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.s3_client = self._create_client()
        self.logger = logger

    @staticmethod
    def get_env_var(name: str, default: Optional[str]=None, required: bool=False) -> str:
        value = os.getenv(name, default)
        if required and not value:
            logger.error(f"Missing required environment variable: {name}")
            sys.exit(1)
        return value

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
        progress_callback = TqdmProgress(filename)

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

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description="Upload a file to S3-compatible storage with progress bar.")
        parser.add_argument("bucket_name", help="Target bucket name")
        parser.add_argument("filename", help="Path to the local file to upload")
        parser.add_argument("object_key", nargs="?", help="Object key in the bucket (defaults to filename)")
        parser.add_argument(
            "--region",
            default="auto",
            choices=["wnam", "enam", "weur", "eeur", "apac", "auto"],
            help="AWS region name (choices: wnam, enam, weur, eeur, apac, auto; default: auto)"
        )
        return parser.parse_args()

def main():
    load_dotenv()

    ENDPOINT_URL = S3Uploader.get_env_var('ENDPOINT_URL', required=True)
    AWS_ACCESS_KEY_ID = S3Uploader.get_env_var('AWS_ACCESS_KEY_ID', required=True)
    AWS_SECRET_ACCESS_KEY = S3Uploader.get_env_var('AWS_SECRET_ACCESS_KEY', required=True)

    args = S3Uploader.parse_args()
    uploader = S3Uploader(
        endpoint_url=ENDPOINT_URL,
        access_key=AWS_ACCESS_KEY_ID,
        secret_key=AWS_SECRET_ACCESS_KEY,
        region=args.region
    )

    try:
        uploader.upload_file(args.filename, args.bucket_name, args.object_key)
    except KeyboardInterrupt:
        logger.warning("Upload cancelled by user.")
        sys.exit(1)

if __name__ == "__main__":
    main()