import boto3
from django.conf import settings


def get_s3_client():
    """
    Locally, connect to the MiniStack emulator using the endpoint/credentials
    supplied via environment variables. When deployed, AWS_S3_ENDPOINT_URL is
    unset so boto3 talks to real AWS using the instance/task IAM role.
    """
    if settings.AWS_S3_ENDPOINT_URL:
        return boto3.client(
            "s3",
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

    return boto3.client("s3")


def upload_file_to_s3(file, key):
    get_s3_client().upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, key)

    return key
