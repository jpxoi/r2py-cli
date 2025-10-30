"""
Delete Action for R2Py CLI.

This module defines the S3Deleter class, which handles the deletion of objects
and buckets from a Cloudflare R2 bucket using the S3-compatible API. It provides
a method to delete an object by specifying the bucket name and object key,
and a method to delete a bucket by specifying the bucket name.
"""

from utils import Colors, Region, S3ActionError, S3Base


class S3Deleter(S3Base):
    """Handles deleting objects from a Cloudflare R2 bucket using the S3-compatible API."""

    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        region: Region = Region.AUTO,
    ):
        """
        Initialize the deleter with S3 credentials and endpoint.
        Args:
            endpoint_url (str): S3-compatible endpoint URL.
            access_key (str): Access key ID.
            secret_key (str): Secret access key.
            region (Region): AWS region or 'auto'.
        """
        super().__init__(endpoint_url, access_key, secret_key, region)
        self.logger = S3Base.get_logger()
        self.colorize = Colors.colorize

    def delete_bucket(self, bucket_name: str) -> None:
        """
        Delete the specified bucket.
        Args:
            bucket_name (str): Target bucket name.
        Raises:
            S3ActionError: If deletion fails.
        """
        self.logger.info("Attempting to delete bucket '%s'", bucket_name)
        try:
            response = self.s3.delete_bucket(Bucket=bucket_name)
            self.logger.debug("Delete response: %s", response)
            self.logger.info("Successfully deleted bucket '%s'", bucket_name)
            print(
                self.colorize(f"Successfully deleted bucket '{bucket_name}'", "OKGREEN")
            )
        except Exception as e:
            raise S3ActionError(f"Failed to delete bucket: {e}") from e

    def delete_object(self, bucket_name: str, object_key: str) -> None:
        """
        Delete an object from the specified bucket.
        Args:
            bucket_name (str): Target bucket name.
            object_key (str): S3 object key to delete.
        Raises:
            S3ActionError: If deletion fails.
        """
        self.logger.info(
            "Attempting to delete object '%s' from bucket '%s'...",
            object_key,
            bucket_name,
        )
        try:
            response = self.s3.delete_object(Bucket=bucket_name, Key=object_key)
            self.logger.debug("Delete response: %s", response)
            self.logger.info("Object deleted: %s/%s", bucket_name, object_key)
            print(
                self.colorize(
                    f"Successfully deleted object '{object_key}' from bucket '{bucket_name}'",
                    "OKGREEN",
                )
            )
        except Exception as e:
            raise S3ActionError(f"Failed to delete object: {e}") from e
