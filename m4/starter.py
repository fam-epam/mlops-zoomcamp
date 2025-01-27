#!/usr/bin/env python

import pickle
import pandas as pd
import argparse


parser = argparse.ArgumentParser(description="Process year and month")
parser.add_argument('year', type=int, help='year of the data')
parser.add_argument('month', type=int, help='month of the data')
args = parser.parse_args()

year = args.year
month = args.month


def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet')

dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)

df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
df['pred_duration'] = y_pred

df_result = df[["ride_id", "pred_duration"]]

output_file = "ride_predictions.pkt"

df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)

print(f"Main predicted duration ({year:04}-{month:02}): {df_result['pred_duration'].mean():.2f}")


