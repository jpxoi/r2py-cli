import os
import sys
from utils.logger import Logger

logger = Logger('s3base').get_logger()

class S3Base:
    @staticmethod
    def get_env_var(name: str, default=None, required=False):
        value = os.getenv(name, default)
        if required and not value:
            logger.error(f"Missing required environment variable: {name}")
            sys.exit(1)
        logger.debug(f"Environment variable '{name}' loaded successfully.")
        return value
