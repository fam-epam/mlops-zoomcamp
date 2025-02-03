#!/usr/bin/env bash

set -e

export TEST_BUCKET_NAME="nyc-duration"
export INPUT_FILE_PATTERN="s3://${TEST_BUCKET_NAME}/in/2023-01.parquet"
export OUTPUT_FILE_PATTERN="s3://${TEST_BUCKET_NAME}/out/2023-01.parquet"
export S3_ENDPOINT_URL="http://localhost:4566"

YEAR=2023
MONTH=1

echo; echo  "> Creating the s3 bucket ..."
aws s3 mb s3://nyc-duration --endpoint-url http://localhost:4566
# aws s3 ls --endpoint-url http://localhost:4566

echo; echo  "> Creating the test data and uploading it to s3"
python integration_test.py ${YEAR} ${MONTH}
# aws s3 ls s3://nyc-duration --endpoint-url http://localhost:4566 --recursive | awk '{print $3}'

echo; echo  "> Calculate the predictions and upload the results to s3"
python batch.py ${YEAR} ${MONTH}

echo; echo "> Calculate the sum of the predictions"
python get_results.py ${YEAR} ${MONTH}