import boto3
import decimal
import json
import os

from boto3.dynamodb.conditions import Key, Attr

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, set):
            return list(o)
        return super(DecimalEncoder, self).default(o)

def story_handler(event, context):
  if event["routeKey"] == "GET /api/v1.0/story":
    table = dynamodb.Table(os.environ['STORIES_TABLE'])
    dynamodb = boto3.resource("dynamodb")
    results=[]
    response = table.scan(
        Limit=25,
        IndexName="ListOfStories"
        )

    for i in response['Items']:
        results.append(i)
    
    return json.dumps(results, indent=4, cls=DecimalEncoder)

  else:
      message = {"Error":"Unsupported Operation", "routeKey": event["routeKey"] }
      return json.dumps(message)
