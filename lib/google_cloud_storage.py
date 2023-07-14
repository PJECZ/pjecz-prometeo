"""
Google Cloud Storage

Functions to get files from Google Cloud Storage.

"""
from google.cloud import storage

from .exceptions import MyFileNotFound


def get_file_from_gcs(
    bucket_name: str,
    file_name: str,
):
    """
    Get file from Google Cloud Storage

    :param bucket_name: Name of the bucket
    :param file_name: Name of the file
    :return: File content
    """

    # Get file from bucket
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(file_name)

    # Check if file exists
    if blob is None:
        raise MyFileNotFound("File not found")

    # Return file content
    return blob.download_as_string()
