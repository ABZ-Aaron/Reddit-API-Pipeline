from os import remove
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta, datetime

"""
DAG to extract Reddit data, load into AWS S3, and copy to AWS Redshift
"""

# Output name of extracted file. This be passed to each
# DAG task so they know which file to process
output_name = datetime.now().strftime("%Y%m%d")

# Run our DAG daily and ensures DAG run will kick off
# once Airflow is started, as it will try to "catch up"
schedule_interval = "@daily"
start_date = days_ago(1)

default_args = {"owner": "airflow", "depends_on_past": False, "retries": 1}

with DAG(
    dag_id="elt_reddit_pipeline",
    description="Reddit ELT",
    schedule_interval=schedule_interval,
    default_args=default_args,
    start_date=start_date,
    catchup=True,
    max_active_runs=1,
    tags=["RedditETL"],
) as dag:

    extract_reddit_data = BashOperator(
        task_id="extract_reddit_data",
        bash_command=f"python /opt/airflow/extraction/extract_reddit_etl.py {output_name}",
        dag=dag,
    )
    extract_reddit_data.doc_md = "Extract Reddit data and store as CSV"

    upload_to_s3 = BashOperator(
        task_id="upload_to_s3",
        bash_command=f"python /opt/airflow/extraction/upload_aws_s3_etl.py {output_name}",
        dag=dag,
    )
    upload_to_s3.doc_md = "Upload Reddit CSV data to S3 bucket"

    copy_to_redshift = BashOperator(
        task_id="copy_to_redshift",
        bash_command=f"python /opt/airflow/extraction/upload_aws_redshift_etl.py {output_name}",
        dag=dag,
    )
    copy_to_redshift.doc_md = "Copy S3 CSV file to Redshift table"

extract_reddit_data >> upload_to_s3 >> copy_to_redshift
