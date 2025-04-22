import sys
import os
from dotenv import load_dotenv
import boto3
import threading

# Load environment variables from .env file
load_dotenv()

ENDPOINT_URL = os.getenv('ENDPOINT_URL')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Check for required environment variables
required_vars = {
    'ENDPOINT_URL': ENDPOINT_URL,
    'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID,
    'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY
}

missing_vars = [name for name, value in required_vars.items() if not value]

if missing_vars:
    print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    print("Please ensure these are set in your .env file or environment.")
    sys.exit(1)

# Configurations
bucket_name = 'jpxoi' # Replace with your bucket name
filename = 'lisa_coachella_2025_week1.mp4' # Replace with your file path
object_key = 'lisa_coachella_2025_week1.mp4' # Replace with your object key

try:
    with open(filename, 'rb') as file:
        s3 = boto3.client(
            service_name='s3',
            endpoint_url=ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='auto',
        )

        class ProgressPercentage(object):
            def __init__(self, filename):
                self._filename = filename
                self._size = float(os.path.getsize(filename))
                self._seen_so_far = 0
                self._lock = threading.Lock()

            def __call__(self, bytes_amount):
                # To simplify, assume this is hooked up to a single filename
                with self._lock:
                    self._seen_so_far += bytes_amount
                    percentage = (self._seen_so_far / self._size) * 100
                    sys.stdout.write(
                        "\r%s  %s / %s  (%.2f%%)" % (
                            self._filename, self._seen_so_far, self._size,
                            percentage))
                    sys.stdout.flush()

        progress_callback = ProgressPercentage(filename)

        s3.upload_fileobj(
            file,
            bucket_name,
            object_key,
            ExtraArgs={'ContentType': 'video/mp4'},
            Callback=progress_callback
        )
        sys.stdout.write("\n")
        sys.stdout.flush()
    print("File uploaded successfully.")
except Exception as e:
    print(f"Error uploading file: {e}")
    sys.exit(1)