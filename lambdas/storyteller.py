import boto3
import decimal
import json

from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
  if event['resource'] == '/story':
    table = dynamodb.Table('ag-stories')
    response = table.scan()
    for i in response['Items']:
      print(json.dumps(i))

if __name__ == "__main__":
  with open('request.test') as f:
    data = json.load(f)
  context = '{}'
  lambda_handler(data, context)
