from typing import Callable
from typing_extensions import List
import pandas as pd
import numpy
from sklearn.feature_extraction import DictVectorizer

def vectorize(df: pd.DataFrame, fit: bool) -> List[any]:
     
    dv = DictVectorizer()

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    data_dicts = df[categorical].to_dict(orient='records')
        
    if fit:
        x_data = dv.fit_transform(data_dicts)
    else:
        x_data = dv.transform(data_dicts)
    
    target = 'duration'
    y_data = df[target].values

    return x_data, y_data, dv