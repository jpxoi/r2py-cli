from utils.s3base import S3Base

class S3Aborter(S3Base):
    """Handles deleting objects from a Cloudflare R2 bucket using the S3-compatible API."""
    def __init__(self, endpoint_url, access_key, secret_key, region):
        """
        Initialize the aborter with S3 credentials and endpoint.
        Args:
            endpoint_url (str): S3-compatible endpoint URL.
            access_key (str): Access key ID.
            secret_key (str): Secret access key.
            region (str): AWS region or 'auto'.
        """
        super().__init__(endpoint_url, access_key, secret_key, region)
        self.logger = S3Base.get_logger()

    def abort_multipart_upload(self, bucket_name, object_key, upload_id):
        """
        Abort a multipart upload.
        Args:
            bucket_name (str): Target bucket name.
            object_key (str): S3 object key for the multipart upload.
            upload_id (str): The ID of the multipart upload to abort.
        """
        self.logger.info(f"Attempting to abort multipart upload for '{object_key}' with upload ID '{upload_id}' in bucket '{bucket_name}'...")
        try:
            response = self.s3.abort_multipart_upload(Bucket=bucket_name, Key=object_key, UploadId=upload_id)
            self.logger.info(f"Abort response: {response}")
            self.logger.info(f"Successfully aborted multipart upload for '{object_key}' in bucket '{bucket_name}'")
            print(f"Successfully aborted multipart upload for '{object_key}' in bucket '{bucket_name}'")
        except Exception as e:
            self.logger.error(f"Failed to abort multipart upload: {e}")
            raise
