from sklearn.ensemble import RandomForestRegressor

class ForecasterWrapper:
    """ Base object to roll a neural network model.
    Rolling over a time axis with a train period from `t - n` to `t` and a
    testing period from `t` to `t + s`.
    Parameters
    ----------
    X, y : array_like
        Respectively input and output data.
    f : callable, optional
        Function to transform target, e.g. ``torch.sign`` function.
    index : array_like, optional
        Time index of data.
    Methods
    -------
    __call__
    Attributes
    ----------
    n, s, r : int
        Respectively size of training, testing and rolling period.
    b, e, T : int
        Respectively batch size, number of repass_steps and size of entire dataset.
    t : int
        The current time period.
    y_eval, y_test : np.ndarray[ndim=1 or 2, dtype=np.float64]
        Respectively evaluating (or training) and testing predictions.
    """
    def __init__(self, method = 'standard'):
        """ Initialize shape of target. """
        if method == 'standard':
            self.model  = RandomForestRegressor(max_depth=5, random_state=0)

    def fit(self, X_train, y_train, method = 'standard'):
        if method == 'standard':
            self.model.fit(X_train, y_train)

    def predict(self, X_test, method = 'standard'):
        if method == 'standard':
            y_pred = self.model.predict(X_test)
            return y_pred
        return None




