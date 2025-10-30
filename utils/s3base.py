"""
Base S3 Utility for R2Py CLI.

S3Base manages a singleton S3 client for the CLI, supporting custom endpoints,
credentials, and region selection (incl. 'auto'). Centralizes config and logging.
All S3 actions should inherit from this class for consistency.
"""

import os
import boto3
from utils import Region
from .logger import Logger

logger = Logger("s3Client").get_logger()


class S3ActionError(Exception):
    """Custom exception for S3 action errors."""

    def __init__(self, message: str):
        """Initialize the exception with a message."""
        self.message = message
        super().__init__(self.message)
        self.logger = Logger("s3Client").get_logger()
        self.logger.error("S3 action error: %s", self.message)


class S3Base:
    """Base class for S3-compatible operations with Cloudflare R2."""

    _clients = {}

    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        region: Region = Region.AUTO,
    ):
        """
        Initialize the S3 client with credentials and endpoint, using a singleton pattern.
        Args:
            endpoint_url (str): S3-compatible endpoint URL.
            access_key (str): Access key ID.
            secret_key (str): Secret access key.
            region (Region): AWS region or 'auto'.
        """
        self.logger = logger
        if region == "auto":
            self.logger.warning("Region set to 'auto'. Routing requests automatically.")
            region = None
        else:
            self.logger.info("Using region: %s", region)
        self.logger.info("Creating or reusing S3 client...")
        key = (endpoint_url, access_key, secret_key, region)
        if key not in S3Base._clients:
            S3Base._clients[key] = boto3.client(
                service_name="s3",
                endpoint_url=endpoint_url,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region,
            )
        self.s3 = S3Base._clients[key]

    @staticmethod
    def get_env_var(name: str, default: str = None, required: bool = False) -> str:
        """
        Get an environment variable, optionally requiring it.
        Args:
            name (str): Environment variable name.
            default (str): Default value if not set.
            required (bool): If True, exit if not set.
        Returns:
            str: The environment variable value.
        Raises:
            S3ActionError: If required variable is missing.
        """
        value = os.getenv(name, default)
        if required and not value:
            logger.error("Missing required environment variable: %s", name)
            raise S3ActionError(f"Missing required environment variable: {name}")
        logger.debug("Environment variable '%s' loaded successfully.", name)
        return value

    @staticmethod
    def get_logger() -> Logger:
        """
        Return the shared logger instance for S3 operations.
        """
        return logger
