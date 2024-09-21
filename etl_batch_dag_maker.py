import os

from utils.destination_requirements import DestinationRequirements
from utils.source_requirements import SourceRequirements
from etl_batch_dag_template import etl_batch_dag_template

dest_tables = [str(x).removesuffix('\n') for x in open('./batch-destination-tables.txt')]
dest_requirements = DestinationRequirements().requirements
src_requirements = SourceRequirements().requirements
dag_template = etl_batch_dag_template

output_dir = 'dags'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for table_name in dest_tables:
    dag_id = f'{table_name.split(".")[1]}_dag'
    schedule_interval = '30 6 * * *'
    start_date = 'datetime(2024,9,20)'
    dest_table = f"'{table_name}'"

    dag_content = dag_template.format(
        dag_id=dag_id,
        schedule_interval=schedule_interval,
        start_date=start_date,
        dest_table=dest_table
    )
    dag_file_path = os.path.join(output_dir, f'{dag_id}.py')
    
    with open(dag_file_path, 'w') as dag_file:
        dag_file.write(dag_content)

print("DAG files generated successfully.")
