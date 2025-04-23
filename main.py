import typer
from dotenv import load_dotenv
from actions.upload import S3Uploader
from actions.download import S3Downloader
from actions.delete import S3Deleter
from actions.list import S3Lister
from utils.s3base import S3Base
from utils.region import Region

app = typer.Typer(help="R2Py CLI Tool")

@app.callback()
def main_callback():
    load_dotenv()

def get_s3_action(action_cls, region: Region):
    ENDPOINT_URL = S3Base.get_env_var('ENDPOINT_URL', required=True)
    AWS_ACCESS_KEY_ID = S3Base.get_env_var('AWS_ACCESS_KEY_ID', required=True)
    AWS_SECRET_ACCESS_KEY = S3Base.get_env_var('AWS_SECRET_ACCESS_KEY', required=True)
    return action_cls(
        endpoint_url=ENDPOINT_URL,
        access_key=AWS_ACCESS_KEY_ID,
        secret_key=AWS_SECRET_ACCESS_KEY,
        region=region.value
    )

@app.command()
def upload(bucket_name: str, filename: str, object_key: str = typer.Argument(None), region: Region = typer.Option(Region.auto, help='AWS region name')):
    """Upload a file to the S3 bucket."""
    uploader = get_s3_action(S3Uploader, region)
    uploader.upload_file(filename, bucket_name, object_key)

@app.command()
def download(bucket_name: str, object_key: str, filename: str = typer.Argument(None), region: Region = typer.Option(Region.auto, help='AWS region name')):
    """Download a file from the S3 bucket."""
    downloader = get_s3_action(S3Downloader, region)
    downloader.download_file(bucket_name, object_key, filename)

@app.command()
def delete(bucket_name: str, object_key: str, region: Region = typer.Option(Region.auto, help='AWS region name')):
    """Delete an object from the S3 bucket."""
    deleter = get_s3_action(S3Deleter, region)
    try:
        deleter.delete_object(bucket_name, object_key)
    except Exception as e:
        typer.echo(f"Error deleting object: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def list(
    bucket_name: str = typer.Argument(None, help="Bucket name (omit for --buckets)", show_default=False),
    region: Region = typer.Option(Region.auto, help='AWS region name'),
    buckets: bool = typer.Option(False, "--buckets", help="List all buckets"),
    with_regions: bool = typer.Option(False, "--with-regions", help="Include regions in the bucket list"),
    multipart: bool = typer.Option(False, "--multipart", help="List multipart uploads in the bucket"),
    prefix: str = typer.Option(None, "--prefix", help="Prefix to filter objects")
):
    """List buckets, objects, or multipart uploads in the S3 bucket."""
    lister = get_s3_action(S3Lister, region)
    try:
        if buckets:
            lister.list_buckets(with_regions)
        elif multipart:
            if not bucket_name:
                typer.echo("Error: --multipart requires a bucket name.", err=True)
                raise typer.Exit(code=1)
            if prefix:
                typer.echo("Error: --multipart and --prefix are mutually exclusive.", err=True)
                raise typer.Exit(code=1)
            lister.list_multipart_uploads(bucket_name)
        elif prefix:
            if not bucket_name:
                typer.echo("Error: --prefix requires a bucket name.", err=True)
                raise typer.Exit(code=1)
            lister.list_objects_with_prefix(bucket_name, prefix)
        else:
            if not bucket_name:
                typer.echo("Error: Must provide a bucket name unless using --buckets.", err=True)
                raise typer.Exit(code=1)
            lister.list_objects(bucket_name)
    except Exception as e:
        typer.echo(f"Error listing: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def abortmultipart(bucket_name: str, object_key: str, upload_id: str, region: Region = typer.Option(Region.auto, help='AWS region name')):
    """Abort a multipart upload."""
    aborter = get_s3_action(S3Deleter, region)
    try:
        aborter.abort_multipart_upload(bucket_name, object_key, upload_id)
    except Exception as e:
        typer.echo(f"Error aborting multipart upload: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
