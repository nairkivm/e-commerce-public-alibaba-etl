
from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from google.oauth2 import service_account
import pandas as pd
import logging

import sys
import os
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '..'
        )
    )
)

from utils.etl_batch import CsvToBigQueryPipeline

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
    'fact_orders_dag',
    default_args=default_args,
    description='A pipeline to extract data from CSV (source) and load it into BigQuery (destination)',
    schedule_interval='30 6 * * *',
    start_date=datetime(2024,9,20),
    catchup=False,
)

# Initialize and configure logging
logging.basicConfig(
    filename=f'{os.path.dirname(__file__)}/../etl-logs/etl_batch.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initialize the pipeline
pipeline = CsvToBigQueryPipeline(
    dest_table='store.fact_orders',
    project_id=os.environ.get('GCP_PROJECT_ID'),
    credentials_dest=os.environ.get('CREDENTIAL_PATH')
)

# Define the start etl task
@task
def start_etl_task():
    logging.info('[ETL] STARTING...')
    starting_time = datetime.now()
    return starting_time

# Define the transform task
@task
def extract_task(pipeline):
    logging.info(f"Extracting the data from csv-s")
    source = pipeline.extract()
    return source

# Define the transform task
@task
def transform_task(pipeline, source):
    logging.info("Transforming")
    transformed_result = pipeline.transform(source)
    return transformed_result

# Define the load task
@task
def load_task(pipeline, transformed_result):
    logging.info(f"Load data to '{pipeline.dest_table}'")
    pipeline.load(transformed_result)

# Define the end etl task
@task
def end_etl_task(starting_time):
    ending_time = datetime.now()
    elapsed_duration = ending_time - starting_time
    logging.info(f'[ETL] DONE! ({elapsed_duration})')

# Define the dag    
with dag:
    start = start_etl_task()
    source = extract_task(pipeline)
    transformed_result = transform_task(pipeline, source)
    load = load_task(pipeline, transformed_result)
    end = end_etl_task(start)

    # Set the task dependencies
    start >> source >> transformed_result >> load >> end
