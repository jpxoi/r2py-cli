import sys
from utils.s3base import S3Base
from utils.colors import Colors
from utils.region import Region

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

    def create_bucket(self, bucket_name: str, region: Region) -> None:
        """
        Create a new bucket in the S3-compatible storage.
        Args:
            bucket_name (str): Name of the bucket to create.
            region (str): AWS region for the bucket.
        """
        self.logger.info(f"Attempting to create bucket '{bucket_name}' in region '{region}'...")
        try:
            self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
            self.logger.info(f"Successfully created bucket '{bucket_name}' in region '{region}'")
            print(f"{Colors.OKGREEN}Successfully created bucket '{bucket_name}' in region '{region}'{Colors.ENDC}")
        except Exception as e:
            self.logger.error(f"Failed to create bucket '{bucket_name}' in region '{region}': {e}")
            sys.exit(1)
        finally:
            self.logger.info(f"Finished attempt to create bucket '{bucket_name}'.")
