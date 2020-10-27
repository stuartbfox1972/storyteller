""" Handle all profile related function """
import logging
import json
import os
import boto3

from boto3.dynamodb.conditions import Key, Attr
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

def _connect():
  """Connect to DynamoDB """
  dynamodb = boto3.resource("dynamodb")
  table = dynamodb.Table(os.environ['STORIES_TABLE'])
  return table

def profile_handler(event, context):
  """Entry point """
  table = _connect()