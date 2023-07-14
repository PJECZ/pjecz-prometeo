"""
Google Cloud Storage

Functions to get and upload files from Google Cloud Storage.

"""
from google.cloud import storage
from google.cloud.exceptions import NotFound

from .exceptions import MyBucketNotFoundError, MyFileNotAllowedError, MyFileNotFoundError, MyUploadError

EXTENSIONS_MIME_TYPES = {
    "doc": "application/msword",
    "docx": "application/msword",
    "pdf": "application/pdf",
    "xls": "xapplication/vnd.ms-excel",
    "xlsx": "xapplication/vnd.ms-excel",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
}


def get_file_from_gcs(
    bucket_name: str,
    file_path_str: str,
) -> bytes:
    """
    Get file from Google Cloud Storage

    :param bucket_name: Name of the bucket
    :param file_path_str: Path to the file
    :return: File content
    """

    # Get bucket
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except NotFound:
        raise MyBucketNotFoundError("Bucket not found")

    # Get file
    blob = bucket.get_blob(file_path_str)
    if blob is None:
        raise MyFileNotFoundError("File not found")

    # Return file content
    return blob.download_as_string()


def upload_file_to_gcs(
    bucket_name: str,
    file_path_str: str,
    content_type: str,
    data: bytes,
) -> str:
    """
    Upload file to Google Cloud Storage

    :param bucket_name: Name of the bucket
    :param file_path_str: Path to the file
    :param content_type: Content type of the file
    :param data: File content
    :return: File URL
    """

    # Check content type
    if content_type not in EXTENSIONS_MIME_TYPES.values():
        raise MyFileNotAllowedError("File not allowed")

    # Get bucket
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except NotFound:
        raise MyBucketNotFoundError("Bucket not found")

    # Create blob
    blob = bucket.blob(file_path_str)

    # Upload file
    try:
        blob.upload_from_string(data, content_type=content_type)
    except Exception as error:
        raise MyUploadError("Error uploading file") from error

    # Return file URL
    return blob.public_url
