import boto3
import configparser
import psycopg2
import pathlib
import sys

script_path = pathlib.Path(__file__).parent.resolve()

parser = configparser.ConfigParser()
parser.read(f"{script_path}/pipeline.conf")

USERNAME = parser.get("redshift_config", "username")
PASSWORD = parser.get("redshift_config", "password")
HOST = parser.get("redshift_config", "host")
PORT = parser.get("redshift_config", "port")
PASSWORD = parser.get("redshift_config", "password")
IAM_ROLE = parser.get("redshift_config", "iam_role")
DATABASE = parser.get("redshift_config", "database")
ACCOUNT_ID = parser.get("boto_config", "account_id")
BUCKET_NAME = parser.get("boto_config", "bucket_name")

date = sys.argv[1]
date = date[:10]

rs_conn = psycopg2.connect(dbname = DATABASE, user = USERNAME, password = PASSWORD, host = HOST, port = PORT)

file_path = f"s3://{BUCKET_NAME}/{date}.csv"
role_string = f'arn:aws:iam::{ACCOUNT_ID}:role/{IAM_ROLE}'

sql_create_table = """CREATE TABLE IF NOT EXISTS public.Reddit (
                            ID varchar,
                            Title varchar(65535),
                            Text varchar(65535),
                            Score int,
                            Comments varchar(65535),
                            URL varchar(65535),
                            Comment varchar(65535),
                            Date date
                        );"""

sql_copy = f"COPY public.Reddit FROM 's3://my-test-bucket-aaron/2022-03-17.csv' iam_role '{role_string}' IGNOREHEADER 1 DELIMITER ',' CSV"
cur = rs_conn.cursor()

cur.execute(sql_create_table)
cur.execute(sql_copy)
cur.close()
rs_conn.commit()
rs_conn.close()

#"select * from stl_load_errors errors"