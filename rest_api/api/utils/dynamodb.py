import os

import boto3


def get_dynamodb_client():
    endpoint_url = os.getenv("DYNAMODB_ENTRYPOINT")
    client = boto3.client("dynamodb", endpoint_url=endpoint_url)
    return client
