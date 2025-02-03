"""Create test file(s) in localstack s3 bucket"""

import os
import sys
from datetime import datetime
from batch import read_data, get_output_path

import pandas as pd


def dt(hour, minute, second=0):
    """Helper function"""

    return datetime(2023, 1, 1, hour, minute, second)


def create_test_df():
    """Create a test dataframe"""

    columns = [
        "PULocationID",
        "DOLocationID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
    ]
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]
    df = pd.DataFrame(data, columns=columns)

    return df


def save_input_to_s3(df, year, month):
    input_file = os.getenv("INPUT_FILE_PATTERN", default=f"s3://nyc-duration/in/{year:04d}-{month:02d}.parquet")
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", default="http://localhost:4566")
    # input_file = os.getenv("INPUT_FILE_PATTERN")
    # S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")

    options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}
    df.to_parquet(
        input_file,
        engine="pyarrow",
        compression=None,
        index=False,
        storage_options=options,
    )


def calculate_predictions_sum(year, month):

    input_file = get_output_path(year, month)
    df = read_data(input_file)

    return float(f"{df['predicted_duration'].sum():.2f}")


def main(year, month):
    df = create_test_df()
    save_input_to_s3(df, year, month)

    # print("Execute the batch script ...")
    # command = f"python batch.py {year} {month}"
    # batch_return_code = os.system(command)

    # if batch_return_code != 0:
    #     print("Batch failed with return code:", batch_return_code)

    # predictions_sum = calculate_predictions_sum(year, month)
    # print(f"Predictions sum: {predictions_sum}")
    # assert predictions_sum == 36.28


if __name__ == "__main__":
    data_year = int(sys.argv[1])
    data_month = int(sys.argv[2])

    main(data_year, data_month)
