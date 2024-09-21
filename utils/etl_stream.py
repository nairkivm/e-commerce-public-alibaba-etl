import pandas as pd
import logging
from kafka import KafkaConsumer
import json
from time import sleep
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google.cloud import bigquery

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

logging.basicConfig(
    filename=f'{os.path.dirname(__file__)}/../etl-logs/etl_stream.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

from utils.source_requirements import SourceRequirements
from utils.destination_requirements import DestinationRequirements
from utils.helper import Helper
from utils.pipeline_template import GenericPipelineInterface
from utils.transform import TableTransformation

class TopicsToBigQueryPipeline(GenericPipelineInterface):
    
    def __init__(self, dest_table: str, project_id: str, credentials_dest: str, bootstrap_server: str, topic_name: str, topic_group: str):
        self.dest_table = dest_table
        self.project_id = project_id
        self.credentials_dest = credentials_dest
        self.bootstrap_server = bootstrap_server
        self.topic_name = topic_name
        self.topic_group = topic_group


    def extract(self, message: dict) -> pd.DataFrame:
        print(f"{'EXTRACTS SOURCE DATA (Topics)':-^60}")
        return pd.DataFrame([message])

    def transform(self, source: pd.DataFrame) -> pd.DataFrame:
        print(f"""{f'TRANSFORMS INTO [{self.dest_table.split(".")[1]}]':-^60}""")
        df = source
        transformation = TableTransformation({DestinationRequirements().requirements[self.dest_table]['source_tables'][0]: df})
        if self.dest_table.endswith('fact_carts_has_products'):
            transformed_df = transformation.transformToFactCartsProducts()
        elif self.dest_table.endswith('fact_shoppingcarts'):
            transformed_df = transformation.transformToFactCarts() 
        elif self.dest_table.endswith('fact_products_sold_vendor'):
            transformed_df = transformation.transformToFactProductSoldVendor()   
        return transformed_df

    def load(self, transformed_result: pd.DataFrame):
        print(f"{f'LOAD INTO [{self.dest_table}]':-^60}")
        credentials = service_account.Credentials.from_service_account_file(self.credentials_dest)
        transformed_result.to_gbq(
            destination_table=self.dest_table,
            project_id=self.project_id,
            if_exists='append',
            credentials=credentials
        )
        print("Data has been loaded.")

    def run(self):
        logging.info("Setting-up consumer")
        consumer = KafkaConsumer(
            self.topic_name,
            bootstrap_servers=[self.bootstrap_server],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=self.topic_group,
            value_deserializer=Helper.safe_deserialize
        )
        for message in consumer:
            logging.info(f"Extracting the data from the csv-s")
            source = self.extract(message.value)
            logging.info("Transforming")
            transformed_result = self.transform(source)
            logging.info(f"Load data to {self.dest_table}")
            self.load(transformed_result)
