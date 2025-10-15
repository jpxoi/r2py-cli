"""
Region Enum for the R2Py CLI Tool.

This module defines the Region enum, which is used to specify
the region for the S3-compatible storage.
"""

from enum import Enum

class Region(str, Enum):
    """Region enum for the R2Py CLI Tool."""
    WNAM = "wnam"
    ENAM = "enam"
    WEUR = "weur"
    EEUR = "eeur"
    APAC = "apac"
    AUTO = "auto"
