from datetime import datetime
from pprint import pprint

import pandas as pd
from deepdiff import DeepDiff

from batch import prepare_data


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def test_prepare_data():
    columns_test = [
        "PULocationID",
        "DOLocationID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
    ]
    data_test = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    columns_ref = [
        "PULocationID",
        "DOLocationID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "duration",
    ]
    data_ref = [
        ("-1", "-1", dt(1, 1), dt(1, 10), 9),
        ("1", "1", dt(1, 2), dt(1, 10), 8),
    ]

    df_test = pd.DataFrame(data_test, columns=columns_test)
    df_ref = pd.DataFrame(data_ref, columns=columns_ref)

    categorical = ["PULocationID", "DOLocationID"]
    df_test = prepare_data(df_test, categorical)

    ddiff = DeepDiff(df_test.to_dict(), df_ref.to_dict())

    if df_test.to_dict() != df_ref.to_dict():
        pprint(ddiff, indent=4)

    assert df_test.to_dict() == df_ref.to_dict()


test_prepare_data()
