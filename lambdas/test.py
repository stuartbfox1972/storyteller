from pprint import pprint
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('story-teller-dev-data')

polly_client = boto3.Session().client('polly')

def lambda_handler(event, context):
    # Get a story's details
    response = table.get_item(Key={'PK': "STORY#0", 'SK': "DETAILS"})
    pprint(response['Item'])




response = polly_client.synthesize_speech(VoiceId='Joanna',
                OutputFormat='mp3', 
                Text = 'This is a sample text to be synthesized.')

file = open('speech.mp3', 'wb')
file.write(response['AudioStream'].read())
file.close()
