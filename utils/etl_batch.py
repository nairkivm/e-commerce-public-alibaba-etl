from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google.cloud import bigquery

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
from utils.pipeline_template import GenericPipelineInterface
from utils.transform import TableTransformation
from utils.validate_data import getDataValidation


logging.basicConfig(
    filename=f'{os.path.dirname(__file__)}\..\log\etl.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

from utils.source_requirements import SourceRequirements
from utils.destination_requirements import DestinationRequirements

csv_source_paths = {
    table_name: path for table_name, path in 
    zip(
        SourceRequirements().requirements.keys(),
        [result['source_path'] for result in SourceRequirements().requirements.values()]
    )
}

class CsvToBigQueryPipeline(GenericPipelineInterface):
    
    def __init__(self, dest_table: str, project_id: str, credentials_dest: Credentials, csv_source_paths = csv_source_paths):
        self.csv_source_paths = csv_source_paths
        self.dest_table = dest_table
        self.project_id = project_id
        self.credentials_dest = credentials_dest

    def extract(self) -> dict[str, pd.DataFrame]:
        print(f"{'EXTRACTS SOURCE DATA (CSV)':-^60}")
        dfs = {}
        source_paths = {
            table_name: path for table_name, path in 
            self.csv_source_paths.items()
            if table_name in DestinationRequirements().requirements[self.dest_table]['source_tables']
        }
        for table_name, path in source_paths.items():
            dfs[table_name] = pd.read_csv(path, sep="\t", encoding_errors='ignore')
            getDataValidation(dfs[table_name], table_name)
        return dfs

    def transform(self, source: dict[str, pd.DataFrame]) -> pd.DataFrame:
        print(f"""{f'TRANSFORMS INTO [{self.dest_table.split(".")[1]}]':-^60}""")
        dfs = source
        transformation = TableTransformation(dfs)
        if self.dest_table.endswith('fact_orders'):
            transformed_df = transformation.transformToFactOrders()
        elif self.dest_table.endswith('fact_order_details'):
            transformed_df = transformation.transformToFactOrderDetails() 
        elif self.dest_table.endswith('dim_products'):
            transformed_df = transformation.transformToDimProducts()  
        elif self.dest_table.endswith('dim_users'):
            transformed_df = transformation.transformToDimUsers() 
        elif self.dest_table.endswith('dim_vendors'):
            transformed_df = transformation.transformToDimVendors()    
        return transformed_df

    def load(self, transformed_result: pd.DataFrame):
        print(f"{f'LOAD INTO [{self.dest_table}]':-^60}")
        credentials = service_account.Credentials.from_service_account_file(self.credentials_dest)
        transformed_result.to_gbq(
            destination_table=self.dest_table,
            project_id=self.project_id,
            if_exists='replace',
            credentials=credentials
        )
        print("Data has been loaded.")
    
    def run(self):
        logging.info(f"Extracting the data from the csv-s")
        source = self.extract()
        logging.info("Transforming")
        transformed_result = self.transform(source)
        logging.info(f"Load data to {self.dest_table}")
        self.load(transformed_result)