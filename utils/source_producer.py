import pandas as pd
import logging
from kafka import KafkaProducer
from json import dumps
from time import sleep
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
    filename=f'{os.path.dirname(__file__)}\..\log\source_producer.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

from utils.source_requirements import SourceRequirements
from utils.destination_requirements import DestinationRequirements

class CsvToProducerPipeline():
    
    def __init__(self, source_table: str, csv_source_path: str, bootstrap_server: str, topic_name: str):
        self.csv_source_path = csv_source_path
        self.source_table = source_table
        self.bootstrap_server = bootstrap_server
        self.topic_name = topic_name

    def get_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.csv_source_path, sep="\t", encoding_errors='ignore')
        return df

    def broadcast_topics(self, producer: KafkaProducer, df: pd.DataFrame) -> None:
        for i, rows in df.iterrows():
            value = rows.to_dict()
            print(i, value)
            producer.send(self.topic_name, value=value)
            sleep(5)
        producer.flush()

    def run(self):
        logging.info(f"Producing the topic for [{self.source_table}]")
        # Set producer
        producer = KafkaProducer(
            bootstrap_servers=[self.bootstrap_server],
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )
        # Broadcast topics
        self.broadcast_topics(producer, self.get_data())

