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

def _lookup(sub, table):
  result = table.get_item(Key={'PK': 'USER#' + sub,
                               'SK': "PROFILE"})
  return result

def _update(sub, username, table, event):
  profiledata = json.loads(event['body'])
  profiledata.update({'PK': 'USER#' + sub,
                      'SK': "PROFILE",
                      'username': username})
  table.put_item(Item=profiledata)
  return '{"status":"profile_updated"}'

def _create_get(sub, username, table):
  result = _lookup(sub, table)

  if 'Item' not in result:
    table.put_item(Item={'PK': "USER#" + sub,
                         'SK': "PROFILE",
                         'username': username})
    return {"status": "profile_created"}
    
  userdata = result['Item']
  userdata.pop('PK')
  userdata.pop('SK')
  return json.dumps(userdata)

def profile_handler(event, context):
  """ Entry point """
  table = _connect()
  sub = event['requestContext']['authorizer']['jwt']['claims']['sub']
  username = event['requestContext']['authorizer']['jwt']['claims']['username']

  if event['routeKey'] == "GET /api/v1.0/profile":
    return _create_get(sub, username, table)

  if event['routeKey'] == "POST /api/v1.0/profile":
    return _update(sub, username, table, event)

