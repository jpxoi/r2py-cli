import pytest
from actions.download import S3Downloader
from utils.s3base import S3ActionError

class DummyS3Client:
    def head_object(self, Bucket, Key):
        if Key == "fail-key":
            raise Exception("Simulated head_object failure")
        return {"ContentLength": 4}
    def download_fileobj(self, Bucket, Key, fileobj, Callback=None):
        if Bucket == "fail-bucket":
            raise Exception("Simulated download failure")
        if Callback:
            Callback(4)

class DummyProgress:
    def __init__(self, *a, **kw): pass
    def __call__(self, *a, **kw): pass
    def close(self): pass

@pytest.fixture(autouse=True)
def patch_boto3_client(monkeypatch):
    monkeypatch.setattr("boto3.client", lambda *a, **kw: DummyS3Client())

def test_download_file_success(monkeypatch, tmp_path):
    test_file = tmp_path / "file.txt"
    monkeypatch.setattr("actions.download.TqdmProgress", DummyProgress)
    downloader = S3Downloader("url", "key", "secret", "auto")
    downloader.download_file("bucket", "object-key", str(test_file))
    assert test_file.exists()

def test_download_file_missing_key(monkeypatch, tmp_path):
    monkeypatch.setattr("actions.download.TqdmProgress", DummyProgress)
    downloader = S3Downloader("url", "key", "secret", "auto")
    with pytest.raises(S3ActionError):
        downloader.download_file("bucket", None, str(tmp_path / "file.txt"))

def test_download_file_head_object_failure(monkeypatch, tmp_path):
    monkeypatch.setattr("actions.download.TqdmProgress", DummyProgress)
    downloader = S3Downloader("url", "key", "secret", "auto")
    with pytest.raises(S3ActionError):
        downloader.download_file("bucket", "fail-key", str(tmp_path / "file.txt"))

def test_download_file_download_failure(monkeypatch, tmp_path):
    test_file = tmp_path / "file.txt"
    monkeypatch.setattr("actions.download.TqdmProgress", DummyProgress)
    downloader = S3Downloader("url", "key", "secret", "auto")
    with pytest.raises(S3ActionError):
        downloader.download_file("fail-bucket", "object-key", str(test_file))
