from flask import request
from datetime import datetime

from aws_xray_sdk.core import patch_all

patch_all()

import boto3
import jwt
import os
import requests


def _get_secret():
    if os.environ['SECRETS_MANAGER_PATH']:
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
    jwt_header = request.headers.get('X-Amzn-Oidc-Data')
    
    # #TODO: Fix this!! Grrr
    jwt_decoded = jwt.decode(jwt_header, verify=False)

    return jwt_decoded