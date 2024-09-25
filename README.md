# E-Commerce Public Alibaba: ETL with Lambda Architecture

## Overview

This is an ETL data pipeline project for a typical electronic store in Alibaba e-commerce platform that implement a [Lambda architecture](https://www.databricks.com/glossary/lambda-architecture) which contains two methods of data processing: batch processing and stream processing. Pandas is used for batch processing and Kafka is used for stream processing (and topic broadcasting). The batch processing is used to process "sales" data and the streaming is used to process "customer cart" and "vendor availability" data (so the vendor can know whether their products are sold out in real time). The data is extracted from txt files, transformed using Python standard and Pandas library, and loaded into Google BigQuery data warehouse. Overall, the data can be directly served to business layer using data visualization tools and SQL query or further transformed using dbt.

## Data source

[E-commerce Public Dataset by Alibaba](https://www.kaggle.com/datasets/AppleEcomerceInfo/ecommerce-information/data)

## ERD of the Source Data

<figure>
    <img src="/e-commerce-alibaba-source-erd.png"
         alt="ERD of Source Data" style="width:100%;">
    <figcaption>ERD of Source Data.</figcaption>
</figure>

## ERD of the Destination Data

<figure>
    <img src="/e-commerce-alibaba-destination-erd.png"
         alt="ERD of Destination Data" style="width:100%;">
    <figcaption>ERD of Destination Data</figcaption>
</figure>

## Data Result (After Transformation with dbt)

<figure>
    <img src="e-commerce-alibaba-userrevenue-data.png"
         alt="User Revenue Table transformed using dbt" style="width:100%;">
    <figcaption>User Revenue Table transformed using dbt</figcaption>
</figure>

## System Diagram

<figure>
    <img src="e-commerce-alibaba-system-diagram.png"
         alt="System Diagram of this project adopting Lambda Architecture" style="width:100%;">
    <figcaption>System Diagram of this project adopting Lambda Architecture</figcaption>
</figure>

## Tech Stacks

- Base           : Python, Bash
- Batch          : Pandas
- Stream         : Kafka-Python
- Transformation : dbt
- Container      : Docker
- Orchestration  : Apache Airflow (soon)
- Data Warehouse : BigQuery

## Replication

Here is a procedure if you want to replicate this data pipeline.

#### Batch Process Part 

1. Clone this repository.
2. Create a GCP project, allow the billing, enable BigQuery, [create a service account](https://cloud.google.com/iam/docs/service-accounts-create), and save the credentials key (.json) in your working directory.
3. Create a virtual environment and install all dependencies in `requirements.txt`.

```bash
# Create a python environment using venv
python -m venv venv
# Activate the virtual environments (Linux)
source venv/bin/activate
# Activate the virtual environments (Windows)
source ./venv/Scripts/activate
# Install all dependencies
pip install -r requirements.txt
```

4. If you want to run the batch ETL manually, create some variables, and run `run_etl_batch.sh`.

```bash
# If you're using Windows, switch to WSL by running `bash`
# Declare the required variables
export $GCP_PROJECT_ID=<your-gcp-project-id> # Ex: projek-etlku-2392 
export $CREDENTIAL_PATH_LOCAL=<your-abs-gcp-srvc-acc-credentials.json-path> # Ex: /usr/etl/credentials.json
export $LOCAL_APP_HOME=<your-working-dir> # Ex: /usr/etl
# Grant permission to the .sh file
chmod +x run_etl_batch.sh
# Run the file
./run_etl_batch.sh
```

5. You can customize the destination table that you want to included in the ETL-batch process in `batch-destination-tables.txt`

6. You can configure the source and destination requirements (for data validation purpose) in `./utils/source_requirements.py` & `./utils/destination_requirements.py`

7. If you want to run the ETL batch using Apache Airflow with Docker containerization, install [Docker](https://docs.docker.com/desktop/install/windows-install/)

8. Create `.env` file using this template

```env
GCP_PROJECT_ID=...(Your GCP project ID)
CREDENTIAL=...(Credential file.json)
CREDENTIAL_PATH_LOCAL=...(Credential path in your machine)
LOCAL_APP_HOME=...(Default:/opt/airflow)
POSTGRES_USER=...(Default: airflow)
POSTGRES_PASSWORD=...(Default: airflow)
POSTGRES_DB=...(Default: airflow)
CREDENTIAL_PATH_FOR_AIRFLOW=...(Credential path in Airflow Docker image)
AIRFLOW__CORE__EXECUTOR=...(Default: LocalExecutor)
AIRFLOW__CORE__SQL_ALCHEMY_CONN=...(Default: postgresql+psycopg2://airflow:airflow@postgres/airflow)
AIRFLOW__CORE__FERNET_KEY=...(You can blank this key, or use fernet_key_generator.py)
AIRFLOW__CORE__LOAD_EXAMPLES=...(Default: False)
AIRFLOW__CORE__DAGS_FOLDER=...(Default: /opt/airflow/dags)
AIRFLOW__WEBSERVER__SECRET_KEY=...(You can run airflow_webserver_secret_key_generator.sh)
AIRFLOW_ADMIN_USERNAME=...
AIRFLOW_ADMIN_PASSWORD=...
AIRFLOW_ADMIN_FIRSTNAME=...
AIRFLOW_ADMIN_LASTNAME=...
AIRFLOW_ADMIN_EMAIL=...
AIRFLOW_APP_HOME=...(Default:/opt/airflow)
```

9. Create some DAGs file for each destination tables by running `etl_batch_dag_maker.py`. You can configure some properties of the dag files (_dag_id_, _schedule_interval_, and _start_date_) based on `etl_batch_dag_template.py` file.

10. Open Docker application and while it's running, run `docker-compose up --build` in your terminal. If you don't want to build and run unrelated batch-process, comment `dbt`, `zookeper`, `kafka`, `etl-stream`, and `producer-stream` service on `docker-compose.yml`.

11. Open Airflow UI on `localhost:8080` to activate the batch-process ETLs.

#### Stream Process Part

12. If you want to run stream-process ETL manually, you have to install `Kafka` and it's dependencies (e.g. Java) and [configure it](https://www.geeksforgeeks.org/how-to-install-and-run-apache-kafka-on-windows/).

12. Start `zookeeper` and `kafka` services using this command.

(If you run it on Windows)

```console
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

(Open another terminal)

```console
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

13. Set up some configuration. You can set the destination tables that you want to stream in `stream-destination-tables.txt`. The tables requirements are also included in `./utils/source_requirements.py` & `./utils/destination_requirements.py`. 

14. Don't forget to append new key-values pair in `.env` for the stream functionality

```env
CREDENTIAL_PATH_FOR_STREAM=...(Destination for credential.json)
BOOTSTRAP_SERVER=...(Default: localhost:9092. If you run in the docker: kafka:9093)
TOPIC_NAME=...(The topic name's prefix)
TOPIC_GROUP=...(The topic name's group (For consumer purpose))
```

15. While the `zookeeper` and `kafka` services are running, open another terminal and run the producer file. Technically, the producer isn't part of the ETL-stream process because it's part of the source system.

```bash
python main_source_producer.py >> <path-to-your-producer.log-file> 2>&1
```

16. The producer broadcast the topics for every 5s, imitating real-life transactions that can happen at any time. While the producer is running, we need to run the consumer or the ETL-stream process. Open another terminal and run this.

```bash
python main_etl_stream.py >> <path-to-your-producer.log-file> 2>&1
```

17. If you want to run the stream-process using Docker containerization, modify the `.env` file (`CREDENTIAL_PATH_FOR_STREAM` and `BOOTSTRAP_SERVER`) and uncomment `zookeper`, `kafka`, `etl-stream`, and `producer-stream` service on `docker-compose.yml` (if you previously comment it out).

18. Run `docker-compose up --build` in your terminal. Now, both batch and stream ETL process are activated.

19. To deactivate the services, run `docker-compose down`. You can also use `docker-compose start` and `docker-compose stop` to turn on/off the services.

#### DBT Extension

20. If you want to attach dbt functionality to the pipeline, install dbt-core and dbt-<your-preferred-adapter> on your local.

```bash
pip install dbt-core==1.8.6 \
pip install dbt-bigquery==1.8.2
```

21. Initialize your dbt project on a custom directory (For me, I initialized the project on dbt_project folder).

```bash
mkdir dbt_project \
cd dbt_project \
dbt init <your-custom-dbt-project-name>
```

22. When you initialize for the first time, you will be getting prompts to create a `profiles.yml`. If you failed this process, you can make the `profiles.yml` manually using `profiles-generator.py`.

23. Create your dbt models, tests, documentations, etc.

24. To run the dbt on Apache Airflow, uncomment the `dbt` service on `docker-compose.yml`.

25. Add some variables to `.env` file.

```env
CREDENTIAL_PATH_FOR_DBT=... (Credentials.json path in your dbt image)
DBT_PROJECT_NAME=...
DBT_PROJECT_LOCAL_DIR=...(Absolute path of your local dbt project)
DBT_LOCAL_PATH=...(Absolute path of your .dbt folder (folder that contains profiles.yml))
DBT_DATASET_NAME=...(Your schema/dataset name in your data warehouse)
```

26. Run `docker-compose up --build` in your terminal. After the tables in the data warehouse has been filled by batch and streaming process, you can run dbt transformation manually by running `dbt_dag` on Airflow UI. By default, this task runs `dbt build` command, but you can modify it with `dbt debug` or something else in the `dbt_dag.py` file inside `dags` folder. You don't need to restart the docker container because the volume on your local machine has been mapped to the Airflow Docker image already.

27. To deactivate the services, run `docker-compose down`. You can also use `docker-compose start` and `docker-compose stop` to turn on/off the services.

#### Extra

28. You can generate more data by modifying the files in `data_source` folder or running a python script, `data_generator.py`.

## Main Reference

- [Partnatech DE Course](https://x.com/nairkivm/status/1804431988146983374)
- [Big Data Architecture – Detailed Explanation](https://www.interviewbit.com/blog/big-data-architecture/)
- [How to Install and Run Apache Kafka on Windows?](https://www.geeksforgeeks.org/how-to-install-and-run-apache-kafka-on-windows/)
- [Hello Kafka World! The complete guide to Kafka with Docker and Python](https://medium.com/big-data-engineering/hello-kafka-world-the-complete-guide-to-kafka-with-docker-and-python-f788e2588cfc)
- [Deploy a Kafka broker in a Docker container](https://www.kaaiot.com/blog/kafka-docker)
- [About dbt core](https://docs.getdbt.com/docs/core/about-core-setup)
- [How to run dbt core from an Airflow pipeline using the DockerOperator](https://medium.com/@tdonizeti/how-to-run-dbt-core-from-an-airflow-pipeline-using-the-dockeroperator-e48cf215e9f6)