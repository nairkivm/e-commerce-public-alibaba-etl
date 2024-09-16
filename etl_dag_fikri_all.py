from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
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
    'bq_to_bq_pipeline_fikri',
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
pipelines = {
    "Dim_Customer" : BigQueryToBigQueryPipeline(
        source_table='shop_dataset.customers',
        dest_table='shop_dwh.Dim_Customer',
        credentials_src='/home/tsabitghazian/airflow_demo/dags/ourplayground/etl-workshop/etl_fikri/bq-etl-task.json',
        credentials_dest='/home/tsabitghazian/airflow_demo/dags/ourplayground/etl-workshop/etl_fikri/bq-etl-task-dest.json'
    ),
    "Dim_Employee" : BigQueryToBigQueryPipeline(
        source_table='shop_dataset.employees',
        dest_table='shop_dwh.Dim_Employee',
        credentials_src='/home/tsabitghazian/airflow_demo/dags/ourplayground/etl-workshop/etl_fikri/bq-etl-task.json',
        credentials_dest='/home/tsabitghazian/airflow_demo/dags/ourplayground/etl-workshop/etl_fikri/bq-etl-task-dest.json'
    ),
    # "Dim_Office" : BigQueryToBigQueryPipeline(
    #     source_table='shop_dataset.offices',
    #     dest_table='shop_dwh.Dim_Office',
    #     credentials_src='/home/tsabitghazian/airflow_demo/dags/ourplayground/etl-workshop/etl_fikri/bq-etl-task.json',
    #     credentials_dest='/home/tsabitghazian/airflow_demo/dags/ourplayground/etl-workshop/etl_fikri/bq-etl-task-dest.json'
    # ),
    # "Dim_Product" : BigQueryToBigQueryPipeline(
    #     source_table='shop_dataset.products',
    #     dest_table='shop_dwh.Dim_Product',
    #     credentials_src='/home/tsabitghazian/airflow_demo/dags/ourplayground/etl-workshop/etl_fikri/bq-etl-task.json',
    #     credentials_dest='/home/tsabitghazian/airflow_demo/dags/ourplayground/etl-workshop/etl_fikri/bq-etl-task-dest.json'
    # ),
    # "Fact_Sales" : BigQueryToBigQueryPipeline(
    #     source_table='shop_dataset.orderdetails',
    #     dest_table='shop_dwh.Fact_Sales',
    #     credentials_src='/home/tsabitghazian/airflow_demo/dags/ourplayground/etl-workshop/etl_fikri/bq-etl-task.json',
    #     credentials_dest='/home/tsabitghazian/airflow_demo/dags/ourplayground/etl-workshop/etl_fikri/bq-etl-task-dest.json'
    # )
}

with dag:
    # Define the extract task
    @task
    def extract_task(pipeline_name, **kwargs):
        logging.info(f"Extracting the data from {pipelines[pipeline_name].source_table}")
        df = pipelines[pipeline_name].extract()
        kwargs['ti'].xcom_push(key=f'extracted_data_{pipeline_name}', value=df)

    # Define the transform task
    @task
    def transform_task(pipeline_name, **kwargs):
        extracted_data = kwargs['ti'].xcom_pull(key=f'extracted_data_{pipeline_name}')
        df = pd.DataFrame.from_dict(extracted_data[0])
        logging.info("Transforming")
        transformed_df = pipelines[pipeline_name].transform(df)
        kwargs['ti'].xcom_push(key=f'transformed_data_{pipeline_name}', value=transformed_df)

    # Define the load task
    @task
    def load_task(pipeline_name, **kwargs):
        transformed_data = kwargs['ti'].xcom_pull(key=f'transformed_data_{pipeline_name}')
        transformed_df = pd.DataFrame.from_dict(transformed_data[0])
        logging.info(f"Load data to {pipelines[pipeline_name].dest_table}")
        pipelines[pipeline_name].load(transformed_df)
    
    # Define dynamic task mapping
    extracts = extract_task.expand(pipeline_name=list(pipelines.keys()))
    transforms = transform_task.expand(pipeline_name=list(pipelines.keys()))
    loads = load_task.expand(pipeline_name=list(pipelines.keys()))

    # Set the task dependencies
    extracts >> transforms >> loads