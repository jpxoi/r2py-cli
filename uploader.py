import sys
import os
import logging
import mimetypes
import argparse
from typing import Optional
from dotenv import load_dotenv
import boto3
from tqdm import tqdm

def setup_logging() -> None:
    """Configure logging format and level."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

def get_env_var(name: str, default: Optional[str]=None, required: bool=False) -> str:
    """Get environment variable or exit if required and missing."""
    value = os.getenv(name, default)
    if required and not value:
        logging.error(f"Missing required environment variable: {name}")
        sys.exit(1)
    return value

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

    def __call__(self, bytes_amount: int) -> None:
        self._seen_so_far += bytes_amount
        self._tqdm.update(bytes_amount)

    def close(self) -> None:
        self._tqdm.close()

def upload_file(filename: str, bucket_name: str, object_key: str, s3_client) -> None:
    """Upload a file to S3 with progress bar."""
    if not os.path.isfile(filename):
        logging.error(f"File not found: {filename}")
        sys.exit(1)
    mime_type, _ = mimetypes.guess_type(filename)
    if not mime_type:
        mime_type = "application/octet-stream"
    progress_callback = TqdmProgress(filename)
    try:
        with open(filename, 'rb') as file:
            s3_client.upload_fileobj(
                file,
                bucket_name,
                object_key,
                ExtraArgs={'ContentType': mime_type},
                Callback=progress_callback
            )
        logging.info(f"File '{filename}' uploaded to '{bucket_name}/{object_key}'.")
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        sys.exit(1)
    finally:
        progress_callback.close()

def parse_args():
    parser = argparse.ArgumentParser(description="Upload a file to S3-compatible storage with progress bar.")
    parser.add_argument("bucket_name", help="Target bucket name")
    parser.add_argument("filename", help="Path to the local file to upload")
    parser.add_argument("object_key", nargs="?", help="Object key in the bucket (defaults to filename)")
    parser.add_argument("--region", default="auto", help="AWS region name (default: auto)")
    return parser.parse_args()

def main():
    setup_logging()
    load_dotenv()

    ENDPOINT_URL = get_env_var('ENDPOINT_URL', required=True)
    AWS_ACCESS_KEY_ID = get_env_var('AWS_ACCESS_KEY_ID', required=True)
    AWS_SECRET_ACCESS_KEY = get_env_var('AWS_SECRET_ACCESS_KEY', required=True)

    args = parse_args()
    bucket_name = args.bucket_name
    filename = args.filename
    object_key = args.object_key if args.object_key else os.path.basename(filename)
    region = args.region

    s3 = boto3.client(
        service_name='s3',
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=region,
    )

    try:
        upload_file(filename, bucket_name, object_key, s3)
    except KeyboardInterrupt:
        logging.warning("Upload cancelled by user.")
        sys.exit(1)

if __name__ == "__main__":
    main()