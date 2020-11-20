""" Handle all profile related function """
import json
import os
import boto3

from datetime import datetime
# from aws_xray_sdk.core import xray_recorder
# from aws_xray_sdk.core import patch_all
# patch_all()

def _clean_results(result):
  data = result['Item']
  data.pop('PK')
  data.pop('SK')
  return data

def _connect():
  """ Connect to DynamoDB """
  dynamodb = boto3.resource("dynamodb")
  table = dynamodb.Table(os.environ['STORIES_TABLE'])
  return table

def _create_get(sub, username, table):
  result = table.get_item(Key={'PK': 'USER#' + sub,
                               'SK': "PROFILE"})

  if 'Item' not in result:
    table.put_item(Item={'PK': "USER#" + sub,
                         'SK': "PROFILE",
                         'username': username})
    return {"status": "profile_created"}

  return json.dumps(_clean_results(result))

def _update(sub, username, table, event):
  profiledata = json.loads(event['body'])
  profiledata.update({'PK': 'USER#' + sub,
                      'SK': "PROFILE",
                      'username': username})
  table.put_item(Item=profiledata)
  return '{"status":"profile_updated"}'

def _get_all_progress(sub, table):
  results = table.query(
    KeyConditionExpression='#pk = :pk AND begins_with ( #sk , :sk )',
    ExpressionAttributeNames ={
      '#pk': 'PK',
      '#sk': 'SK'
    },
    ExpressionAttributeValues={
      ':pk': 'USER#' + sub,
      ':sk': 'PROGRESS#'
    }
  )
  if 'Items' in results:
    return results['Items']

  return

def _get_story_progress(sub, table, story_id):
  result = table.get_item(Key={'PK': 'USER#' + sub,
                               'SK': "PROGRESS#" + story_id})

  if 'Item' not in result:
    return {"status": "no_progress_tracked"}

  message = _clean_results(result)
  return json.dumps(message)

def _update_story_progress(sub, table, event):
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  story_id = event['pathParameters']['storyId']
  progressdata = json.loads(event['body'])
  progressdata.update({'PK': 'USER#' + sub,
                       'SK': "PROGRESS#" + story_id,
                       'timestamp': dt_string})
  table.put_item(Item=progressdata)
  return '{"status":"progress_updated"}'

def profile_handler(event, context):
  """ Entry point """
  table = _connect()
  sub = event['requestContext']['authorizer']['jwt']['claims']['sub']
  username = event['requestContext']['authorizer']['jwt']['claims']['username']
  

  if event['routeKey'] == "GET /api/v1.0/profile":
    return _create_get(sub, username, table)

  if event['routeKey'] == "POST /api/v1.0/profile":
    return _update(sub, username, table, event)

  if event['routeKey'] == "GET /api/v1.0/profile/progress":
    return _get_all_progress(sub, table)

  if event['routeKey'] == "GET /api/v1.0/profile/progress/{storyId}":
    story_id = event['pathParameters']['storyId']
    return _get_story_progress(sub, table, story_id)

  if event['routeKey'] == "POST /api/v1.0/profile/progress/{storyId}":
    return _update_story_progress(sub, table, event)
