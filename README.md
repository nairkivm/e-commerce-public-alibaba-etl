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

4. If you want to run the batch ETL manually, create some variables, and run `run_scripts.sh`.

```bash
# If you're using Windows, switch to WSL by running `bash`
# Declare the required variables
export $GCP_PROJECT_ID=<your-gcp-project-id> # Ex: projek-etlku-2392 
export $CREDENTIAL_PATH=<your-abs-gcp-srvc-acc-credentials.json-path> # Ex: /usr/etl/credentials.json
export $APP_HOME=<your-working-dir> # Ex: /usr/etl
# Grant permission to the .sh file
chmod +x run_scripts.sh
# Run the file
./run_scripts.sh
```

5. You can customize the destination table that want to included in the ELT-batch process in `batch-destination-tables.txt`

6. You can configure the source and destination requirements (for data validation purpose) in `./utils/source_requirements.py` & `./utils/destination_requirements.py`

7. If you want to run the ETL batch using containerization, install [Docker](https://docs.docker.com/desktop/install/windows-install/)

8. Create `.env` file using this template

```env
GCP_PROJECT_ID=<your-gcp-project-id>
CREDENTIAL_PATH=<your-abs-gcp-srvc-acc-credentials.json-path>
APP_HOME=<your-working-dir>
```

9. Open Docker application and while it's running, run `docker-compose up --build` in your terminal. You can see the log in the `logs` folder.

10. For now, the ETL-stream is not available in the containerization. If you want to run it manually, you have to install `Kafka` and it's dependencies (e.g. Java) and [configure it](https://www.geeksforgeeks.org/how-to-install-and-run-apache-kafka-on-windows/).

11. Start `zookeeper` and `kafka` services using this command.

(If you run it on Windows)

```console
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

(Open another terminal)

```console
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

12. While the two services is running, open another terminal and run the producer file. Technically, the producer isn't part of the ETL-stream process because it's part of the source system.

```bash
python main_source_producer.py --source-table <source.csv-path> --bootstrap-server <default:"localhost:9092">
--topic-name <your-custom-topic-name> >> <path-to-your-producer.log-file> 2>&1
```

13. The producer broadcast the topics for every 5s, imitating real-life transactions that can happen at any time. While the producer is running, we need to run the consumer or the ETL-stream process. Open another terminal and run this.

```bash
python main_etl_stream.py --type etl --dest <your-destination-table-in-big-query> --project-id <your-gcp-project-id> --service-account-dest <your-abs-gcp-srvc-acc-credentials.json-path> --bootstrap-server "localhost:9092" --topic-name <your-custom-topic-name> --topic-group <your-custom-topic-group-name>
```