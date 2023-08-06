import numpy as np
import pandas as pd


from napoleontoolbox.rebalancing import rolling


def rolling_forecasting(f, X, y, n=252, s=63, ret=True, drift=True, filtering_threshold = 0.7, **kwargs):
    X = pd.DataFrame(X).fillna(method='ffill')
    idx = X.index
    w_mat = pd.DataFrame(index=idx, columns=X.columns)
    portfolio = pd.Series(100., index=idx, name='portfolio')

    if ret:
        X_ = X.pct_change()

    else:
        X_ = X

    roll = rolling._RollingMechanism(idx, n=n, s=s)

    def allocation_process(series):
        # True if less than 50% of obs. are constant
        return series.value_counts(dropna=False).max() < filtering_threshold * n

    for slice_n, slice_s in roll():
        # Select X
        sub_X = X_.loc[slice_n].copy()
        assets = list(X.columns[sub_X.apply(allocation_process)])
        sub_X = sub_X.fillna(method='bfill')
        # Compute weights
        if len(assets) == 1:
            w = np.array([[1.]])

        else:
            w = f(sub_X.loc[:, assets].values, **kwargs)

        if w.flatten().sum(axis = 0 )>1:
            w=w/w.sum(axis=0)
        w_mat.loc[roll.d, assets] = w.flatten()
        w_mat.loc[roll.d, :] = w_mat.loc[roll.d, :].fillna(0.)
        # Compute portfolio performance
        # perf = _perf_alloc(
        #     X.loc[slice_s, assets].fillna(method='bfill').values,
        #     w=w,
        #     drift=drift
        # )
        # portfolio.loc[slice_s] = portfolio.loc[roll.d] * perf.flatten()

    #w_mat = w_mat.fillna(method='ffill').fillna(0.)

    #return portfolio, w_mat
    return None

