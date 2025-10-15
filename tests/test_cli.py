import pytest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
import sys
import os
from typing import Dict, Any
from cli import app
from utils import Region, S3ActionError

# Add parent directory to path to import the cli module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


runner = CliRunner()

@pytest.fixture
def mock_env_vars():
    env_vars = {
        'ENDPOINT_URL': 'https://example.com',
        'AWS_ACCESS_KEY_ID': 'test_access_key',
        'AWS_SECRET_ACCESS_KEY': 'test_secret_key'
    }
    with patch.dict(os.environ, env_vars):
        yield env_vars

@pytest.fixture
def mock_get_s3_action():
    with patch('cli.get_s3_action') as mock:
        yield mock

class TestCliCommands:
    def test_list_buckets(self, mock_env_vars, mock_get_s3_action):
        mock_lister = MagicMock()
        mock_get_s3_action.return_value = mock_lister

        result = runner.invoke(app, ["list", "--buckets"])

        assert result.exit_code == 0
        mock_get_s3_action.assert_called_once_with(pytest.importorskip("actions").S3Lister, Region.AUTO)
        mock_lister.list_buckets.assert_called_once_with(False)

    def test_list_buckets_with_region(self, mock_env_vars, mock_get_s3_action):
        mock_lister = MagicMock()
        mock_get_s3_action.return_value = mock_lister

        result = runner.invoke(app, ["list", "--buckets", "--with-region"])

        assert result.exit_code == 0
        mock_lister.list_buckets.assert_called_once_with(True)

    def test_list_objects(self, mock_env_vars, mock_get_s3_action):
        mock_lister = MagicMock()
        mock_get_s3_action.return_value = mock_lister

        result = runner.invoke(app, ["list", "test-bucket"])

        assert result.exit_code == 0
        mock_lister.list_objects.assert_called_once_with("test-bucket")

    def test_list_objects_with_prefix(self, mock_env_vars, mock_get_s3_action):
        mock_lister = MagicMock()
        mock_get_s3_action.return_value = mock_lister

        result = runner.invoke(app, ["list", "test-bucket", "--prefix", "test/"])

        assert result.exit_code == 0
        mock_lister.list_objects_with_prefix.assert_called_once_with("test-bucket", "test/")

    def test_list_objects_with_prefix_no_bucket_fails(self, mock_env_vars, mock_get_s3_action): 
        result = runner.invoke(app, ["list", "--prefix", "test/"])

        assert result.exit_code == 1
        assert "Error: --prefix requires a bucket name." in result.stdout

    def test_list_multipart_uploads(self, mock_env_vars, mock_get_s3_action):
        mock_lister = MagicMock()
        mock_get_s3_action.return_value = mock_lister

        result = runner.invoke(app, ["list", "test-bucket", "--multipart"])

        assert result.exit_code == 0
        mock_lister.list_multipart_uploads.assert_called_once_with("test-bucket")

    def test_list_multipart_with_prefix_fails(self, mock_env_vars, mock_get_s3_action):
        result = runner.invoke(app, ["list", "test-bucket", "--multipart", "--prefix", "test/"])

        assert result.exit_code == 1
        assert "mutually exclusive" in result.stdout

    def test_list_multipart_no_bucket_fails(self, mock_env_vars, mock_get_s3_action):
        result = runner.invoke(app, ["list", "--multipart"])
        
        assert result.exit_code == 1
        assert "Error: --multipart requires a bucket name." in result.stdout

    def test_list_no_bucket_fails(self, mock_env_vars, mock_get_s3_action):
        result = runner.invoke(app, ["list"])
        
        assert result.exit_code == 1
        assert "Must provide a bucket name" in result.stdout

    def test_create_bucket(self, mock_env_vars, mock_get_s3_action):
        mock_creator = MagicMock()
        mock_get_s3_action.return_value = mock_creator
        
        result = runner.invoke(app, ["create", "test-bucket"])
        
        assert result.exit_code == 0
        mock_get_s3_action.assert_called_once_with(pytest.importorskip("actions").S3Creator, Region.AUTO)
        mock_creator.create_bucket.assert_called_once_with("test-bucket")

    def test_create_bucket_with_s3actionerror(self, mock_env_vars, mock_get_s3_action):
        mock_creator = MagicMock()
        mock_creator.create_bucket.side_effect = S3ActionError("Test error")
        mock_get_s3_action.return_value = mock_creator
        
        result = runner.invoke(app, ["create", "test-bucket"])
        
        assert result.exit_code == 1
        assert "Create error: Test error" in result.stdout
        mock_get_s3_action.assert_called_once_with(pytest.importorskip("actions").S3Creator, Region.AUTO)

    def test_create_bucket_with_exception(self, mock_env_vars, mock_get_s3_action):
        mock_creator = MagicMock()
        mock_creator.create_bucket.side_effect = Exception("Test exception")
        mock_get_s3_action.return_value = mock_creator
        
        result = runner.invoke(app, ["create", "test-bucket"])
        
        assert result.exit_code == 1
        assert "Error creating bucket: Test exception" in result.stdout
        mock_get_s3_action.assert_called_once_with(pytest.importorskip("actions").S3Creator, Region.AUTO)

    def test_upload_file(self, mock_env_vars, mock_get_s3_action):
        mock_uploader = MagicMock()
        mock_get_s3_action.return_value = mock_uploader
        
        result = runner.invoke(app, ["upload", "test-bucket", "test-file.txt", "test-key"])
        
        assert result.exit_code == 0
        mock_get_s3_action.assert_called_once_with(pytest.importorskip("actions").S3Uploader, Region.AUTO)
        mock_uploader.upload_file.assert_called_once_with("test-file.txt", "test-bucket", "test-key")

    def test_upload_file_no_object_key(self, mock_env_vars, mock_get_s3_action):
        mock_uploader = MagicMock()
        mock_get_s3_action.return_value = mock_uploader
        
        result = runner.invoke(app, ["upload", "test-bucket", "test-file.txt"])
        
        assert result.exit_code == 0
        mock_get_s3_action.assert_called_once_with(pytest.importorskip("actions").S3Uploader, Region.AUTO)
        mock_uploader.upload_file.assert_called_once_with("test-file.txt", "test-bucket", None)
    
    def test_upload_file_with_s3actionerror(self, mock_env_vars, mock_get_s3_action):
        mock_uploader = MagicMock()
        mock_uploader.upload_file.side_effect = S3ActionError("Test error")
        mock_get_s3_action.return_value = mock_uploader
        
        result = runner.invoke(app, ["upload", "test-bucket", "test-file.txt", "test-key"])
        
        assert result.exit_code == 1
        assert "Upload error: Test error" in result.stdout
        mock_get_s3_action.assert_called_once_with(pytest.importorskip("actions").S3Uploader, Region.AUTO)

    def test_upload_file_with_exception(self, mock_env_vars, mock_get_s3_action):
        mock_uploader = MagicMock()
        mock_uploader.upload_file.side_effect = Exception("Test exception")
        mock_get_s3_action.return_value = mock_uploader
        
        result = runner.invoke(app, ["upload", "test-bucket", "test-file.txt", "test-key"])
        
        assert result.exit_code == 1
        assert "Error uploading: Test exception" in result.stdout
        mock_get_s3_action.assert_called_once_with(pytest.importorskip("actions").S3Uploader, Region.AUTO)

    def test_download_file(self, mock_env_vars, mock_get_s3_action):
        mock_downloader = MagicMock()
        mock_get_s3_action.return_value = mock_downloader
        
        result = runner.invoke(app, ["download", "test-bucket", "test-key", "test-file.txt"])
        
        assert result.exit_code == 0
        mock_get_s3_action.assert_called_once_with(pytest.importorskip("actions").S3Downloader, Region.AUTO)
        mock_downloader.download_file.assert_called_once_with("test-bucket", "test-key", "test-file.txt")

    def test_download_file_no_object_key(self, mock_env_vars, mock_get_s3_action):
        mock_downloader = MagicMock()
        mock_get_s3_action.return_value = mock_downloader
        
        result = runner.invoke(app, ["download", "test-bucket", "test-key"])
        
        assert result.exit_code == 0
        mock_get_s3_action.assert_called_once_with(pytest.importorskip("actions").S3Downloader, Region.AUTO)
        mock_downloader.download_file.assert_called_once_with("test-bucket", "test-key", None)

    def test_download_file_with_s3actionerror(self, mock_env_vars, mock_get_s3_action):
        mock_downloader = MagicMock()
        mock_downloader.download_file.side_effect = S3ActionError("Test error")
        mock_get_s3_action.return_value = mock_downloader
        
        result = runner.invoke(app, ["download", "test-bucket", "test-key", "test-file.txt"])
        
        assert result.exit_code == 1
        assert "Download error: Test error" in result.stdout
        mock_get_s3_action.assert_called_once_with(pytest.importorskip("actions").S3Downloader, Region.AUTO)

    def test_download_file_with_exception(self, mock_env_vars, mock_get_s3_action):
        mock_downloader = MagicMock()
        mock_downloader.download_file.side_effect = Exception("Test exception")
        mock_get_s3_action.return_value = mock_downloader
        
        result = runner.invoke(app, ["download", "test-bucket", "test-key", "test-file.txt"])
        
        assert result.exit_code == 1
        assert "Error downloading: Test exception" in result.stdout
        mock_get_s3_action.assert_called_once_with(pytest.importorskip("actions").S3Downloader, Region.AUTO)

    def test_delete_object(self, mock_env_vars, mock_get_s3_action):
        mock_deleter = MagicMock()
        mock_get_s3_action.return_value = mock_deleter
        
        # Mock the confirm prompt to return True
        result = runner.invoke(app, ["delete", "test-bucket", "test-key"], input="y\n")
        
        assert result.exit_code == 0
        mock_deleter.delete_object.assert_called_once_with("test-bucket", "test-key")

    def test_delete_object_no_key(self, mock_env_vars, mock_get_s3_action):
        mock_deleter = MagicMock()
        mock_get_s3_action.return_value = mock_deleter
        
        # Mock the confirm prompt to return True
        result = runner.invoke(app, ["delete", "test-bucket"], input="y\n")
        
        assert result.exit_code == 0
        mock_deleter.delete_bucket.assert_called_once_with("test-bucket")

    def test_delete_object_no_key_cancelled(self, mock_env_vars, mock_get_s3_action):
        mock_deleter = MagicMock()
        mock_get_s3_action.return_value = mock_deleter
        
        # Mock the confirm prompt to return False
        result = runner.invoke(app, ["delete", "test-bucket"], input="n\n")
        
        assert result.exit_code == 0
        assert "Deletion cancelled" in result.stdout
        mock_deleter.delete_bucket.assert_not_called()
    
    def test_delete_object_no_key_with_s3actionerror(self, mock_env_vars, mock_get_s3_action):
        mock_deleter = MagicMock()
        mock_deleter.delete_bucket.side_effect = S3ActionError("Test error")
        mock_get_s3_action.return_value = mock_deleter
        
        # Mock the confirm prompt to return True
        result = runner.invoke(app, ["delete", "test-bucket"], input="y\n")
        
        assert result.exit_code == 1
        assert "Delete error: Test error" in result.stdout
        mock_deleter.delete_bucket.assert_called_once_with("test-bucket")

    def test_delete_bucket(self, mock_env_vars, mock_get_s3_action):
        mock_deleter = MagicMock()
        mock_get_s3_action.return_value = mock_deleter
        
        # Mock the confirm prompt to return True
        result = runner.invoke(app, ["delete", "test-bucket"], input="y\n")
        
        assert result.exit_code == 0
        mock_deleter.delete_bucket.assert_called_once_with("test-bucket")

    def test_detele_with_s3actionerror(self, mock_env_vars, mock_get_s3_action):
        mock_deleter = MagicMock()
        mock_deleter.delete_object.side_effect = S3ActionError("Test error")
        mock_get_s3_action.return_value = mock_deleter
        
        # Mock the confirm prompt to return True
        result = runner.invoke(app, ["delete", "test-bucket", "test-key"], input="y\n")
        
        assert result.exit_code == 1
        assert "Delete error: Test error" in result.stdout
        mock_deleter.delete_object.assert_called_once_with("test-bucket", "test-key")

    def test_delete_with_exception(self, mock_env_vars, mock_get_s3_action):
        mock_deleter = MagicMock()
        mock_deleter.delete_object.side_effect = Exception("Test exception")
        mock_get_s3_action.return_value = mock_deleter
        
        # Mock the confirm prompt to return True
        result = runner.invoke(app, ["delete", "test-bucket", "test-key"], input="y\n")
        
        assert result.exit_code == 1
        assert "Error deleting: Test exception" in result.stdout
        mock_deleter.delete_object.assert_called_once_with("test-bucket", "test-key")

    def test_abort_multipart(self, mock_env_vars, mock_get_s3_action):
        mock_aborter = MagicMock()
        mock_get_s3_action.return_value = mock_aborter

        # Mock the confirm prompt to return True
        result = runner.invoke(app, ["abort", "test-bucket", "test-key", "upload-id"], input="y\n")

        assert result.exit_code == 0
        mock_aborter.abort_multipart_upload.assert_called_once_with("test-bucket", "test-key", "upload-id")

    def test_abort_multipart_no_confirm(self, mock_env_vars, mock_get_s3_action):
        mock_aborter = MagicMock()
        mock_get_s3_action.return_value = mock_aborter
        
        # Mock the confirm prompt to return False
        result = runner.invoke(app, ["abort", "test-bucket", "test-key", "upload-id"], input="n\n")
        
        assert result.exit_code == 0
        assert "Abortion cancelled" in result.stdout
        mock_aborter.abort_multipart_upload.assert_not_called()

    def test_abort_multipart_with_s3actionerror(self, mock_env_vars, mock_get_s3_action):
        mock_aborter = MagicMock()
        mock_aborter.abort_multipart_upload.side_effect = S3ActionError("Test error")
        mock_get_s3_action.return_value = mock_aborter
        
        # Mock the confirm prompt to return True
        result = runner.invoke(app, ["abort", "test-bucket", "test-key", "upload-id"], input="y\n")
        
        assert result.exit_code == 1
        assert "Abort error: Test error" in result.stdout
        mock_aborter.abort_multipart_upload.assert_called_once_with("test-bucket", "test-key", "upload-id")

    def test_abort_multipart_with_exception(self, mock_env_vars, mock_get_s3_action):
        mock_aborter = MagicMock()
        mock_aborter.abort_multipart_upload.side_effect = Exception("Test exception")
        mock_get_s3_action.return_value = mock_aborter
        
        # Mock the confirm prompt to return True
        result = runner.invoke(app, ["abort", "test-bucket", "test-key", "upload-id"], input="y\n")
        
        assert result.exit_code == 1
        assert "Error aborting multipart upload: Test exception" in result.stdout
        mock_aborter.abort_multipart_upload.assert_called_once_with("test-bucket", "test-key", "upload-id")


    def test_delete_object_cancelled(self, mock_env_vars, mock_get_s3_action):
        mock_deleter = MagicMock()
        mock_get_s3_action.return_value = mock_deleter
        
        # Mock the confirm prompt to return False
        result = runner.invoke(app, ["delete", "test-bucket", "test-key"], input="n\n")
        
        assert result.exit_code == 0
        assert "Deletion cancelled" in result.stdout
        mock_deleter.delete_object.assert_not_called()

    def test_error_handling(self, mock_env_vars, mock_get_s3_action):
        mock_lister = MagicMock()
        mock_lister.list_objects.side_effect = S3ActionError("Test error")
        mock_get_s3_action.return_value = mock_lister
        
        result = runner.invoke(app, ["list", "test-bucket"])
        
        assert result.exit_code == 1
        assert "List error: Test error" in result.stdout
