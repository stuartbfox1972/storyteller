import boto3
import decimal
import json
import os

from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ['STORIES_TABLE'])

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, set):
            return list(o)
        return super(DecimalEncoder, self).default(o)

def story_handler(event, context):
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
  elif event['routeKey'] == "GET /api/v1.0/story/{id}":
    storyId = "STORY#" + event['pathParameters']['id']
    result = table.get_item(Key={'PK': storyId, 'SK': "DETAILS"},
                            ProjectionExpression="ageRange,author,opening,publishDate,storyId,tags,title,#v",
                            ExpressionAttributeNames={'#v': 'views'}
                           )
                           
    if 'Item' in result:
      return json.dumps(result['Item'], indent=4, cls=DecimalEncoder)
    else:
      message = prepResponse('{"message": "Unknown story"}', 404)
      return message

  elif event['routeKey'] == "GET /api/v1.0/story/{id}/{paragraph}":
    storyId = "STORY#" + event['pathParameters']['id']
    paragraphId = "PARAGRAPH#" + event['pathParameters']['paragraph']
    result = table.get_item(Key={'PK': storyId, 'SK': paragraphId},
                            ProjectionExpression="body,choices,paragraphId,storyId"
                           )
                           
    if 'Item' in result:
      return json.dumps(result['Item'], indent=4, cls=DecimalEncoder)
    else:
      message = prepResponse('{"message": "Unknown paragraph"}', 404)
      return message
  else:
      message = prepResponse('{"message":"Unsupported Operation"}', 405)
      return message
      
def prepResponse(body, status):
    message = {
        "isBase64Encoded": "false",
        "statusCode": status,
        "body": body
    }
    return message