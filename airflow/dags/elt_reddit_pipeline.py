from os import remove
from airflow import DAG 
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta, datetime

# First of every month at midnight
schedule_interval = '@daily'
start_date = days_ago(1)

default_args = {
    "owner": "airflow",
    "start_date": start_date,
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id='elt_reddit_pipeline',
    description ='Loading Reddit API Data into Redshift',
    schedule_interval=schedule_interval,
    default_args=default_args,
    catchup=True,
    max_active_runs=1,
    tags=['Reddit'],
) as dag:

    extract_reddit_data_task = BashOperator(
        task_id = 'extract_reddit_data',
        bash_command = "python /opt/airflow/extraction/extract_reddit_etl.py '{{ execution_date }}'",
        dag = dag,
    )
    extract_reddit_data_task.doc_md = 'Extract past month Reddit data using PRAW and store as CSV'

    upload_to_s3 = BashOperator(
        task_id = 'upload_to_s3',
        bash_command = "python /opt/airflow/extraction/upload_aws_s3_etl.py '{{ execution_date }}'",
        dag = dag,
    )
    upload_to_s3.doc_md = 'Upload Reddit CSV data to S3 bucket'
    
    copy_to_redshift = BashOperator(
        task_id = 'copy_to_redshift',
        bash_command = "python /opt/airflow/extraction/upload_aws_redshift_etl.py '{{ execution_date }}'",
        dag = dag,
    )
    copy_to_redshift.doc_md = 'Copy S3 CSV file to Redshift table'

    remove_files = BashOperator(
        task_id = 'remove_files',
        bash_command = 'rm /opt/airflow/extraction/*.csv',
        dag = dag
    )
    remove_files.doc_md = 'Delete local CSV file or files stored in directory'

extract_reddit_data_task >> upload_to_s3 >> copy_to_redshift >> remove_files