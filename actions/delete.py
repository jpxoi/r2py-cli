from utils import S3Base, Colors, Region

class S3Deleter(S3Base):
    """Handles deleting objects from a Cloudflare R2 bucket using the S3-compatible API."""
    def __init__(self, endpoint_url: str, access_key: str, secret_key: str, region: Region = Region.auto):
        """
        Initialize the deleter with S3 credentials and endpoint.
        Args:
            endpoint_url (str): S3-compatible endpoint URL.
            access_key (str): Access key ID.
            secret_key (str): Secret access key.
            region (str): AWS region or 'auto'.
        """
        super().__init__(endpoint_url, access_key, secret_key, region)
        self.logger = S3Base.get_logger()
    
    def delete_bucket(self, bucket_name: str) -> None:
        """
        Delete the specified bucket.
        Args:
            bucket_name (str): Target bucket name.
        """
        self.logger.info(f"Attempting to delete bucket '{bucket_name}'...")
        try:
            response = self.s3.delete_bucket(Bucket=bucket_name)
            self.logger.info(f"Delete response: {response}")
            self.logger.info(f"Successfully deleted bucket '{bucket_name}'")
            print(f"{Colors.OKGREEN}Successfully deleted bucket '{bucket_name}'{Colors.ENDC}")
        except Exception as e:
            self.logger.error(f"Failed to delete bucket: {e}")
            raise

    def delete_object(self, bucket_name: str, object_key: str) -> None:
        """
        Delete an object from the specified bucket.
        Args:
            bucket_name (str): Target bucket name.
            object_key (str): S3 object key to delete.
        """
        self.logger.info(f"Attempting to delete object '{object_key}' from bucket '{bucket_name}'...")
        try:
            response = self.s3.delete_object(Bucket=bucket_name, Key=object_key)
            self.logger.info(f"Delete response: {response}")
            self.logger.info(f"Successfully deleted object '{object_key}' from bucket '{bucket_name}'")
            print(f"{Colors.OKGREEN}Successfully deleted object '{object_key}' from bucket '{bucket_name}'{Colors.ENDC}")
        except Exception as e:
            self.logger.error(f"Failed to delete object: {e}")
            raise
