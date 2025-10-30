"""
Upload Action for R2Py CLI.

This module defines the S3Uploader class, which handles the uploading of files
to a Cloudflare R2 bucket using the S3-compatible API. It provides a method to
upload a file by specifying the filename, bucket name, and object key.
"""

import mimetypes
import os
from typing import Optional

from utils import Region, S3ActionError, S3Base, TqdmProgress


class S3Uploader(S3Base):
    """Handles uploading files to a Cloudflare R2 bucket using the S3-compatible API."""

    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        region: Region = Region.AUTO,
    ):
        """
        Initialize the uploader with S3 credentials and endpoint.
        Args:
            endpoint_url (str): S3-compatible endpoint URL.
            access_key (str): Access key ID.
            secret_key (str): Secret access key.
            region (Region): AWS region or 'auto'.
        """
        super().__init__(endpoint_url, access_key, secret_key, region)
        self.logger = S3Base.get_logger()

    def upload_file(
        self, filename: str, bucket_name: str, object_key: Optional[str] = None
    ) -> None:
        """
        Upload a file to the specified bucket.
        Args:
            filename (str): Local file path to upload.
            bucket_name (str): Target bucket name.
            object_key (Optional[str]): S3 object key (defaults to filename).
        Raises:
            S3ActionError: If file not found or upload fails.
        """
        if not os.path.isfile(filename):
            raise S3ActionError(f"File not found: {filename}")
        if not object_key:
            self.logger.warning(
                "Object key not provided. Using filename as object key."
            )
            object_key = os.path.basename(filename)
        mime_type, _ = mimetypes.guess_type(filename)
        if not mime_type:
            self.logger.warning(
                "Could not determine MIME type for %s. "
                "Defaulting to 'application/octet-stream'.",
                filename,
            )
            mime_type = "application/octet-stream"
        self.logger.info(
            "Uploading '%s' to '%s/%s' with MIME type '%s'.",
            filename,
            bucket_name,
            object_key,
            mime_type,
        )
        progress_callback = TqdmProgress(filename, action="upload", logger=self.logger)

        try:
            with open(filename, "rb") as file:
                self.s3.upload_fileobj(
                    file,
                    bucket_name,
                    object_key,
                    ExtraArgs={"ContentType": mime_type},
                    Callback=progress_callback,
                )
            self.logger.info(
                "File '%s' uploaded to '%s/%s'.", filename, bucket_name, object_key
            )
        except Exception as e:
            raise S3ActionError(f"Error uploading file: {e}") from e
        finally:
            progress_callback.close()
