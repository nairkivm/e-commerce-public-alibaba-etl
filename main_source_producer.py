import threading
import os

from utils.source_producer import CsvToProducerPipeline
from utils.destination_requirements import DestinationRequirements
from utils.source_requirements import SourceRequirements
from utils.check_connection import check_connection

if __name__ == '__main__':
    print(f'[Topic Producer] STARTING...')

    dest_tables = [str(x).removesuffix('\n') for x in open('./stream-destination-tables.txt')]
    
    threads = []
    for table_name in dest_tables:
        source_table = DestinationRequirements().requirements[table_name]['source_tables'][0]
        csv_source_path = SourceRequirements().requirements[source_table]['source_path']
        bootstrap_server = os.environ.get('BOOTSTRAP_SERVER')
        topic_name = os.environ.get('TOPIC_NAME')+f'_{table_name.split(".")[1]}'
        print(
            'source_table: ', source_table, '\n',
            'csv_source_path: ', csv_source_path, '\n',
            'bootstrap_server: ', bootstrap_server, '\n',
            'topic_name: ', topic_name
        )
        check_connection(bootstrap_server.split(":")[0], bootstrap_server.split(":")[1])
        pipeline = CsvToProducerPipeline(source_table, csv_source_path, bootstrap_server, topic_name)
        thread = threading.Thread(target=pipeline.run)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    print(f'[Topic Producer] DONE!')