import boto3
import json
import pyjwt
import os

def _get_secret():
    if os.environ['SECRETS_MANAGER_PATH']:
        return