#!/usr/bin/env python
"""
This is what the script does:

- load model (from local file)
- load data (internet or s3)

    - If the following environment variable is set, it has precedence:

        export INPUT_FILE_PATTERN="s3://nyc-duration/in/2023-01.parquet"
        
    else, the following default value is used:
    
        INPUT_FILE_PATTERN="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet"
        
        where "month" & "year" are the names of the variables specifying the year and month of the data
    
- preprocess data
- predict duration based on the loaded data
- save the predictions

    - If the following environment variable is set, it have precedence:

        export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/2023-01.parquet"
    
    else, the following default value is used:
    
        OUTPUT_FILE_PATTERN="yellow_taxi_predictions.parquet"
        
        where "month" & "year" are the names of the variables specifying the year and month of the data
    
"""

import os
import pickle
import sys

import pandas as pd


def prepare_data(df, categorical):
    """Prepare data before using it for training"""

    df["duration"] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df["duration"] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype("int").astype("str")

    return df


def read_data(filename):
    """Read data from a file"""

    if "S3_ENDPOINT_URL" in os.environ:
        S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
        options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}
        df = pd.read_parquet(filename, storage_options=options)
    else:
        df = pd.read_parquet(filename)

    return df


def save_data(df, output_file):
    """Write a dataframe to a file"""

    if "S3_ENDPOINT_URL" in os.environ:
        S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
        options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}
        df = df.to_parquet(
            output_file,
            engine="pyarrow",
            compression=None,
            index=False,
            storage_options=options,
        )
    else:
        df = df.to_parquet(output_file, engine="pyarrow", index=False)


def get_input_path(year, month):
    default_input_pattern = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet"
    )
    input_pattern = os.getenv("INPUT_FILE_PATTERN", default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = "yellow_taxi_predictions.parquet"
    output_pattern = os.getenv("OUTPUT_FILE_PATTERN", default_output_pattern)
    return output_pattern.format(year=year, month=month)


def main(year, month):
    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)

    with open("models/model.bin", "rb") as f_in:
        dv, lr = pickle.load(f_in)

    categorical = ["PULocationID", "DOLocationID"]

    df = read_data(input_file)
    df = prepare_data(df, categorical)
    df["ride_id"] = f"{year:04d}/{month:02d}_" + df.index.astype("str")

    dicts = df[categorical].to_dict(orient="records")
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print("predicted mean duration:", y_pred.mean())

    df_result = pd.DataFrame()
    df_result["ride_id"] = df["ride_id"]
    df_result["predicted_duration"] = y_pred

    save_data(df_result, output_file)


if __name__ == "__main__":
    data_year = int(sys.argv[1])
    data_month = int(sys.argv[2])

    main(data_year, data_month)
