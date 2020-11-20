""" Handle all story related function """
import decimal
import json
import os
import boto3

# from aws_xray_sdk.core import xray_recorder
# from aws_xray_sdk.core import patch_all
# patch_all()

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

class DecimalEncoder(json.JSONEncoder):
  """Some funky magic from StackOverflow"""
  def default(self, o):
    if isinstance(o, decimal.Decimal):
      return str(o)
    if isinstance(o, set):
      return list(o)
    return super(DecimalEncoder, self).default(o)

def _connect():
  """Connect to DynamoDB """
  dynamodb = boto3.resource("dynamodb")
  table = dynamodb.Table(os.environ['STORIES_TABLE'])
  return table

def story_handler(event, context):
  """Entry point """
  table = _connect()
  if event['routeKey'] == "GET /api/v1.0/story":
    results=[]
    response = table.scan(
        ProjectionExpression="author,ageRange,storyId,tags,title,#v",
        ExpressionAttributeNames={'#v': 'views'},
        IndexName="ListOfStories"
        )

    for i in response['Items']:
      results.append(i)

    return json.dumps(results, indent=4, cls=DecimalEncoder)

  if event['routeKey'] == "GET /api/v1.0/story/{storyId}":
    story_id = "STORY#" + event['pathParameters']['storyId']
    result = table.get_item(Key={'PK': story_id, 'SK': "DETAILS"},
                            ProjectionExpression="ageRange, \
                                                  author, \
                                                  opening, \
                                                  publishDate, \
                                                  storyId, \
                                                  tags, \
                                                  title, \
                                                  #v",
                            ExpressionAttributeNames={'#v': 'views'}
                           )

    if 'Item' in result:
      return json.dumps(result['Item'], indent=4, cls=DecimalEncoder)

    message = prep_response('{"message": "Unknown story"}', 404)
    return message

  if event['routeKey'] == "GET /api/v1.0/story/{storyId}/{paragraphId}":
    story_id = "STORY#" + event['pathParameters']['storyId']
    paragraph_id = "PARAGRAPH#" + event['pathParameters']['paragraphId']
    result = table.get_item(Key={'PK': story_id, 'SK': paragraph_id},
                            ProjectionExpression="body,choices,paragraphId,storyId"
                           )

    if 'Item' in result:
      return json.dumps(result['Item'], indent=4, cls=DecimalEncoder)

    message = prep_response('{"message": "Unknown paragraph"}', 404)
    return message

  message = prep_response('{"message":"Unsupported Operation"}', 405)
  return message

def prep_response(body, status):
  """Prepare a response """
  message = {
    "isBase64Encoded": "false",
    "statusCode": status,
    "body": body
  }
  return message
