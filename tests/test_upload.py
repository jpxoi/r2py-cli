import pytest
from utils.s3base import S3ActionError
from actions.upload import S3Uploader, S3Base

class DummyS3Client:
    def upload_fileobj(self, file, bucket, key, ExtraArgs=None, Callback=None):
        if bucket == "fail-bucket":
            raise Exception("Simulated upload failure")
        if Callback:
            Callback(1024)

class DummyProgress:
    def __init__(self, *a, **kw): pass
    def __call__(self, *a, **kw): pass
    def close(self): pass

@pytest.fixture(autouse=True)
def patch_boto3_client(monkeypatch):
    import actions.upload
    import utils.s3base
    monkeypatch.setattr("boto3.client", lambda *a, **kw: DummyS3Client())

@pytest.fixture(autouse=True)
def clear_clients_cache():
    # Clear the clients cache before each test to avoid test interference
    S3Base._clients = {}
    yield
    # Clear again after the test
    S3Base._clients = {}

def test_upload_file_success(monkeypatch, tmp_path):
    test_file = tmp_path / "file.txt"
    test_file.write_text("data")
    monkeypatch.setattr("actions.upload.TqdmProgress", DummyProgress)
    uploader = S3Uploader("url", "key", "secret", "auto")
    uploader.upload_file(str(test_file), "bucket", "object-key")

def test_upload_file_not_found(monkeypatch):
    monkeypatch.setattr("actions.upload.TqdmProgress", DummyProgress)
    uploader = S3Uploader("url", "key", "secret", "auto")
    with pytest.raises(S3ActionError):
        uploader.upload_file("/nonexistent/file.txt", "bucket", "object-key")

def test_upload_file_failure(monkeypatch, tmp_path):
    test_file = tmp_path / "file.txt"
    test_file.write_text("data")
    monkeypatch.setattr("actions.upload.TqdmProgress", DummyProgress)
    uploader = S3Uploader("url", "key", "secret", "auto")
    with pytest.raises(S3ActionError):
        uploader.upload_file(str(test_file), "fail-bucket", "object-key")