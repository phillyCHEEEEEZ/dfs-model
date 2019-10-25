
# https://www.datacamp.com/community/tutorials/xgboost-in-python

import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt

from sklearn.datasets import load_boston
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# import data
boston = load_boston()

# print descriptives
print(boston.keys())
print(boston.data.shape)
print(boston.feature_names)
print(boston.DESCR)

# convert to data frame
data = pd.DataFrame(boston.data)
data.columns = boston.feature_names
data.head()

# append price
data['PRICE'] = boston.target

# info & summary stats
data.info()
data.describe()

# separate target variable from rest of variables
X, y = data.iloc[:, :-1], data.iloc[:, -1]

# convert into Dmatrix
data_dmatrix = xgb.DMatrix(data=X, label=y)


####### basic xgboost #######
# create train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=123)

# initialize xgboost regressor
xg_reg = xgb.XGBRegressor(objective='reg:linear', colsample_bytree=0.3, learning_rate=0.1,
                          max_depth=5, alpha=10, n_estimators=10)

# fit regressor to training set and make predictions
xg_reg.fit(X_train, y_train)
preds = xg_reg.predict(X_test)

# compute RMSE
rmse = np.sqrt(mean_squared_error(y_test, preds))
print("RMSE: %f" % (rmse))


####### k-fold cross validation #######
# create dictionary for parameters
params = {"objective": "reg:linear", 'colsample_bytree': 0.3, 'learning_rate': 0.1,
          'max_depth': 5, 'alpha': 10}

# build 3-fold cross validation model
cv_results = xgb.cv(dtrain=data_dmatrix, params=params, nfold=3,
                    num_boost_round=50, early_stopping_rounds=10, metrics="rmse", as_pandas=True, seed=123)
cv_results.head()

# print final boosting metric
print((cv_results["test-rmse-mean"]).tail(1))


####### visualize boosting trees and feature importance #######
# initialize xgboost regressor
xg_reg = xgb.train(params=params, dtrain=data_dmatrix, num_boost_round=10)

# plot tree
xgb.plot_tree(xg_reg, num_trees=0)
plt.rcParams['figure.figsize'] = [50, 10]
plt.show()

# plot feature importance
xgb.plot_importance(xg_reg)
plt.rcParams['figure.figsize'] = [5, 5]
plt.show()
