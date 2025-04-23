import typer
from dotenv import load_dotenv
from actions.upload import S3Uploader
from actions.download import S3Downloader
from actions.delete import S3Deleter
from utils.s3base import S3Base

app = typer.Typer(name="R2", help="R2 S3 CLI Tool")

@app.callback()
def main_callback():
    load_dotenv()

@app.command()
def upload(bucket_name: str, filename: str, object_key: str = typer.Argument(None), region: str = typer.Option('auto', help='AWS region name')):
    """Upload a file to the S3 bucket."""
    ENDPOINT_URL = S3Base.get_env_var('ENDPOINT_URL', required=True)
    AWS_ACCESS_KEY_ID = S3Base.get_env_var('AWS_ACCESS_KEY_ID', required=True)
    AWS_SECRET_ACCESS_KEY = S3Base.get_env_var('AWS_SECRET_ACCESS_KEY', required=True)
    uploader = S3Uploader(
        endpoint_url=ENDPOINT_URL,
        access_key=AWS_ACCESS_KEY_ID,
        secret_key=AWS_SECRET_ACCESS_KEY,
        region=region
    )
    uploader.upload_file(filename, bucket_name, object_key)

@app.command()
def download(bucket_name: str, object_key: str, filename: str = typer.Argument(None), region: str = typer.Option('auto', help='AWS region name')):
    """Download a file from the S3 bucket."""
    ENDPOINT_URL = S3Base.get_env_var('ENDPOINT_URL', required=True)
    AWS_ACCESS_KEY_ID = S3Base.get_env_var('AWS_ACCESS_KEY_ID', required=True)
    AWS_SECRET_ACCESS_KEY = S3Base.get_env_var('AWS_SECRET_ACCESS_KEY', required=True)
    downloader = S3Downloader(
        endpoint_url=ENDPOINT_URL,
        access_key=AWS_ACCESS_KEY_ID,
        secret_key=AWS_SECRET_ACCESS_KEY,
        region=region
    )
    downloader.download_file(bucket_name, object_key, filename)

@app.command()
def delete(bucket_name: str, object_key: str, region: str = typer.Option('auto', help='AWS region name')):
    """Delete an object from the S3 bucket."""
    ENDPOINT_URL = S3Base.get_env_var('ENDPOINT_URL', required=True)
    AWS_ACCESS_KEY_ID = S3Base.get_env_var('AWS_ACCESS_KEY_ID', required=True)
    AWS_SECRET_ACCESS_KEY = S3Base.get_env_var('AWS_SECRET_ACCESS_KEY', required=True)
    deleter = S3Deleter(
        endpoint_url=ENDPOINT_URL,
        access_key=AWS_ACCESS_KEY_ID,
        secret_key=AWS_SECRET_ACCESS_KEY,
        region=region
    )
    try:
        deleter.delete_object(bucket_name, object_key)
    except Exception as e:
        typer.echo(f"Error deleting object: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
