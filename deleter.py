import boto3
from utils.logger import Logger

class S3Deleter:
    def __init__(self, endpoint_url, access_key, secret_key, region):
        self.logger = Logger('deleter').get_logger()
        self.s3 = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region if region != 'auto' else None
        )

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
