import urllib
import boto3
import pandas as pd
import io

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('company-info-test')

def lambda_handler(event, context):
  bucket = event['Records'][0]['s3']['bucket']['name']
  # S3 event converts filename with space to "+". This function makes sure that key variable holds original file name.
  key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
  response = s3.get_object(Bucket=bucket, Key=key)
  file_content = response["Body"].read()
  data_read = io.BytesIO(file_content)
  df = pd.read_excel(data_read)
  for index, row in df.iterrows():
    item = {}
    item['Id'] = index
    item['Name'] = row['Name']
    item['Age'] = row['Age']
    item['Company'] = row['Company']
    item['project'] = row['Project']
    response = table.put_item(Item=item)

    def dummy_function(num):
      return num/num

    def test_dummy_function():
      result = dummy_function(10)
      assert result == 1