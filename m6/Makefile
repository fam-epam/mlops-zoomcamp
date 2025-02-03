TEST_BUCKET_NAME := nyc-duration
export INPUT_FILE_PATTERN=s3://$(TEST_BUCKET_NAME)/in/2023-01.parquet
export OUTPUT_FILE_PATTERN=s3://$(TEST_BUCKET_NAME)/out/2023-01.parquet
export S3_ENDPOINT_URL=http://localhost:4566


all: test setup s3 integration_test cleanup

test:
	echo "Executing the unit tests ..."
	pytest tests/
	echo

integration_test: s3
	echo "Executing the integration test"
	# python integration_test.py 2023 1	# alternative variant - requires enabling the code from 'integration_test.py'
	bash run.sh	# first variant
	echo

setup:
	echo "Bringing up the 'localstack'"
	docker compose up -d
	sleep 5

s3: setup
	echo "Creating the S3 bucket"
	aws s3 mb s3://${TEST_BUCKET_NAME} --endpoint-url http://localhost:4566
	echo

cleanup:
	echo "Cleaning up ..."
	docker compose down
	echo