import os
import pytest
from utils.progress import TqdmProgress

class DummyLogger:
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass
    def debug(self, msg): pass

def test_tqdm_progress_upload(monkeypatch, tmp_path):
    test_file = tmp_path / "file.txt"
    test_file.write_text("data" * 1024)  # 4KB
    progress = TqdmProgress(str(test_file), action="upload", logger=DummyLogger())
    progress(1024)
    progress.close()

def test_tqdm_progress_download(monkeypatch, tmp_path):
    test_file = tmp_path / "file.txt"
    total_size = 4096
    progress = TqdmProgress(str(test_file), action="download", total_size=total_size, logger=DummyLogger())
    progress(2048)
    progress(2048)
    progress.close()

def test_tqdm_progress_invalid_action(tmp_path):
    test_file = tmp_path / "file.txt"
    with pytest.raises(ValueError):
        TqdmProgress(str(test_file), action="invalid", logger=DummyLogger())

def test_tqdm_progress_download_missing_total_size(tmp_path):
    test_file = tmp_path / "file.txt"
    with pytest.raises(ValueError):
        TqdmProgress(str(test_file), action="download", logger=DummyLogger())
