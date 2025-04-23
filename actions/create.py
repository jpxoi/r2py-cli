import sys
from utils import S3Base, Colors, Region

class S3Creator(S3Base):
    """Handles creating buckets and managing S3 resources."""
    def __init__(self, endpoint_url: str, access_key: str, secret_key: str, region: Region = Region.auto):
        """
        Initialize the creator with S3 credentials and endpoint.
        Args:
            endpoint_url (str): S3-compatible endpoint URL.
            access_key (str): Access key ID.
            secret_key (str): Secret access key.
            region (str): AWS region or 'auto'.
        """
        super().__init__(endpoint_url, access_key, secret_key, region)
        self.logger = S3Base.get_logger()

    def create_bucket(self, bucket_name: str, region: str = None) -> None:
        """
        Create a new bucket in the S3-compatible storage.
        Args:
            bucket_name (str): Name of the bucket to create.
            region (str): AWS region for the bucket (optional).
        """
        self.logger.info(f"Attempting to create bucket '{bucket_name}'...")
        try:
            if region:
                self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
            else:
                self.s3.create_bucket(Bucket=bucket_name)
            self.logger.info(f"Successfully created bucket '{bucket_name}'")
            print(f"{Colors.OKGREEN}Successfully created bucket '{bucket_name}'{Colors.ENDC}")
        except Exception as e:
            self.logger.error(f"Failed to create bucket: {e}")
            sys.exit(1)
        finally:
            self.logger.info("Finished creating bucket.")
