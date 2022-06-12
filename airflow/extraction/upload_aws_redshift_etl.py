import configparser
import pathlib
import psycopg2
import sys

# Full path to script
script_path = pathlib.Path(__file__).parent.resolve()

# Parse our configuration file
parser = configparser.ConfigParser()
parser.read(f"{script_path}/pipeline_conf.conf")

# Store our configuration variables
USERNAME = parser.get("aws_config", "redshift_username")
PASSWORD = parser.get("aws_config", "redshift_password")
HOST = parser.get("aws_config", "redshift_hostname")
PORT = parser.get("aws_config", "redshift_port")
REDSHIFT_ROLE = parser.get("aws_config", "redshift_role")
DATABASE = parser.get("aws_config", "redshift_database")
BUCKET_NAME = parser.get("aws_config", "bucket_name")
ACCOUNT_ID = parser.get("aws_config", "account_id")

# Connect to our Redshift database
rs_conn = psycopg2.connect(dbname = DATABASE, user = USERNAME, password = PASSWORD, host = HOST, port = PORT)

# Used to determine the S3 file we need
output_name = sys.argv[1]

# Our S3 bucket and file
file_path = f"s3://{BUCKET_NAME}/{output_name}.csv"

# Our IAM role
role_string = f'arn:aws:iam::{ACCOUNT_ID}:role/{REDSHIFT_ROLE}'

print(role_string)

# Create Redshift table if it doesn't exist
sql_create_table = """CREATE TABLE IF NOT EXISTS public.reddit (
                            ID varchar PRIMARY KEY,
                            Title varchar(max),
                            Text varchar(max),
                            Score int,
                            Comments varchar(max),
                            URL varchar(max),
                            Comment varchar(max),
                            DatePosted timestamp
                        );"""

# 1. Loading our data into a temporary table. 
# 2. Delete data from main table where ID is the same
# 3. Insert all data from temp table into main table
#
# Purpose of this is that if a new day's reddit file contains the same post (same ID), we'll update our table 
# with that one, as some columns such as Score may be different
create_temp_table = "CREATE TEMP table reddit_stage (LIKE public.reddit);"
sql_copy_to_temp = f"COPY reddit_stage FROM '{file_path}' iam_role '{role_string}' IGNOREHEADER 1 DELIMITER ',' CSV;"
delete_from_table = "DELETE FROM public.reddit USING reddit_stage WHERE public.reddit.ID = reddit_stage.ID;"
insert_into_table = "INSERT INTO public.reddit SELECT * FROM reddit_stage;"
drop_temp_table = "DROP TABLE reddit_stage;"

cur = rs_conn.cursor()
cur.execute(sql_create_table)
cur.execute(create_temp_table)
cur.execute(sql_copy_to_temp)
cur.execute(delete_from_table)
cur.execute(insert_into_table)
cur.execute(drop_temp_table)
cur.close()
rs_conn.commit()
rs_conn.close()
