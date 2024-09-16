from google.oauth2.credentials import Credentials
from pipeline import GenericPipelineInterface
from google.oauth2 import service_account
from google.cloud import bigquery
from transform import TableTransformation

import pandas as pd
import logging

logging.basicConfig(filename='ingestion.log',
                    filemode='a',
                    format='%(asctime)s - %(path)s - %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

class BigQueryToBigQueryPipeline(GenericPipelineInterface):
    
    def __init__(self, source_table: str, dest_table: str, credentials_src: Credentials, credentials_dest: Credentials):
        self.source_table = source_table
        self.dest_table = dest_table
        self.project_id_src = "fikri-project"
        self.credentials_src = credentials_src
        self.credentials_dest = credentials_dest

    def extract(self) -> pd.DataFrame:
        client = bigquery.Client.from_service_account_json(self.credentials_src)
        query = f"SELECT * FROM `{self.source_table}`"
        query_job = client.query(query)
        df = query_job.result().to_dataframe()
        return df

    def transform(self, source: pd.DataFrame) -> pd.DataFrame:
        df = source.copy()
        transformation = TableTransformation(df)
        if self.dest_table.endswith('Dim_Customer'):
            transformed_df = transformation.transformToDimCustomer()     
        elif self.dest_table.endswith('Dim_Employee'):
            transformed_df = transformation.transformToDimEmployee() 
        elif self.dest_table.endswith('Dim_Office'):
            transformed_df = transformation.transformToDimOffice()  
        elif self.dest_table.endswith('Dim_Product'):
            transformed_df = transformation.transformToProduct() 
        elif self.dest_table.endswith('Fact_Sales'):
            transformed_df = transformation.transformToFactSales()    
        return transformed_df

    def load(self, transformed_result: pd.DataFrame):
        credentials = service_account.Credentials.from_service_account_file(self.credentials_dest)
        
        transformed_result.to_gbq(
            destination_table=self.dest_table,
            project_id='fikri-project-426605',
            if_exists='replace',
            credentials=credentials
        )