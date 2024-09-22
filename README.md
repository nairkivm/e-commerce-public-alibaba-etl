# E-Commerce Public Alibaba: ETL with Lambda Architecture

## Overview

This is an ETL data pipeline project for a typical electronic store in Alibaba e-commerce platform that implement a [Lambda architecture](https://www.databricks.com/glossary/lambda-architecture) which contains two methods of data processing: batch processing and stream processing. Pandas is used for batch processing and Kafka is used for stream processing (and topic broadcasting). The batch processing is used to process "sales" data and the streaming is used to process "customer cart" and "vendor availability" data (so the vendor can know whether their products are sold out in real time). The data is extracted from csv files, transformed using Python standard and Pandas library, and loaded into Google BigQuery data warehouse.

# Data source

[E-commerce Public Dataset by Alibaba](https://www.kaggle.com/datasets/AppleEcomerceInfo/ecommerce-information/data)

### Tech Stacks

- Base           : Python, Bash
- Batch          : Pandas
- Stream         : Kafka-Python
- Container      : Docker
- Orchestration  : Apache Airflow (soon)
- Data Warehouse : BigQuery

### Replication

Here is a procedure if you want to replicate this data pipeline.

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
export $CREDENTIAL_PATH=<your-abs-gcp-srvc-acc-credentials.json-path> # Ex: /usr/etl/credentials.json
export $APP_HOME=<your-working-dir> # Ex: /usr/etl
# Grant permission to the .sh file
chmod +x run_etl_batch.sh
# Run the file
./run_etl_batch.sh
```

5. You can customize the destination table that want to included in the ETL-batch process in `batch-destination-tables.txt`

6. You can configure the source and destination requirements (for data validation purpose) in `./utils/source_requirements.py` & `./utils/destination_requirements.py`

7. If you want to run the ETL batch using Apache Airflow with Docker containerization, install [Docker](https://docs.docker.com/desktop/install/windows-install/)

8. Create `.env` file using this template

```env
GCP_PROJECT_ID=...(Your GCP project ID)
CREDENTIAL_PATH=...(Credential path in Docker)
CREDENTIAL=...(Credential file.json)
APP_HOME=...(Default:/opt/airflow)
AIRFLOW__CORE__EXECUTOR=...(Default: LocalExecutor)
AIRFLOW__CORE__SQL_ALCHEMY_CONN=...(Default: postgresql+psycopg2://airflow:airflow@postgres/airflow)
AIRFLOW__CORE__FERNET_KEY=...(You can blank this key, or use fernet_key_generator.py)
AIRFLOW__CORE__LOAD_EXAMPLES=...(Default: False)
AIRFLOW__CORE__DAGS_FOLDER=...(Default: /opt/airflow/dags)
AIRFLOW__WEBSERVER__SECRET_KEY=...(You can run airflow_webserver_secret_key_generator.sh)
ADMIN_USERNAME=...
ADMIN_PASSWORD=...
ADMIN_FIRSTNAME=...
ADMIN_LASTNAME=...
ADMIN_EMAIL=...
POSTGRES_USER=...(Default: airflow)
POSTGRES_PASSWORD=...(Default: airflow)
POSTGRES_DB=...(Default: airflow)
```

9. Create some DAGs file for each destination tables by running `etl_batch_dag_maker.py`. You can configure some properties of the dag files (_dag_id_, _schedule_interval_, and _start_date_) based on `etl_batch_dag_template.py` file.

10. Open Docker application and while it's running, run `docker-compose up --build` in your terminal. If you don't want to build and run unrelated batch-process, comment `zookeper`, `kafka`, `etl-stream`, and `producer-stream` service on `docker-compose.yml`.

11. Open Airflow UI on `localhost:8080` to activate the batch-process ETLs.

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
TOPIC_GROUP=...
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