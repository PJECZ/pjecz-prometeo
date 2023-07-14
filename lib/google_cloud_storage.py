"""
Google Cloud Storage

Functions to get and upload files from Google Cloud Storage.

"""
from pathlib import Path
from urllib.parse import urlparse

from google.cloud import storage
from google.cloud.exceptions import NotFound

from .exceptions import (
    MyBucketNotFoundError,
    MyFileNotAllowedError,
    MyFileNotFoundError,
    MyNotValidParamError,
    MyUploadError,
)

EXTENSIONS_MEDIA_TYPES = {
    "doc": "application/msword",
    "docx": "application/msword",
    "pdf": "application/pdf",
    "xls": "xapplication/vnd.ms-excel",
    "xlsx": "xapplication/vnd.ms-excel",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
}


def get_media_type_from_filename(filename: str) -> str:
    """
    Get media type from filename

    :param filename: Name of file
    :return: Media type
    """

    # Get extension
    extension = Path(filename).suffix[1:].lower()

    # Get media type
    try:
        media_type = EXTENSIONS_MEDIA_TYPES[extension]
    except KeyError as error:
        raise MyFileNotAllowedError("File not allowed") from error

    # Return media type
    return media_type


def get_blob_name_from_url(url: str) -> str:
    """
    Get blob name from URL

    :param url: URL of the file
    :return: Blob name
    """

    # Parse URL
    parsed_url = urlparse(url)

    # Get blob name
    try:
        blob_name = parsed_url.path[1:]
    except IndexError as error:
        raise MyNotValidParamError("Not valid URL") from error

    # Return blob name
    return blob_name


def get_file_from_gcs(
    bucket_name: str,
    blob_name: str,
) -> bytes:
    """
    Get file from Google Cloud Storage

    :param bucket_name: Name of the bucket
    :param blob_name: Path to the file
    :return: File content
    """

    # Get bucket
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except NotFound:
        raise MyBucketNotFoundError("Bucket not found")

    # Get file
    blob = bucket.get_blob(blob_name)
    if blob is None:
        raise MyFileNotFoundError("File not found")

    # Return file content
    return blob.download_as_string()


def upload_file_to_gcs(
    bucket_name: str,
    blob_name: str,
    content_type: str,
    data: bytes,
) -> str:
    """
    Upload file to Google Cloud Storage

    :param bucket_name: Name of the bucket
    :param blob_name: Path to the file
    :param content_type: Content type of the file
    :param data: File content
    :return: Public URL
    """

    # Check content type
    if content_type not in EXTENSIONS_MEDIA_TYPES.values():
        raise MyFileNotAllowedError("File not allowed")

    # Get bucket
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except NotFound:
        raise MyBucketNotFoundError("Bucket not found")

    # Create blob
    blob = bucket.blob(blob_name)

    # Upload file
    try:
        blob.upload_from_string(data, content_type=content_type)
    except Exception as error:
        raise MyUploadError("Error uploading file") from error

    # Return public URL
    return blob.public_url
