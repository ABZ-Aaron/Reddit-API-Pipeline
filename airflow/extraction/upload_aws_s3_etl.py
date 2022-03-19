import boto3
import configparser
import botocore
import glob
import os
import pathlib
import sys

script_path = pathlib.Path(__file__).parent.resolve()

# Load AWS credentials
parser = configparser.ConfigParser()
parser.read(f"{script_path}/pipeline.conf")
ACCESS_KEY = parser.get("boto_config", "access_key")
SECRET_ACCESS_KEY = parser.get("boto_config", "secret_key")

date = sys.argv[1]
date = date[:10]

os.chdir(script_path)
FILENAME = f"{date}.csv"
#FILENAME = glob.glob('*.{}'.format('csv'))[0]
KEY = FILENAME

s3 = boto3.resource('s3',aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_ACCESS_KEY, region_name = 'eu-west-2' )

BUCKET_NAME = 'my-test-bucket-aaron'

exists = True
try:
    s3.meta.client.head_bucket(Bucket = BUCKET_NAME)
except botocore.exceptions.ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == '404':
        exists = False

if not exists:
  s3.create_bucket(Bucket = BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})

s3.meta.client.upload_file(Filename = FILENAME, 
               Bucket = BUCKET_NAME, 
               Key = KEY)