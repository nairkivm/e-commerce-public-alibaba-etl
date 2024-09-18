from utils.etl_batch import CsvToBigQueryPipeline
import argparse
from google.oauth2 import service_account
from datetime import datetime

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Do ETL from source to destination'
    )
    parser.add_argument('--type', help='type of ingestion whether `etl` or `elt`', choices=['etl', 'elt'], required=True)
    parser.add_argument('--project-id', help='Google Workspace project_id', required=True)
    parser.add_argument('--dest', help='BigQuery table ID destination with following format `{DATASET_ID}.{TABLE_NAME}`', required=True)
    parser.add_argument('--service-account-dest', help='File path to Google\'s Service Account destination dataset', required=True)
    
    args = parser.parse_args()

    if args.type == 'etl':
        print('[ETL] STARTING...')
        starting_time = datetime.now()
        CsvToBigQueryPipeline(args.dest, args.project_id, args.service_account_dest).run()
        ending_time = datetime.now()
        elapsed_duration = ending_time - starting_time
        print(f'[ETL] DONE! ({elapsed_duration})')