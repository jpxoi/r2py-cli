import sys
import os
import argparse
from typing import Optional
import boto3
from utils.logger import Logger
from utils.progress import TqdmProgress

logger = Logger('download').get_logger()

class S3Downloader:
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
        progress_callback = TqdmProgress(filename, action="download", total_size=total_size, logger=self.logger)
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
