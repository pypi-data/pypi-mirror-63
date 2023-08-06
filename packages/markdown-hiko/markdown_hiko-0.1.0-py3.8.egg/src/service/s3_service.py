import logging
import boto3
from botocore.exceptions import ClientError
import os


class S3Service:
    def __init__(self, bucket: str):
        # Check environment value
        if os.getenv("AWS_ACCESS_KEY_ID") is None:
            raise Exception("Please set AWS_SECRET_ACCESS_KEY")
        if os.getenv("AWS_SECRET_ACCESS_KEY") is None:
            raise Exception("Please set AWS_SECRET_ACCESS_KEY")
        if os.getenv("AWS_DEFAULT_REGION") is None:
            raise Exception("Please set AWS_DEFAULT_REGION")
        self.bucket = bucket

    def upload_file(self, file_name, object_name=None):
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, self.bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True
