from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from google.oauth2 import service_account
import pandas as pd
import logging
import sys
import os

sys.path.append('/home/tsabitghazian/airflow_demo/dags/ourplayground/etl-workshop/etl_fikri')

from etl_bigquery_to_bigquery_daily import BigQueryToBigQueryPipeline

# Set default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'bq_to_bq_pipeline_fikri_dim_office',
    default_args=default_args,
    description='A pipeline to extract data from BigQuery (source) and load it into BigQuery (destination)',
    schedule_interval='10 2 * * *',
    start_date=datetime(2024, 8, 20),
    catchup=False,
)

# Initialize and configure logging
logging.basicConfig(filename='ingestion.log',
                    filemode='a',
                    format='%(asctime)s - %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

# Initialize the pipeline 
pipeline = BigQueryToBigQueryPipeline(
    source_table='shop_dataset.offices',
    dest_table='shop_dwh.Dim_Office',
    credentials_src='/home/tsabitghazian/airflow_demo/dags/ourplayground/etl-workshop/etl_fikri/bq-etl-task.json',
    credentials_dest='/home/tsabitghazian/airflow_demo/dags/ourplayground/etl-workshop/etl_fikri/bq-etl-task-dest.json'
)

# Define the extract task
def extract_task(**kwargs):
    logging.info(f"Extracting the data from {pipeline.source_table}")
    df = pipeline.extract()
    kwargs['ti'].xcom_push(key='extracted_data', value=df)

# Define the transform task
def transform_task(**kwargs):
    extracted_data = kwargs['ti'].xcom_pull(key='extracted_data')
    df = pd.DataFrame.from_dict(extracted_data)
    logging.info("Transforming")
    transformed_df = pipeline.transform(df)
    kwargs['ti'].xcom_push(key='transformed_data', value=transformed_df)

# Define the load task
def load_task(**kwargs):
    transformed_data = kwargs['ti'].xcom_pull(key='transformed_data')
    transformed_df = pd.DataFrame.from_dict(transformed_data)
    logging.info(f"Load data to {pipeline.dest_table}")
    pipeline.load(transformed_df)

# Define Airflow tasks
extract = PythonOperator(
    task_id='extract',
    python_callable=extract_task,
    provide_context=True,
    dag=dag,
)

transform = PythonOperator(
    task_id='transform',
    python_callable=transform_task,
    provide_context=True,
    dag=dag,
)

load = PythonOperator(
    task_id='load',
    python_callable=load_task,
    provide_context=True,
    dag=dag,
)

# Set the task dependencies
extract >> transform >> load