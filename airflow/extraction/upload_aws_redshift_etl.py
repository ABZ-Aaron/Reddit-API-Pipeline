import configparser

import pathlib

import psycopg2

import sys

# Full path to script
script_path = pathlib.Path(__file__).parent.resolve()

# Parse our configuration file
parser = configparser.ConfigParser()
parser.read(f"{script_path}/pipeline.conf")

# Store our configuration variables
USERNAME = parser.get("redshift_config", "username")
PASSWORD = parser.get("redshift_config", "password")
HOST = parser.get("redshift_config", "host")
PORT = parser.get("redshift_config", "port")
PASSWORD = parser.get("redshift_config", "password")
IAM_ROLE = parser.get("redshift_config", "iam_role")
DATABASE = parser.get("redshift_config", "database")
ACCOUNT_ID = parser.get("boto_config", "account_id")
BUCKET_NAME = parser.get("boto_config", "bucket_name")

# Connect to our Redshift database
rs_conn = psycopg2.connect(dbname = DATABASE, user = USERNAME, password = PASSWORD, host = HOST, port = PORT)

# Used to determine the S3 file we need
date = sys.argv[1]
date = date[:10]

# Our S3 bucket and file
file_path = f"s3://{BUCKET_NAME}/{date}.csv"

# Our IAM role
role_string = f'arn:aws:iam::{ACCOUNT_ID}:role/{IAM_ROLE}'

# Create Redshift table if it doesn't exist
sql_create_table = """CREATE TABLE IF NOT EXISTS public.Reddit (
                            ID varchar,
                            Title varchar(max),
                            Text varchar(max),
                            Score int,
                            Comments varchar(max),
                            URL varchar(max),
                            Comment varchar(max),
                            DateExecuted date,
                            DatePosted timestamp
                        );"""

# Copy S3 file to Redshift table
sql_copy = f"COPY public.Reddit FROM '{file_path}' iam_role '{role_string}' IGNOREHEADER 1 DELIMITER ',' CSV"
cur = rs_conn.cursor()

cur.execute(sql_create_table)
cur.execute(sql_copy)
cur.close()
rs_conn.commit()
rs_conn.close()
