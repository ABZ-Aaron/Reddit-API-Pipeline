from airflow import DAG 
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    "owner": "airflow",
    "start_date": days_ago(2),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id='elt_reddit_pipeline',
    schedule_interval="@daily",
    default_args=default_args,
    catchup=True,
    max_active_runs=1,
    tags=['testing'],
) as dag:

    extract_reddit_data_task = BashOperator(
        task_id = 'extract_reddit_data',
        bash_command = "python /opt/airflow/extraction/extract_reddit_etl.py '{{ execution_date }}'",
        dag = dag,
    )

    upload_to_s3 = BashOperator(
        task_id = 'upload_to_s3',
        bash_command = "python /opt/airflow/extraction/upload_aws_s3_etl.py '{{ execution_date }}'",
        dag = dag,
    )
    
    copy_to_redshift = BashOperator(
        task_id = 'copy_to_redshift',
        bash_command = "python /opt/airflow/extraction/upload_aws_redshift_etl.py '{{ execution_date }}'",
        dag = dag,
    )

extract_reddit_data_task >> upload_to_s3 >> copy_to_redshift