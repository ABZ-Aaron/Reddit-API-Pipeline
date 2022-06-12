import boto3
import botocore
import configparser
import os
import pathlib
import sys

# Full path to our script
script_path = pathlib.Path(__file__).parent.resolve()

# Load AWS credentials
parser = configparser.ConfigParser()
parser.read(f"{script_path}/pipeline_conf.conf")
BUCKET_NAME = parser.get("aws_config", "bucket_name")
AWS_REGION = parser.get("aws_config", "aws_region")

# Used to determine what our extracted CSV file name is, and what our S3 file name should be
output_name = sys.argv[1]
FILENAME = f"{output_name}.csv"
KEY = FILENAME

# Connect to S3
s3 = boto3.resource('s3')

# Determine if our S3 bucket exists
exists = True
try:
    s3.meta.client.head_bucket(Bucket = BUCKET_NAME)
except botocore.exceptions.ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == '404':
        exists = False

# If bucket does not exist, create it 
if not exists:
  s3.create_bucket(Bucket = BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': AWS_REGION})

# Upload our CSV file to S3 Bucket
s3.meta.client.upload_file(Filename = '/tmp/' + FILENAME, 
               Bucket = BUCKET_NAME, 
               Key = KEY)