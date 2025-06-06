import pytest
from actions.abort import S3Aborter
from utils.s3base import S3ActionError, S3Base

class DummyS3Client:
    def abort_multipart_upload(self, Bucket, Key, UploadId):
        if UploadId == "fail-upload-id":
            raise Exception("Simulated abort failure")
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

def test_abort_multipart_upload_success():
    aborter = S3Aborter("url", "key", "secret", "auto")
    aborter.abort_multipart_upload("bucket", "key", "upload-id")

def test_abort_multipart_upload_failure():
    aborter = S3Aborter("url", "key", "secret", "auto")
    with pytest.raises(S3ActionError):
        aborter.abort_multipart_upload("bucket", "key", "fail-upload-id")
