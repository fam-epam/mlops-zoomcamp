import pandas as pd
from sklearn.linear_model import LinearRegression
from mlops.utils.data_preparation.vectors import vectorize

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_exporter
def export(df: pd.DataFrame, *args, **kwargs) :
    
    X_train, y_train, dv = vectorize(df, fit=True)

    lr = LinearRegression()
    lr.fit(X_train, y_train)

    print(f"{lr.intercept_:.2f}") 

    return dv, lr

