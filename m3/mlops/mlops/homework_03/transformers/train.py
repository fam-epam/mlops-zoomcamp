import pandas as pd
from sklearn.linear_model import LinearRegression
from mlops.utils.data_preparation.vectors import vectorize

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def export(df: pd.DataFrame, *args, **kwargs) :
    
    X_train, y_train, dv = vectorize(df, fit=True)

    lr = LinearRegression()
    lr.fit(X_train, y_train)

    print(f"{lr.intercept_:.2f}") 

    return dv, lr

