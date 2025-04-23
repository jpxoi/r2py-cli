# R2Py CLI Tool

![GitHub](https://img.shields.io/github/license/jpxoi/r2py-cli)
![GitHub last commit](https://img.shields.io/github/last-commit/jpxoi/r2py-cli)
![GitHub issues](https://img.shields.io/github/issues/jpxoi/r2py-cli)
![GitHub pull requests](https://img.shields.io/github/issues-pr/jpxoi/r2py-cli)
![GitHub contributors](https://img.shields.io/github/contributors/jpxoi/r2py-cli)

This is a command-line tool to interact with Cloudflare R2 storage. It allows you to upload, download, delete, and list objects in your R2 buckets. The tool is designed to be simple and efficient, making it easy to manage your files in R2. This is a command-line tool to interact with Cloudflare R2 using its S3-compatible API. It is built using Python and the `boto3` library, which provides a simple interface for interacting with S3-compatible storage services.

> [!NOTE]
> This project is not an official Cloudflare product and is not maintained by Cloudflare. It is an open-source project created by the community for the community.

> [!CAUTION]
> This is a work in progress and may not cover all edge cases or error handling. Please use it with caution and report any issues you encounter.

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

- **list**: List buckets, objects, or multipart uploads

    ```bash
    python main.py list [OPTIONS] [BUCKET_NAME]
    ```

  - `BUCKET_NAME`: The name of the R2 bucket (omit for --buckets).
  - `--buckets`: List all buckets (omit BUCKET_NAME).
  - `--with-region`: Show region info when listing buckets.
  - `--multipart`: List multipart uploads in the bucket (requires BUCKET_NAME).
  - `--prefix`: Filter objects by prefix (requires BUCKET_NAME).
  - `--region`: Specify the region for the bucket. This is optional and defaults to `auto`.

  **Examples:**
  - List all buckets: `python main.py list --buckets`
  - List all buckets with region: `python main.py list --buckets --with-region`
  - List objects in a bucket: `python main.py list my-bucket`
  - List objects with prefix: `python main.py list my-bucket --prefix images/`
  - List multipart uploads: `python main.py list my-bucket --multipart`

- **create**: Create a new bucket

    ```bash
    python main.py create [OPTIONS] BUCKET_NAME
    ```

  - `BUCKET_NAME`: The name of the R2 bucket to create.
  - `--region`: Specify the region for the bucket. This is optional and defaults to `auto`.

  **Example:**

  ```bash
  python main.py create my-new-bucket
  ```

- **upload**: Upload a file to a bucket

    ```bash
    python main.py upload [OPTIONS] BUCKET_NAME FILENAME [OBJECT_KEY]
    ```

  - `BUCKET_NAME`: The name of the R2 bucket.
  - `FILENAME`: The path to the file you want to upload.
  - `OBJECT_KEY`: The key under which to store the file in the bucket. If not provided, the filename will be used.
  - `--region`: Specify the region for the bucket. This is optional and defaults to `auto`.

  **Example:**

  ```bash
  python main.py upload my-bucket /path/to/file.txt
  ```

  This will upload `file.txt` to `my-bucket` with the same name (i.e., `file.txt`).
  If you want to specify a different object key, you can do so like this:

  ```bash
    python main.py upload my-bucket /path/to/file.txt my-object-key
  ```

  This will upload `file.txt` to `my-bucket` with the key `my-object-key`.

- **download**: Download a file from a bucket

    ```bash
    python main.py download [OPTIONS] BUCKET_NAME OBJECT_KEY [FILENAME]
    ```

  - `BUCKET_NAME`: The name of the R2 bucket.
  - `OBJECT_KEY`: The key of the object you want to download from the bucket.
  - `FILENAME`: The path where the downloaded file will be saved. If not provided, the object key basename will be used.
  - `--region`: Specify the region for the bucket. This is optional and defaults to `auto`.

    **Example:**

    ```bash
    python main.py download my-bucket my-object-key /path/to/save/file.txt
    ```

    This will download the object with key `my-object-key` from `my-bucket` and save it as `file.txt`.
    If you want to save it with the same name as the object key, you can omit the `FILENAME` argument:

    ```bash
    python main.py download my-bucket my-object-key
    ```

    This will download the object with key `my-object-key` from `my-bucket` and save it with the same name.

- **delete**: Delete an object from a bucket or delete a bucket if no object key is provided

    ```bash
    python main.py delete [OPTIONS] BUCKET_NAME OBJECT_KEY
    ```

  - `BUCKET_NAME`: The name of the R2 bucket.
  - `OBJECT_KEY`: The key of the object you want to delete from the bucket. If not provided, the bucket will be deleted.
  - `--region`: Specify the region for the bucket. This is optional and defaults to `auto`.

- **abort**: Abort a multipart upload

    ```bash
    python main.py abort [OPTIONS] BUCKET_NAME OBJECT_KEY UPLOAD_ID
    ```

  - `BUCKET_NAME`: The name of the R2 bucket.
  - `OBJECT_KEY`: The key of the object being uploaded.
  - `UPLOAD_ID`: The multipart upload ID to abort.
  - `--region`: Specify the region for the bucket. This is optional and defaults to `auto`.

## Improved CLI UI

- All output is colorized for better readability (bucket names, object keys, errors, etc.).
- Listings are formatted in tables with headers.
- Clear error messages and progress feedback for all operations.

## Testing

There is not yet a test suite for this CLI. Feel free to contribute by adding tests for the existing functionality.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). You can redistribute it and/or modify it under the terms of the GNU General Public License. See the [LICENSE](LICENSE) file for details.
