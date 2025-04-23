import pytest
from actions.create import S3Creator
from utils.s3base import S3ActionError

class DummyS3Client:
    def create_bucket(self, Bucket, CreateBucketConfiguration=None):
        if Bucket == "fail-bucket":
            raise Exception("Simulated create_bucket failure")
        return {"ResponseMetadata": {"HTTPStatusCode": 200}}

@pytest.fixture(autouse=True)
def patch_boto3_client(monkeypatch):
    monkeypatch.setattr("boto3.client", lambda *a, **kw: DummyS3Client())

def test_create_bucket_success():
    creator = S3Creator("url", "key", "secret", "auto")
    creator.create_bucket("bucket")

def test_create_bucket_failure():
    creator = S3Creator("url", "key", "secret", "auto")
    with pytest.raises(S3ActionError):
        creator.create_bucket("fail-bucket")
