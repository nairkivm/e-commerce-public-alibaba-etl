E-Commerce Public Alibaba: ETL with Lambda Architecture

Command to run batch process directly: 
`python main_etl_batch.py --type etl --project-id %GCP_PROJECT_ID% --dest "store.fact_orders" --service-account-dest %CREDENTIALS_PATH% >> "%cd%/log/etl_error.log" 2>&1`

python main_etl_stream.py --type etl --dest "store.fact_products_sold_vendor" --project-id "fikri-project-426605" --service-account-dest "c_destination.json" --bootstrap-server "localhost:9092" --topic-name "products_test" --topic-group "products" 