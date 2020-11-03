""" Handle all profile related function """
import logging
import json
import os
import boto3

from boto3.dynamodb.conditions import Key, Attr
#from aws_xray_sdk.core import xray_recorder
#from aws_xray_sdk.core import patch_all
#patch_all()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def _connect():
  """ Connect to DynamoDB """
  dynamodb = boto3.resource("dynamodb")
  table = dynamodb.Table(os.environ['STORIES_TABLE'])
  return table

def profile_handler(event, context):
  """ Entry point """
  table = _connect()
  sub = event['requestContext']['authorizer']['jwt']['claims']['sub']
  if event['routeKey'] == "GET /api/v1.0/profile":
    result = table.get_item(Key={'PK': 'USER#' + sub,
                                   'SK': "PROFILE"})
    if 'Item' in result:
      userdata = result['Item']
      return json.dumps(userdata)

    return '{"status":"user not found"}'
