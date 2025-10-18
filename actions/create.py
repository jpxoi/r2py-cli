"""
Create Bucket Action for R2Py CLI.

This module defines the S3Creator class, which handles the creation of buckets
in a Cloudflare R2 bucket using the S3-compatible API. It provides a method to
create a bucket by specifying the bucket name and region.
"""

from utils import S3Base, Colors, S3ActionError, Region

class S3Creator(S3Base):
    """Handles creating buckets and managing S3 resources."""
    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        region: Region = Region.AUTO
    ):
        """
        Initialize the creator with S3 credentials and endpoint.
        Args:
            endpoint_url (str): S3-compatible endpoint URL.
            access_key (str): Access key ID.
            secret_key (str): Secret access key.
            region (Region): AWS region or 'auto'.
        """
        super().__init__(endpoint_url, access_key, secret_key, region)
        self.logger = S3Base.get_logger()
        self.colorize = Colors.colorize

    def create_bucket(self, bucket_name: str, region: str = None) -> None:
        """
        Create a new bucket in the S3-compatible storage.
        Args:
            bucket_name (str): Name of the bucket to create.
            region (str): AWS region for the bucket (optional).
        Raises:
            S3ActionError: If creation fails.
        """
        self.logger.info("Attempting to create bucket '%s'", bucket_name)
        try:
            if region:
                self.s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': region
                    }
                )
            else:
                self.s3.create_bucket(Bucket=bucket_name)
            self.logger.info("Successfully created bucket '%s'", bucket_name)
            print(self.colorize(f"Successfully created bucket '{bucket_name}'", "OKGREEN"))
        except Exception as e:
            raise S3ActionError(f"Failed to create bucket: {e}") from e
        finally:
            self.logger.info("Finished creating bucket.")
