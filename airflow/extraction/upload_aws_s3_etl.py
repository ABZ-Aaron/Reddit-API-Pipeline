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
parser.read(f"{script_path}/pipeline.conf")
ACCESS_KEY = parser.get("boto_config", "access_key")
SECRET_ACCESS_KEY = parser.get("boto_config", "secret_key")

# Define bucket name and where it should be stored location-wise
BUCKET_NAME = 'my-test-bucket-aaron'
LOCATION = 'eu-west-2'

# Used to determine what our extracted CSV file name is, and what our S3 file name should be
date = sys.argv[1]
date = date[:10]
os.chdir(script_path)
FILENAME = f"{date}.csv"
KEY = FILENAME

# Connect to S3
s3 = boto3.resource('s3', aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_ACCESS_KEY, region_name = LOCATION )

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
  s3.create_bucket(Bucket = BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})

# Upload our CSV file to S3 Bucket
s3.meta.client.upload_file(Filename = FILENAME, 
               Bucket = BUCKET_NAME, 
               Key = KEY)