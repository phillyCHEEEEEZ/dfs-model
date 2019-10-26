import os
import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# get working directory
wd = os.getcwd()

# import data
df = pd.read_csv(wd + '/nhl/data/master/aggregate_projections_all.csv')

# drop columns
columns_to_drop = ['Player', 'Position', 'Team', 'Opponent', 'Salary', 'Date']
df.drop(columns_to_drop, axis=1, inplace=True)

# drop NAs
df.dropna(inplace=True)

# separate target variable from rest of variables
X, y = df.iloc[:, :-1], df.iloc[:, -1]

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
