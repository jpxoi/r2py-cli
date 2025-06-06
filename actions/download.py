import sys
import os
from typing import Optional
from utils import TqdmProgress, S3Base, S3ActionError, Region

class S3Downloader(S3Base):
    """Handles downloading files from a Cloudflare R2 bucket using the S3-compatible API."""
    def __init__(self, endpoint_url: str, access_key: str, secret_key: str, region: Region = Region.auto):
        """
        Initialize the downloader with S3 credentials and endpoint.
        Args:
            endpoint_url (str): S3-compatible endpoint URL.
            access_key (str): Access key ID.
            secret_key (str): Secret access key.
            region (Region): AWS region or 'auto'.
        """
        super().__init__(endpoint_url, access_key, secret_key, region)
        self.logger = S3Base.get_logger()

    def download_file(self, bucket_name: str, object_key: str, filename: Optional[str] = None) -> None:
        """
        Download a file from the specified bucket.
        Args:
            bucket_name (str): Source bucket name.
            object_key (str): S3 object key to download.
            filename (Optional[str]): Local file path to save (defaults to object_key basename).
        Raises:
            S3ActionError: If object key is missing, metadata fetch fails, or download fails.
        """
        if not object_key:
            self.logger.warning("Object key not provided.")
            raise S3ActionError("Object key not provided.")
        if not filename:
            filename = os.path.basename(object_key)
        try:
            head = self.s3.head_object(Bucket=bucket_name, Key=object_key)
            total_size = head['ContentLength']
        except Exception as e:
            self.logger.error(f"Could not get object metadata: {e}")
            raise S3ActionError(f"Could not get object metadata: {e}")
        progress_callback = TqdmProgress(filename, action="download", total_size=total_size, logger=self.logger)
        try:
            with open(filename, 'wb') as f:
                self.s3.download_fileobj(
                    bucket_name,
                    object_key,
                    f,
                    Callback=progress_callback
                )
            self.logger.info(f"File '{object_key}' downloaded from '{bucket_name}' to '{filename}'.")
        except Exception as e:
            self.logger.error(f"Error downloading file: {e}")
            raise S3ActionError(f"Error downloading file: {e}")
        finally:
            progress_callback.close()
