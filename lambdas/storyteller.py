import boto3
import decimal
import json

from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
  if event['resource'] == '/story':
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('ag-stories')
    response = table.scan()
    for i in response['Items']:
      print(json.dumps(i))
  elif event['resource'] == '/story/{id}':
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('ag-stories')
    print(event['pathParameters']['id'])
    response = table.get_item(Key={'storyid': event['pathParameters']['id']})
    print(json.dumps(response['Item']))
  else:
      return json.dumps('{"Error":"Unsupported Operation"}')
