import sys
import os
from typing import Optional
from utils.progress import TqdmProgress
from utils.s3base import S3Base

class S3Lister(S3Base):
    """Handles listing buckets, files, etc. from a Cloudflare R2 bucket using the S3-compatible API."""
    def __init__(self, endpoint_url: str, access_key: str, secret_key: str, region: str = "auto"):
        """
        Initialize the lister with S3 credentials and endpoint.
        Args:
            endpoint_url (str): S3-compatible endpoint URL.
            access_key (str): Access key ID.
            secret_key (str): Secret access key.
            region (str): AWS region or 'auto'.
        """
        super().__init__(endpoint_url, access_key, secret_key, region)
        self.logger = S3Base.get_logger()

    def list_buckets(self, with_regions: bool) -> None:
        """
        List all buckets in the S3-compatible storage.
        """
        try:
            response = self.s3.list_buckets()
            buckets = response.get('Buckets', [])
            if not buckets:
                self.logger.warning("No buckets found.")
            else:
                for bucket in buckets:
                    self.logger.info(f"Bucket: {bucket['Name']} with creation date {bucket['CreationDate']}")
                    print(f"Bucket: {bucket['Name']}")
                    if with_regions:
                        self.logger.info(f"Fetching region for bucket '{bucket['Name']}'...")
                        region = self.s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint']
                        self.logger.info(f"Region: {region}")
                        print(f"Region: {region}")
                    print(f"Creation Date: {bucket['CreationDate']}\n")
                    
        except Exception as e:
            self.logger.error(f"Error listing buckets: {e}")
            sys.exit(1)
        finally:
            self.logger.info("Finished listing buckets.")
            print("Finished listing buckets.")
            sys.exit(0)

    def list_objects(self, bucket_name: str) -> None:
        """
        List all objects in the specified bucket.
        Args:
            bucket_name (str): Target bucket name.
        """
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in response:
                for obj in response['Contents']:
                    print(f"Object: {obj['Key']}, Size: {obj['Size']} bytes")
            else:
                print("No objects found.")
        except Exception as e:
            self.logger.error(f"Error listing objects: {e}")
            sys.exit(1)
        finally:
            self.logger.info(f"Finished listing objects in bucket '{bucket_name}'.")
            print(f"Finished listing objects in bucket '{bucket_name}'.")
            sys.exit(0)
    
    def list_multipart_uploads(self, bucket_name: str) -> None:
        """
        List all multipart uploads in the specified bucket.
        Args:
            bucket_name (str): Target bucket name.
        """
        try:
            response = self.s3.list_multipart_uploads(Bucket=bucket_name)
            if 'Uploads' in response:
                for upload in response['Uploads']:
                    print(f"Upload ID: {upload['UploadId']}, Key: {upload['Key']}")
            else:
                print("No multipart uploads found.")
        except Exception as e:
            self.logger.error(f"Error listing multipart uploads: {e}")
            sys.exit(1)
        finally:
            self.logger.info(f"Finished listing multipart uploads in bucket '{bucket_name}'.")
            print(f"Finished listing multipart uploads in bucket '{bucket_name}'.")
            sys.exit(0)

    def list_objects_with_prefix(self, bucket_name: str, prefix: str) -> None:
        """
        List all objects in the specified bucket with a given prefix.
        Args:
            bucket_name (str): Target bucket name.
            prefix (str): Prefix to filter objects.
        """
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            if 'Contents' in response:
                for obj in response['Contents']:
                    print(f"Object: {obj['Key']}, Size: {obj['Size']} bytes")
            else:
                print("No objects found with the specified prefix.")
        except Exception as e:
            self.logger.error(f"Error listing objects with prefix: {e}")
            sys.exit(1)
        finally:
            self.logger.info(f"Finished listing objects with prefix '{prefix}' in bucket '{bucket_name}'.")
            print(f"Finished listing objects with prefix '{prefix}' in bucket '{bucket_name}'.")
            sys.exit(0)
