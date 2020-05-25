import json
import sys

from storyteller import lambda_handler

data = json.load(sys.stdin)
context = '{}'
lambda_handler(data, context)
