"""
List Action for R2Py CLI.

This module defines the S3Lister class, which handles the listing of buckets,
objects, and multipart uploads from a Cloudflare R2 bucket using the S3-compatible API.
It provides methods to list buckets, objects, and multipart uploads by specifying
the bucket name and region.
"""

from utils import S3Base, Colors, S3ActionError, Region


class S3Lister(S3Base):
    """
    Handles listing buckets, files, etc. from a Cloudflare R2 bucket using the S3-compatible API.
    """

    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        region: Region = Region.AUTO,
    ):
        """
        Initialize the lister with S3 credentials and endpoint.
        Args:
            endpoint_url (str): S3-compatible endpoint URL.
            access_key (str): Access key ID.
            secret_key (str): Secret access key.
            region (Region): AWS region or 'auto'.
        """
        super().__init__(endpoint_url, access_key, secret_key, region)
        self.logger = S3Base.get_logger()
        self.colorize = Colors.colorize
        self.colorize_bold = Colors.colorize_bold
        self.colorize_underline = Colors.colorize_underline

    def list_buckets(self, with_region: bool) -> None:
        """
        List all buckets in the S3-compatible storage.
        Raises:
            S3ActionError: If listing buckets fails.
        """
        try:
            response = self.s3.list_buckets()
            buckets = response.get("Buckets", [])
            print(self.colorize("=== Buckets ===", "HEADER"))
            if not buckets:
                print(self.colorize("No buckets found.", "WARNING"))
                self.logger.warning("No buckets found.")
            else:
                for bucket in buckets:
                    print(self.colorize(f"Bucket: {bucket['Name']}", "OKGREEN"))
                    if with_region:
                        print(self.colorize("  Region: ", "OKBLUE"), end="")
                        try:
                            region = self.s3.get_bucket_location(Bucket=bucket["Name"])[
                                "LocationConstraint"
                            ]
                        except Exception as e:
                            region = self.colorize(f"Error: {e}", "FAIL")
                        print(f"{region}")
                    print(
                        self.colorize(
                            f"  Created: {bucket['CreationDate']}\n", "OKCYAN"
                        )
                    )
        except Exception as e:
            raise S3ActionError(f"Error listing buckets: {e}") from e
        finally:
            self.logger.info("Finished listing buckets.")

    def list_objects(self, bucket_name: str) -> None:
        """
        List all objects in the specified bucket.
        Args:
            bucket_name (str): Target bucket name.
        Raises:
            S3ActionError: If listing objects fails.
        """
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name)
            print(self.colorize(f"=== Objects in Bucket: {bucket_name} ===", "HEADER"))
            if "Contents" in response:
                print(
                    self.colorize("%-60s %12s", "UNDERLINE")
                    % ("Object Key", "Size (bytes)")
                )
                for obj in response["Contents"]:
                    colored_key = self.colorize(obj["Key"], "OKGREEN")
                    print(f"{colored_key:<60} {obj['Size']:12}")
            else:
                print(self.colorize("No objects found.", "WARNING"))
        except Exception as e:
            raise S3ActionError(f"Error listing objects: {e}") from e
        finally:
            self.logger.info("Finished listing objects in bucket '%s'.", bucket_name)

    def list_multipart_uploads(self, bucket_name: str) -> None:
        """
        List all multipart uploads in the specified bucket.
        Args:
            bucket_name (str): Target bucket name.
        Raises:
            S3ActionError: If listing multipart uploads fails.
        """
        try:
            response = self.s3.list_multipart_uploads(Bucket=bucket_name)
            print(
                self.colorize_bold(
                    f"=== Multipart Uploads in Bucket: {bucket_name} ===", "HEADER"
                )
            )
            if "Uploads" in response:
                print(
                    self.colorize_underline("%-40s %-40s", "UNDERLINE")
                    % ("Upload ID", "Object Key")
                )
                for upload in response["Uploads"]:
                    colored_id = self.colorize(upload["UploadId"], "OKBLUE")
                    colored_key = self.colorize(upload["Key"], "OKGREEN")
                    print(f"{colored_id:<40} {colored_key:<40}")
            else:
                print(self.colorize("No multipart uploads found.", "WARNING"))
        except Exception as e:
            raise S3ActionError(f"Error listing multipart uploads: {e}") from e
        finally:
            self.logger.info(
                "Finished listing multipart uploads in bucket '%s'.", bucket_name
            )

    def list_objects_with_prefix(self, bucket_name: str, prefix: str) -> None:
        """
        List all objects in the specified bucket with a given prefix.
        Args:
            bucket_name (str): Target bucket name.
            prefix (str): Prefix to filter objects.
        Raises:
            S3ActionError: If listing objects with prefix fails.
        """
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            title = f"=== Objects in Bucket: {bucket_name} (Prefix: '{prefix}') ==="
            print(self.colorize_bold(title, "HEADER"))
            if "Contents" in response:
                print(
                    self.colorize_underline("%-60s %12s", "UNDERLINE")
                    % ("Object Key", "Size (bytes)")
                )
                for obj in response["Contents"]:
                    colored_key = self.colorize(obj["Key"], "OKGREEN")
                    print(f"{colored_key:<60} {obj['Size']:12}")
            else:
                print(
                    self.colorize(
                        "No objects found with the specified prefix.", "WARNING"
                    )
                )
        except Exception as e:
            raise S3ActionError(f"Error listing objects with prefix: {e}") from e
        finally:
            self.logger.info(
                "Finished listing objects with prefix '%s' in bucket '%s'.",
                prefix,
                bucket_name,
            )
