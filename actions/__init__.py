"""
Actions module for R2Py CLI.

This module defines the actions for the R2Py CLI tool.
"""

from .upload import S3Uploader
from .download import S3Downloader
from .abort import S3Aborter
from .delete import S3Deleter
from .list import S3Lister
from .create import S3Creator
