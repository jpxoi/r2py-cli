import os
import sys
import boto3
from utils.logger import Logger

logger = Logger('s3Client').get_logger()

class S3Base:
    def __init__(self, endpoint_url, access_key, secret_key, region):
        self.logger = logger
        if region == 'auto':
            self.logger.warning("Region set to 'auto'. Routing requests automatically.")
            region = None
        else:
            self.logger.info(f"Using region: {region}")
        self.logger.info("Creating S3 client...")
        self.s3 = boto3.client(
            service_name='s3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    @staticmethod
    def get_env_var(name: str, default=None, required=False):
        value = os.getenv(name, default)
        if required and not value:
            logger.error(f"Missing required environment variable: {name}")
            sys.exit(1)
        logger.debug(f"Environment variable '{name}' loaded successfully.")
        return value

    @staticmethod
    def get_logger():
        return logger