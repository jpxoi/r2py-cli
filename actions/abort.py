"""
Abort Multipart Upload Action for R2Py CLI.

This module defines the S3Aborter class, which handles the aborting of multipart uploads
from a Cloudflare R2 bucket using the S3-compatible API. It provides a method to abort a
multipart upload by specifying the bucket name, object key, and upload ID.
"""

from utils import S3Base, Colors, S3ActionError, Region

class S3Aborter(S3Base):
    """
    Handles aborting multipart uploads from a Cloudflare R2 bucket using the S3-compatible API.
    """
    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        region: Region = Region.AUTO,
    ):
        """
        Initialize the aborter with S3 credentials and endpoint.
        Args:
            endpoint_url (str): S3-compatible endpoint URL.
            access_key (str): Access key ID.
            secret_key (str): Secret access key.
            region (Region): AWS region or 'auto'.
        """
        super().__init__(endpoint_url, access_key, secret_key, region)
        self.logger = S3Base.get_logger()
        self.colorize = Colors.colorize

    def abort_multipart_upload(self, bucket_name: str, object_key: str, upload_id: str) -> None:
        """
        Abort a multipart upload.
        Args:
            bucket_name (str): Target bucket name.
            object_key (str): S3 object key for the multipart upload.
            upload_id (str): The ID of the multipart upload to abort.
        Raises:
            S3ActionError: If aborting fails.
        """
        self.logger.info(
            "Attempting to abort multipart upload for '%s' with upload ID '%s' in bucket '%s'...",
            object_key, upload_id, bucket_name
        )
        try:
            response = self.s3.abort_multipart_upload(Bucket=bucket_name, Key=object_key, UploadId=upload_id)
            self.logger.debug("Abort response: %s", response)
            self.logger.info(
                "Successfully aborted multipart upload for '%s' in bucket '%s'",
                object_key, bucket_name
            )
            print(self.colorize("Successfully aborted multipart upload for '{object_key}' in bucket '{bucket_name}'", "OKGREEN"))
        except Exception as e:
            raise S3ActionError(f"Failed to abort multipart upload: {e}") from e
        finally:
            self.logger.info("Finished aborting multipart upload.")
