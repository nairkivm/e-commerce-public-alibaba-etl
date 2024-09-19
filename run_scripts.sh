#!/bin/bash

# Ensure the logs directory exists
mkdir -p /usr/src/app/logs

# Run Python script
while IFS= read -r dest; do
    dest=$(echo "$dest" | tr -d '\r' | xargs)
    echo "Processing destination: $dest"
    python3 ./main_etl_batch.py --type etl --project-id $GCP_PROJECT_ID --dest "$dest" --service-account-dest $CREDENTIAL_PATH >> "${APP_HOME}/logs/etl_error.log" 2>&1
done < /usr/src/app/batch-destination-tables.txt