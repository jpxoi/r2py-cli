import sys
import argparse
from dotenv import load_dotenv
from actions.upload import S3Uploader
from actions.download import S3Downloader
from actions.delete import S3Deleter
from utils.s3base import S3Base

logger = S3Base.get_logger()  # Updated to use S3Base.get_logger()

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="R2 S3 CLI Tool")
    parser.add_argument('--action', required=True, choices=['upload', 'download', 'delete'], help='Action to perform: upload, download, or delete')
    parser.add_argument('bucket_name', help='S3 bucket name')
    parser.add_argument('file1', help='Source: Local file path (for upload) or S3 object key (for download)')
    parser.add_argument('file2', nargs='?', help='Destination: S3 object key (for upload) or local file path (for download)')
    parser.add_argument('--region', default='auto', choices=["wnam", "enam", "weur", "eeur", "apac", "auto"], help='AWS region name')
    args = parser.parse_args()

    # Load credentials from environment
    ENDPOINT_URL = S3Base.get_env_var('ENDPOINT_URL', required=True)
    AWS_ACCESS_KEY_ID = S3Base.get_env_var('AWS_ACCESS_KEY_ID', required=True)
    AWS_SECRET_ACCESS_KEY = S3Base.get_env_var('AWS_SECRET_ACCESS_KEY', required=True)

    if args.action == 'upload':
        uploader = S3Uploader(
            endpoint_url=ENDPOINT_URL,
            access_key=AWS_ACCESS_KEY_ID,
            secret_key=AWS_SECRET_ACCESS_KEY,
            region=args.region
        )
        filename = args.file1
        object_key = args.file2 if args.file2 else None
        uploader.upload_file(filename, args.bucket_name, object_key)
    elif args.action == 'download':
        downloader = S3Downloader(
            endpoint_url=ENDPOINT_URL,
            access_key=AWS_ACCESS_KEY_ID,
            secret_key=AWS_SECRET_ACCESS_KEY,
            region=args.region
        )
        object_key = args.file1
        filename = args.file2 if args.file2 else None
        downloader.download_file(args.bucket_name, object_key, filename)
    elif args.action == 'delete':
        deleter = S3Deleter(
            endpoint_url=ENDPOINT_URL,
            access_key=AWS_ACCESS_KEY_ID,
            secret_key=AWS_SECRET_ACCESS_KEY,
            region=args.region
        )
        object_key = args.file1
        try:
            deleter.delete_object(args.bucket_name, object_key)
        except Exception as e:
            logger.error(f"Error deleting object: {e}")
            sys.exit(1)
    else:
        logger.error(f"Unknown action: {args.action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
