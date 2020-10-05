from flask import request
from datetime import datetime

from aws_xray_sdk.core import patch_all

patch_all()

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


def get_cognito_public_keys():
    secrets=_get_secret()
    region = secrets["region"]
    pool_id = secrets["userpool_id"]
    url = f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json"

    resp = requests.get(url)
    return json.dumps(json.loads(resp.text)["keys"][1])


def _decode_token():
    jwt_header = request.headers.get('X-Amzn-Oidc-Data')
    
    #TODO: Fix this!! Grrr
    jwt_decoded = jwt.decode(jwt_header, verify=False)

    payload = json.dumps(jwt_decoded)
    return payload
