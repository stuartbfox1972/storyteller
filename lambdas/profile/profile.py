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
  username = event['requestContext']['authorizer']['jwt']['claims']['username']

  if event['routeKey'] == "GET /api/v1.0/profile":
    result = table.get_item(Key={'PK': 'USER#' + sub,
                                   'SK': "PROFILE"})
    if 'Item' in result:
      userdata = result['Item']
      return json.dumps(userdata)

    table.put_item(Item={'PK': "USER#" + sub,
                         'SK': "PROFILE",
                         'username': username})

    return '{"status":"new_profile_created"}'

  if event['routeKey'] == "POST /api/v1.0/profile":
    profiledata = json.loads(event['body'])
    profiledata.update({'PK': 'USER#' + sub,
                        'SK': "PROFILE"})
    table.put_item(Item=profiledata)
    return '{"status":"profile_updated"}'
