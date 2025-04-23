from utils.s3base import S3Base

class S3Deleter(S3Base):
    def __init__(self, endpoint_url, access_key, secret_key, region):
        super().__init__(endpoint_url, access_key, secret_key, region)
        self.logger = S3Base.get_logger()

    def delete_object(self, bucket_name, object_key):
        self.logger.info(f"Attempting to delete object '{object_key}' from bucket '{bucket_name}'...")
        try:
            response = self.s3.delete_object(Bucket=bucket_name, Key=object_key)
            self.logger.info(f"Delete response: {response}")
            self.logger.info(f"Successfully deleted object '{object_key}' from bucket '{bucket_name}'")
            print(f"Successfully deleted object '{object_key}' from bucket '{bucket_name}'")
        except Exception as e:
            self.logger.error(f"Failed to delete object: {e}")
            raise
