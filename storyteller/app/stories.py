from flask import Response

import boto3
import botocore.session
import json

def _list_stories():
    return '{"Message": "All good"}'