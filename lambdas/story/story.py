import boto3
import decimal
import json
import os

from boto3.dynamodb.conditions import Key, Attr

def story_handler(event, context):
  if event["routeKey"] == "/api/v1.0/story":
    dynamodb = boto3.resource("dynamodb", region_name=os["AWS_REGION"])
    table = dynamodb.Table(os['STORIES_TABLE'])
    response = table.scan(
      IndexName="ListOfStories"
    )

    return json.dumps(response['Items'])

  else:
      return json.dumps('{"Error":"Unsupported Operation"}')
