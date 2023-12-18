import json
from datetime import datetime

def handler(event, context):
  print("Function called!!!")
  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  return {
      'statusCode': 200,
      'body': json.dumps('Hello World! Current time: ' + current_time)
  }
