from flask import request

import base64
import boto3
import json
import jwt
import os
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

    # Step 1: Get the key id from JWT headers (the kid field)
    secrets=_get_secret()
    encoded_jwt = request.headers['X-Amzn-Oidc-Data']
    jwt_headers = encoded_jwt.split('.')[0]
    decoded_jwt_headers = base64.b64decode(jwt_headers)
    decoded_jwt_headers = decoded_jwt_headers.decode("utf-8")
    decoded_json = json.loads(decoded_jwt_headers)
    kid = decoded_json['kid']

    # Step 2: Get the public key from regional endpoint
    url = 'https://public-keys.auth.elb.' + secrets['region'] + '.amazonaws.com/' + kid
    req = requests.get(url)
    pub_key = req.text

    # Step 3: Get the payload
    payload = jwt.decode(encoded_jwt, pub_key, algorithms=['RS256'])
    return payload