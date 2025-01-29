#!/usr/bin/env python

import pickle
import pandas as pd
import argparse

CATEGORICAL = ['PULocationID', 'DOLocationID']
year = 2023
month = 5


def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[CATEGORICAL] = df[CATEGORICAL].fillna(-1).astype('int').astype('str')
    
    return df

def load_model(model_file):
    with open(model_file, 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return dv,model

dv, model = load_model('model.bin')


def load_data(year, month):
    df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet')
    return df

df = load_data(year, month)

def predict(dv, model, df):
    dicts = df[CATEGORICAL].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    return y_pred

y_pred = predict(dv, model, df)

def save(year, month, df, y_pred):
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
    
    return df_result

df_result = save(year, month, df, y_pred)

print(f"Main predicted duration ({year:04}-{month:02}): {y_pred.mean():.2f}")


