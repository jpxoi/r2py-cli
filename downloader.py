import sys
import os
import argparse
from typing import Optional
from dotenv import load_dotenv
import boto3
from tqdm import tqdm
from logger import Logger

logger = Logger('download').get_logger()

class TqdmProgress:
    """Progress bar callback for S3 downloads."""
    def __init__(self, filename: str, total_size: int):
        self._filename = filename
        self._size = float(total_size)
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
        self.logger.info(f"Starting download for {self._filename} ({self._size / (1024 * 1024):.2f} MB)")
        self.logger.info(f"Progress bar initialized for {self._filename}")
        self.logger.info(f"File size: {self._size / (1024 * 1024):.2f} MB")

    def __call__(self, bytes_amount: int) -> None:
        self._seen_so_far += bytes_amount
        self._tqdm.update(bytes_amount)
        self.logger.debug(f"Downloaded {self._seen_so_far / (1024 * 1024):.2f} MB of {self._filename}")

    def close(self) -> None:
        self._tqdm.close()

class S3Downloader:
    def __init__(self, endpoint_url: str, access_key: str, secret_key: str, region: str = "auto"):
        self.logger = logger
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.s3_client = self._create_client()

    @staticmethod
    def get_env_var(name: str, default: Optional[str]=None, required: bool=False) -> str:
        value = os.getenv(name, default)
        if required and not value:
            logger.error(f"Missing required environment variable: {name}")
            sys.exit(1)
        logger.debug(f"Environment variable '{name}' loaded successfully.")
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

    def download_file(self, bucket_name: str, object_key: str, filename: Optional[str] = None) -> None:
        if not object_key:
            self.logger.warning("Object key not provided.")
            sys.exit(1)
        if not filename:
            filename = os.path.basename(object_key)
        try:
            head = self.s3_client.head_object(Bucket=bucket_name, Key=object_key)
            total_size = head['ContentLength']
        except Exception as e:
            self.logger.error(f"Could not get object metadata: {e}")
            sys.exit(1)
        progress_callback = TqdmProgress(filename, total_size)
        try:
            with open(filename, 'wb') as f:
                self.s3_client.download_fileobj(
                    bucket_name,
                    object_key,
                    f,
                    Callback=progress_callback
                )
            self.logger.info(f"File '{object_key}' downloaded from '{bucket_name}' to '{filename}'.")
        except Exception as e:
            self.logger.error(f"Error downloading file: {e}")
            sys.exit(1)
        finally:
            progress_callback.close()

    @staticmethod
    def parse_args():
        logger.info("Parsing command line arguments.")
        parser = argparse.ArgumentParser(description="Download a file from S3-compatible storage with progress bar.")
        parser.add_argument("bucket_name", help="Source bucket name")
        parser.add_argument("object_key", help="Object key in the bucket")
        parser.add_argument("filename", nargs="?", help="Destination local filename (defaults to object key)")
        parser.add_argument(
            "--region",
            default="auto",
            choices=["wnam", "enam", "weur", "eeur", "apac", "auto"],
            help="AWS region name (choices: wnam, enam, weur, eeur, apac, auto; default: auto)"
        )
        logger.debug("Command line arguments parsed successfully.")
        return parser.parse_args()

def main():
    load_dotenv()
    logger.info("Loading environment variables from .env file.")

    ENDPOINT_URL = S3Downloader.get_env_var('ENDPOINT_URL', required=True)
    AWS_ACCESS_KEY_ID = S3Downloader.get_env_var('AWS_ACCESS_KEY_ID', required=True)
    AWS_SECRET_ACCESS_KEY = S3Downloader.get_env_var('AWS_SECRET_ACCESS_KEY', required=True)

    args = S3Downloader.parse_args()
    downloader = S3Downloader(
        endpoint_url=ENDPOINT_URL,
        access_key=AWS_ACCESS_KEY_ID,
        secret_key=AWS_SECRET_ACCESS_KEY,
        region=args.region
    )

    try:
        downloader.download_file(args.bucket_name, args.object_key, args.filename)
    except KeyboardInterrupt:
        logger.warning("Download cancelled by user.")
        sys.exit(1)

if __name__ == "__main__":
    main()
