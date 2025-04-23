import os
from tqdm import tqdm
from utils.logger import Logger

class TqdmProgress:
    """Progress bar callback for S3 downloads or uploads."""
    def __init__(self, filename: str, action: str, total_size: int = None, logger: Logger = None):
        self._filename = filename
        self._action = action
        self.logger = logger
        if action == "upload":
            self._size = float(os.path.getsize(filename)) if total_size is None else float(total_size)
        elif action == "download":
            if total_size is None:
                raise ValueError("total_size must be provided for downloads")
            self._size = float(total_size)
        else:
            raise ValueError("action must be 'upload' or 'download'")
        self._tqdm = tqdm(
            total=self._size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc=os.path.basename(filename),
            leave=True,
            dynamic_ncols=True,
            colour='green' if action == "upload" else 'blue',
        )
        self._seen_so_far = 0
        if self.logger:
            if action == "upload":
                self.logger.info(f"Starting upload for {self._filename} ({self._size / (1024 * 1024):.2f} MB)")
            else:
                self.logger.info(f"Starting download for {self._filename} ({self._size / (1024 * 1024):.2f} MB)")
            self.logger.info(f"Progress bar initialized for {self._filename}")
            self.logger.info(f"File size: {self._size / (1024 * 1024):.2f} MB")

    def __call__(self, bytes_amount: int) -> None:
        self._seen_so_far += bytes_amount
        self._tqdm.update(bytes_amount)
        if self.logger:
            self.logger.debug(f"{'Uploaded' if self._action == 'upload' else 'Downloaded'} {self._seen_so_far / (1024 * 1024):.2f} MB of {self._filename}")

    def close(self) -> None:
        self._tqdm.close()