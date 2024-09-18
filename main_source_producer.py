from utils.source_producer import CsvToProducerPipeline
import argparse
from datetime import datetime

from utils.source_requirements import SourceRequirements

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Produce the topics'
    )
    parser.add_argument('--source-table', help='Source table nama', required=True)
    parser.add_argument('--bootstrap-server', help='Kafka bootstrap server. Default: "localhost:9092"', default="localhost:9092", required=True)
    parser.add_argument('--topic-name', help='Kafka topic name.', required=True)
    
    args = parser.parse_args()

    print('[Topic Producer] STARTING...')
    starting_time = datetime.now()
    CsvToProducerPipeline(args.source_table, SourceRequirements().requirements[args.source_table]['source_path'], args.bootstrap_server, args.topic_name).run()
    ending_time = datetime.now()
    elapsed_duration = ending_time - starting_time
    print(f'[Topic Producer] DONE! ({elapsed_duration})')