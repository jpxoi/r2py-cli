import pytest
from actions.delete import S3Deleter
from utils.s3base import S3ActionError, S3Base


class DummyS3Client:
    def delete_bucket(self, Bucket):
        if Bucket == "fail-bucket":
            raise Exception("Simulated delete_bucket failure")
        return {"ResponseMetadata": {"HTTPStatusCode": 204}}

    def delete_object(self, Bucket, Key):
        if Key == "fail-key":
            raise Exception("Simulated delete_object failure")
        return {"ResponseMetadata": {"HTTPStatusCode": 204}}


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


def test_delete_bucket_success():
    deleter = S3Deleter("url", "key", "secret", "auto")
    deleter.delete_bucket("bucket")


def test_delete_bucket_failure():
    deleter = S3Deleter("url", "key", "secret", "auto")
    with pytest.raises(S3ActionError):
        deleter.delete_bucket("fail-bucket")


def test_delete_object_success():
    deleter = S3Deleter("url", "key", "secret", "auto")
    deleter.delete_object("bucket", "key")


def test_delete_object_failure():
    deleter = S3Deleter("url", "key", "secret", "auto")
    with pytest.raises(S3ActionError):
        deleter.delete_object("bucket", "fail-key")
