import pytest
from actions.list import S3Lister
from utils.s3base import S3ActionError, S3Base

class DummyS3Client:
    def list_buckets(self):
        return {"Buckets": [{"Name": "bucket", "CreationDate": "2025-04-23T00:00:00Z"}]}
    def get_bucket_location(self, Bucket):
        if Bucket == "fail-bucket":
            raise Exception("Simulated get_bucket_location failure")
        return {"LocationConstraint": "auto"}
    def list_objects_v2(self, Bucket, Prefix=None):
        if Bucket == "fail-bucket":
            raise Exception("Simulated list_objects_v2 failure")
        if Prefix:
            return {"Contents": [{"Key": "prefix/file.txt", "Size": 123}]}
        return {"Contents": [{"Key": "file.txt", "Size": 456}]}
    def list_multipart_uploads(self, Bucket):
        if Bucket == "fail-bucket":
            raise Exception("Simulated list_multipart_uploads failure")
        return {"Uploads": [{"UploadId": "upload-id", "Key": "file.txt"}]}

@pytest.fixture(autouse=True)
def patch_boto3_client(monkeypatch):
    monkeypatch.setattr("boto3.client", lambda *a, **kw: DummyS3Client())

@pytest.fixture(autouse=True)
def clear_clients_cache():
    # Clear the clients cache before each test to avoid test interference
    S3Base._clients = {}
    yield
    # Clear again after the test
    S3Base._clients = {}

def test_list_buckets_success():
    lister = S3Lister("url", "key", "secret", "auto")
    lister.list_buckets(with_region=False)

def test_list_buckets_failure(monkeypatch):
    class FailingS3Client(DummyS3Client):
        def list_buckets(self):
            raise Exception("Simulated list_buckets failure")
    monkeypatch.setattr("boto3.client", lambda *a, **kw: FailingS3Client())
    lister = S3Lister("url", "key", "secret", "auto")
    with pytest.raises(S3ActionError):
        lister.list_buckets(with_region=False)

def test_list_objects_success():
    lister = S3Lister("url", "key", "secret", "auto")
    lister.list_objects("bucket")

def test_list_objects_failure(monkeypatch):
    class FailingS3Client(DummyS3Client):
        def list_objects_v2(self, Bucket, Prefix=None):
            raise Exception("Simulated list_objects_v2 failure")
    monkeypatch.setattr("boto3.client", lambda *a, **kw: FailingS3Client())
    lister = S3Lister("url", "key", "secret", "auto")
    with pytest.raises(S3ActionError):
        lister.list_objects("fail-bucket")

def test_list_multipart_uploads_success():
    lister = S3Lister("url", "key", "secret", "auto")
    lister.list_multipart_uploads("bucket")

def test_list_multipart_uploads_failure(monkeypatch):
    class FailingS3Client(DummyS3Client):
        def list_multipart_uploads(self, Bucket):
            raise Exception("Simulated list_multipart_uploads failure")
    monkeypatch.setattr("boto3.client", lambda *a, **kw: FailingS3Client())
    lister = S3Lister("url", "key", "secret", "auto")
    with pytest.raises(S3ActionError):
        lister.list_multipart_uploads("fail-bucket")

def test_list_objects_with_prefix_success():
    lister = S3Lister("url", "key", "secret", "auto")
    lister.list_objects_with_prefix("bucket", "prefix/")

def test_list_objects_with_prefix_failure(monkeypatch):
    class FailingS3Client(DummyS3Client):
        def list_objects_v2(self, Bucket, Prefix=None):
            raise Exception("Simulated list_objects_v2 failure")
    monkeypatch.setattr("boto3.client", lambda *a, **kw: FailingS3Client())
    lister = S3Lister("url", "key", "secret", "auto")
    with pytest.raises(S3ActionError):
        lister.list_objects_with_prefix("fail-bucket", "prefix/")
