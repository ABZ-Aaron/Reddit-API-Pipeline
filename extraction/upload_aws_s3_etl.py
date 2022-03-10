import boto3
import json

PATH = "/Users/aaronwright/Documents/Tech/Projects/RedditApp"
BUCKET = 'redbucket-aaron'
KEY = '2022-3-8_WK31.csv'
FILENAME = '/extraction/output/2022-3-8_WK31.csv'

# Load in configuration data from our JSON file
with open(f'{PATH}/extraction/secrets/secret_aws_s3.json', 'r') as f:
  config_data = json.load(f)

# Save our JSON data
ACCESS_KEY = config_data['ACCESS_KEY']
SECRET_ACCESS_KEY = config_data['SECRET_ACCESS_KEY']

# Initialise client. Connect to S3
s3 = boto3.client('s3', 
                  region_name = 'eu-west-2', 
                  aws_access_key_id = ACCESS_KEY,
                  aws_secret_access_key = SECRET_ACCESS_KEY)

s3.upload_file(Filename = f'{PATH}/{FILENAME}', 
               Bucket = BUCKET, 
               Key = KEY)