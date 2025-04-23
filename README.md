# R2 S3 Client CLI

This is a command-line tool to upload, download, or delete files to Cloudflare R2 using its S3-compatible API. It is built using Python and the `boto3` library, which provides a simple interface for interacting with S3-compatible storage services.
The CLI is designed to be user-friendly and provides progress bars for uploads and downloads, as well as logging for all operations.
It is a work in progress and may not cover all edge cases or error handling. Please use it with caution and report any issues you encounter.

## Features

- Upload files to R2 buckets
- Download files from R2 buckets
- Delete objects from R2 buckets
- Progress bar and logging for all operations

## Requirements

- Python 3.8+
- Cloudflare R2 account and credentials

## Installation

1. Clone this repository.
2. Create and activate a Python virtual environment (recommended to isolate project dependencies):

    **On Windows:**

    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

    **On macOS/Linux:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies within the virtual environment:

    ```bash
    pip install -r requirements.txt
    ```

## Environment Variables

Before using the CLI, define the following environment variables (e.g., in a `.env` file):

- `ENDPOINT_URL`: The S3-compatible endpoint for your R2 account (e.g., `https://<accountid>.r2.cloudflarestorage.com`)
- `AWS_ACCESS_KEY_ID`: Your R2 access key
- `AWS_SECRET_ACCESS_KEY`: Your R2 secret key

Example `.env`:

```env
ENDPOINT_URL=https://<accountid>.r2.cloudflarestorage.com
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

## Usage

Run the CLI using Python:

```bash
python main.py [OPTIONS] COMMAND [ARGS]
```

### Options

- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
- `--help`: Shows the help message with the available commands.

### Commands

- **upload**: Upload a file to a bucket

    ```bash
    python main.py upload [OPTIONS] BUCKET_NAME FILENAME [OBJECT_KEY]
    ```

  - `BUCKET_NAME`: The name of the R2 bucket.
  - `FILENAME`: The path to the file you want to upload.
  - `OBJECT_KEY`: The key under which to store the file in the bucket. If not provided, the filename will be used.
  - `--region`: Specify the region for the bucket. This is optional and defaults to `auto`.

- **download**: Download a file from a bucket

    ```bash
    python main.py download [OPTIONS] BUCKET_NAME OBJECT_KEY [FILENAME]
    ```

  - `BUCKET_NAME`: The name of the R2 bucket.
  - `OBJECT_KEY`: The key of the object you want to download from the bucket.
  - `FILENAME`: The path where the downloaded file will be saved. If not provided, the object key basename will be used.
  - `--region`: Specify the region for the bucket. This is optional and defaults to `auto`.

- **delete**: Delete an object from a bucket

    ```bash
    python main.py delete [OPTIONS] BUCKET_NAME OBJECT_KEY
    ```

  - `BUCKET_NAME`: The name of the R2 bucket.
  - `OBJECT_KEY`: The key of the object you want to delete from the bucket.
  - `--region`: Specify the region for the bucket. This is optional and defaults to `auto`.

## Testing

There is not yet a test suite for this CLI. Feel free to contribute by adding tests for the existing functionality.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). You can redistribute it and/or modify it under the terms of the GNU General Public License. See the [LICENSE](LICENSE) file for details.
