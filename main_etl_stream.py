import threading
import os

from utils.etl_stream import TopicsToBigQueryPipeline

if __name__ == '__main__':
    print(f'[ETL] STARTING...')

    dest_tables = [str(x).removesuffix('\n') for x in open('./stream-destination-tables.txt')]
    project_id = os.environ.get('GCP_PROJECT_ID')
    srvc_acc_dest = os.environ.get('CREDENTIAL_PATH_FOR_STREAM')
    bootstrap_server = os.environ.get('BOOTSTRAP_SERVER')
    topic_group = os.environ.get('TOPIC_GROUP')
    
    threads = []
    for dest in dest_tables:
        topic_name = os.environ.get('TOPIC_NAME')+f'_{dest.split(".")[1]}'
        pipeline = TopicsToBigQueryPipeline(dest, project_id, srvc_acc_dest, bootstrap_server, topic_name, topic_group)
        thread = threading.Thread(target=pipeline.run)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f'[ETL] DONE!')
    