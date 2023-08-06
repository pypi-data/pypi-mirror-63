from napoleontoolbox.rebalancing import rolling
from sklearn.metrics import mean_squared_error
import pandas as pd

def rolling_forecasting(forecasting_model, X, y, n=252, s=63, method = 'standard', display = False, **kwargs):
    assert X.shape[0] == y.shape[0]
    idx = X.index
    forecasting_series = pd.Series(index=idx, name='prediction')
    roll = rolling._RollingMechanism(idx, n=n, s=s)
    for slice_n, slice_s in roll():
        # Select X
        X_train = X.loc[slice_n].copy()
        y_train = y.loc[slice_n].copy()

        X_test = X.loc[slice_s].copy()
        y_test = y.loc[slice_s].copy()

        forecasting_model.fit(X_train, y_train, method)
        y_pred = forecasting_model.predict(X_test, method)
        forecasting_series.loc[slice_s] = y_pred.values
        if display:
            print('rmse for slice ' + str(slice_s))
            mean_squared_error(y_test, y_pred, squared=False)
    return forecasting_series

