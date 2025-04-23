import sys
from utils.s3base import S3Base
from utils.colors import Colors
from utils.region import Region

class S3Lister(S3Base):
    """Handles listing buckets, files, etc. from a Cloudflare R2 bucket using the S3-compatible API."""
    def __init__(self, endpoint_url: str, access_key: str, secret_key: str, region: Region = Region.auto):
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

    def list_buckets(self, with_region: bool) -> None:
        """
        List all buckets in the S3-compatible storage.
        """
        try:
            response = self.s3.list_buckets()
            buckets = response.get('Buckets', [])
            print(f"{Colors.HEADER}{Colors.BOLD}=== Buckets ==={Colors.ENDC}")
            if not buckets:
                print(f"{Colors.WARNING}No buckets found.{Colors.ENDC}")
                self.logger.warning("No buckets found.")
            else:
                for bucket in buckets:
                    print(f"{Colors.OKGREEN}Bucket:{Colors.ENDC} {Colors.BOLD}{bucket['Name']}{Colors.ENDC}")
                    if with_region:
                        print(f"  {Colors.OKBLUE}Region:{Colors.ENDC} ", end='')
                        try:
                            region = self.s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint']
                        except Exception as e:
                            region = f"{Colors.FAIL}Error: {e}{Colors.ENDC}"
                        print(f"{region}")
                    print(f"  {Colors.OKCYAN}Created:{Colors.ENDC} {bucket['CreationDate']}\n")

        except Exception as e:
            self.logger.error(f"Error listing buckets: {e}")
            sys.exit(1)
        finally:
            self.logger.info("Finished listing buckets.")

    def list_objects(self, bucket_name: str) -> None:
        """
        List all objects in the specified bucket.
        Args:
            bucket_name (str): Target bucket name.
        """
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name)
            print(f"{Colors.HEADER}{Colors.BOLD}=== Objects in Bucket: {bucket_name} ==={Colors.ENDC}")
            if 'Contents' in response:
                print(f"{Colors.UNDERLINE}%-60s %12s{Colors.ENDC}" % ("Object Key", "Size (bytes)"))
                for obj in response['Contents']:
                    print("%-60s %12d" % (f"{Colors.OKGREEN}{obj['Key']}{Colors.ENDC}", obj['Size']))
            else:
                print(f"{Colors.WARNING}No objects found.{Colors.ENDC}")
        except Exception as e:
            self.logger.error(f"Error listing objects: {e}")
            sys.exit(1)
        finally:
            self.logger.info(f"Finished listing objects in bucket '{bucket_name}'.")

    def list_multipart_uploads(self, bucket_name: str) -> None:
        """
        List all multipart uploads in the specified bucket.
        Args:
            bucket_name (str): Target bucket name.
        """
        try:
            response = self.s3.list_multipart_uploads(Bucket=bucket_name)
            print(f"{Colors.HEADER}{Colors.BOLD}=== Multipart Uploads in Bucket: {bucket_name} ==={Colors.ENDC}")
            if 'Uploads' in response:
                print(f"{Colors.UNDERLINE}%-40s %-40s{Colors.ENDC}" % ("Upload ID", "Object Key"))
                for upload in response['Uploads']:
                    print("%-40s %-40s" % (f"{Colors.OKBLUE}{upload['UploadId']}{Colors.ENDC}", f"{Colors.OKGREEN}{upload['Key']}{Colors.ENDC}"))
            else:
                print(f"{Colors.WARNING}No multipart uploads found.{Colors.ENDC}")
        except Exception as e:
            self.logger.error(f"Error listing multipart uploads: {e}")
            sys.exit(1)
        finally:
            self.logger.info(f"Finished listing multipart uploads in bucket '{bucket_name}'.")

    def list_objects_with_prefix(self, bucket_name: str, prefix: str) -> None:
        """
        List all objects in the specified bucket with a given prefix.
        Args:
            bucket_name (str): Target bucket name.
            prefix (str): Prefix to filter objects.
        """
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            print(f"{Colors.HEADER}{Colors.BOLD}=== Objects in Bucket: {bucket_name} (Prefix: '{prefix}') ==={Colors.ENDC}")
            if 'Contents' in response:
                print(f"{Colors.UNDERLINE}%-60s %12s{Colors.ENDC}" % ("Object Key", "Size (bytes)"))
                for obj in response['Contents']:
                    print("%-60s %12d" % (f"{Colors.OKGREEN}{obj['Key']}{Colors.ENDC}", obj['Size']))
            else:
                print(f"{Colors.WARNING}No objects found with the specified prefix.{Colors.ENDC}")
        except Exception as e:
            self.logger.error(f"Error listing objects with prefix: {e}")
            sys.exit(1)
        finally:
            self.logger.info(f"Finished listing objects with prefix '{prefix}' in bucket '{bucket_name}'.")
