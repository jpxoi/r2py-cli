"""
Progress Bar Utility for R2Py CLI Tool.

This module provides the TqdmProgress class, which integrates the tqdm library to display
a colored, real-time progress bar for file uploads and downloads to/from S3-compatible storage.
The progress bar automatically scales units and provides clear feedback to users during
long-running data transfers via the CLI. Use this for visual feedback in both uploads and downloads,
optionally emitting detailed logs about the transfer process.
"""

import os
from tqdm import tqdm
from .logger import Logger


class TqdmProgress:
    """Progress bar callback for S3 downloads or uploads."""

    def __init__(
        self, filename: str, action: str, total_size: int = None, logger: Logger = None
    ):
        """
        Initialize the progress bar for upload or download.
        Args:
            filename (str): File being transferred.
            action (str): 'upload' or 'download'.
            total_size (int, optional): Total size in bytes (required for download).
            logger (Logger, optional): Logger for progress messages.
        """
        self._filename = filename
        self._action = action
        self.logger = logger
        if action == "upload":
            self._size = (
                float(os.path.getsize(filename))
                if total_size is None
                else float(total_size)
            )
        elif action == "download":
            if total_size is None:
                raise ValueError("total_size must be provided for downloads")
            self._size = float(total_size)
        else:
            raise ValueError("action must be 'upload' or 'download'")
        self._tqdm = tqdm(
            total=self._size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=os.path.basename(filename),
            leave=True,
            dynamic_ncols=True,
            colour="green" if action == "upload" else "blue",
        )
        self._seen_so_far = 0
        if self.logger:
            if action == "upload":
                self.logger.info(
                    f"Starting upload for {self._filename} "
                    f"({self._size / (1024 * 1024):.2f} MB)"
                )
            else:
                self.logger.info(
                    f"Starting download for {self._filename} "
                    f"({self._size / (1024 * 1024):.2f} MB)"
                )
            self.logger.info(f"Progress bar initialized for {self._filename}")
            self.logger.info(f"File size: {self._size / (1024 * 1024):.2f} MB")

    def __call__(self, bytes_amount: int) -> None:
        """
        Update the progress bar with the number of bytes transferred.
        Args:
            bytes_amount (int): Number of bytes transferred since last update.
        """
        self._seen_so_far += bytes_amount
        self._tqdm.update(bytes_amount)
        if self.logger:
            action_str = "Uploaded" if self._action == "upload" else "Downloaded"
            mb_seen = self._seen_so_far / (1024 * 1024)
            self.logger.debug(f"{action_str} {mb_seen:.2f} MB of {self._filename}")

    def close(self) -> None:
        """
        Close the progress bar.
        """
        self._tqdm.close()
