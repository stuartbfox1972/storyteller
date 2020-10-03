from flask import Response

import boto3
import botocore.session
import json

from aws_xray_sdk.core import patch_all

patch_all()

def _list_stories():
    return '{"Message": "All good"}'
