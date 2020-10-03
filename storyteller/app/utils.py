from flask import request
from datetime import datetime

import boto3
import json
import jwt
import os
import pytz
import requests


def _get_secret():
    if os.environ['SECRETS_MANAGER_PATH']:
        secret_path = os.environ["SECRETS_MANAGER_PATH"]
        region_name = os.environ["AWS_DEFAULT_REGION"]

        # Create a Secrets Manager client
        sm_session = boto3.session.Session()
        sm_client = sm_session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = sm_client.get_secret_value(
                SecretId=secret_path
            )
        except ClientError as e:
            raise e
        else:
            secret = json.loads(get_secret_value_response['SecretString'])
            return (secret)

def _decode_token():

    secrets=_get_secret()

    jwt_header = request.headers.get('X-Amzn-Oidc-Data')
    if jwt_header is None:
        jwt_header = "eyJ0eXAiOiJKV1QiLCJraWQiOiI2OWVmNGNhZS0wYWJmLTRjNTItYWIyNS03NGI2NDA3MGJlMGUiLCJhbGciOiJFUzI1NiIsImlzcyI6Imh0dHBzOi8vY29nbml0by1pZHAuZXUtY2VudHJhbC0xLmFtYXpvbmF3cy5jb20vZXUtY2VudHJhbC0xXzFLaWxSckN0ViIsImNsaWVudCI6InIzdmwxcXE5ZHFuNXJqYTNjdTBvZTZzZ2UiLCJzaWduZXIiOiJhcm46YXdzOmVsYXN0aWNsb2FkYmFsYW5jaW5nOmV1LWNlbnRyYWwtMTo2ODk2ODAwODQwMzU6bG9hZGJhbGFuY2VyL2FwcC9jb2duaS1GYXJnYS0xMkZMQUEwVkRHQ1dXLzgzZDQxNTBkNmFmM2RiOTYiLCJleHAiOjE1ODM1ODY3ODB9.eyJzdWIiOiIzZjFmODc4My04ZTI3LTQ3M2QtODUyZS05MGM5NGM0ZjI3MGIiLCJ1c2VybmFtZSI6Im1ib3JnbWVpZXJAdGVjcmFjZXIuZGUiLCJleHAiOjE1ODM1ODY3ODAsImlzcyI6Imh0dHBzOi8vY29nbml0by1pZHAuZXUtY2VudHJhbC0xLmFtYXpvbmF3cy5jb20vZXUtY2VudHJhbC0xXzFLaWxSckN0ViJ9.nXCE9-LtOfxeRGYia4THH8U4xhKv15Sr3H-lzCLAnJ9p8kJ3kkZie6gfd-Yen3SzonB45Ycu0uSrS5X7JUyo2A"

    #TODO: In production you WANT to verify the signature!
    jwt_decoded = jwt.decode(jwt_header, verify=True)

    variables = {
        "username": jwt_decoded["username"],
        "valid_until_utc": datetime.fromtimestamp(jwt_decoded["exp"],tz=pytz.UTC).isoformat(),
        "jwt_decoded": json.dumps(jwt_decoded, indent=4),
    }
    return variables