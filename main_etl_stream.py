from utils.etl_stream import TopicsToBigQueryPipeline
import argparse
from google.oauth2 import service_account
from datetime import datetime

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Do ETL from source to destination'
    )
    parser.add_argument('--type', help='type of ingestion whether `etl` or `elt`', choices=['etl', 'elt'], required=True)
    parser.add_argument('--dest', help='BigQuery table ID destination with following format `{DATASET_ID}.{TABLE_NAME}`', required=True)
    parser.add_argument('--project-id', help='Google Workspace project_id', required=True)
    parser.add_argument('--service-account-dest', help='File path to Google\'s Service Account destination dataset', required=True)
    parser.add_argument('--bootstrap-server', help='Kafka bootstrap server. Default: "localhost:9092"', default="localhost:9092", required=True)
    parser.add_argument('--topic-name', help='Kafka topic name.', required=True)
    parser.add_argument('--topic-group', help='Kafka topic group.', required=True)
    
    args = parser.parse_args()

    if args.type == 'etl':
        print('[ETL] STARTING...')
        starting_time = datetime.now()
        TopicsToBigQueryPipeline(args.dest, args.project_id, args.service_account_dest, args.bootstrap_server, args.topic_name, args.topic_group).run()
        ending_time = datetime.now()
        elapsed_duration = ending_time - starting_time
        print(f'[ETL] DONE! ({elapsed_duration})')