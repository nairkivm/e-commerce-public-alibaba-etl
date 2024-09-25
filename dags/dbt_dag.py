import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from docker.types import Mount

default_args = {
    'owner'                 : 'airflow',
    'description'           : 'Use of the DockerOperator',
    'start_date'            : datetime.now(),
    'retries'               : 1,
    'retry_delay'           : timedelta(minutes=5)
}

with DAG('dbt_dag', default_args=default_args, schedule_interval=timedelta(minutes=5), catchup=False) as dag:

    t1 = BashOperator(
        task_id='print_current_date',
        bash_command='date && echo "dbt task started..."'
        )
        
    t2 = DockerOperator(
        task_id='run_dbt',
        image='dbt_airflow_docker',
        api_version='auto',
        auto_remove=True,
        command="bash -c 'dbt build --project-dir /usr/app --profiles-dir /usr/app/.dbt'",
        docker_url='unix://var/run/docker.sock',
        network_mode="bridge",
        mounts = [
            Mount(source=f'{os.environ.get("DBT_PROJECT_LOCAL_DIR")}', target='/usr/app', type='bind'),
            Mount(source=f'{os.environ.get("CREDENTIAL_PATH_LOCAL")}', target=f'{os.environ.get("CREDENTIAL_PATH_FOR_DBT")}', type='bind'),
            Mount(source=f'{os.environ.get("DBT_LOCAL_PATH")}', target='/usr/app/.dbt', type='bind')
        ]
    )

    t3 = BashOperator(
        task_id='print_done',
        bash_command='echo "dbt build has been executed!"'
        )

    t1 >> t2 >> t3