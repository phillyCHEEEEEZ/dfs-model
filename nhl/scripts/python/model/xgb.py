import os
import datetime
import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# datetime vars
now = datetime.datetime.now()
today = str(now.strftime('%Y-%m-%d'))

# get working directory
wd = 'c:/dev/Python/Repos/dfs-model/'

# import data
df_history = pd.read_csv(wd + '/nhl/data/master/aggregate_projections_all.csv')
df_today = pd.read_csv(wd + '/nhl/data/aggregate_projections.csv')

# combine data
df = df_history.append(df_today, ignore_index=True)

# categorical columns
cat_columns = ['Position']

# one hot encoding
df = pd.get_dummies(df, prefix_sep="_", columns=cat_columns)

# drop columns
columns_to_drop = ['Player', 'Team', 'Opponent', 'Salary', 'Date', 'Actual', ]
df.drop(columns_to_drop, axis=1, inplace=True)

# reorder
df = df[['Position_C', 'Position_W', 'Position_D', 'Position_G', 'Line',
         'PP Line', 'Moneyline', 'Over/Under', 'Spread', 'Team Pts',
         'FC', 'RW', 'NF', 'DFF', 'Avg']]

# drop NAs
# df.dropna(inplace=True)

# separate target variable from rest of variables
x, y = df.iloc[:, :-1], df.iloc[:, -1]

# convert into Dmatrix
data_dmatrix = xgb.DMatrix(data=x, label=y)


####### basic xgboost #######
# create train and test sets
x_train = x[:len(df_history)]
x_test = x[len(df_history):]
y_train = y[:len(df_history)]
y_test = y[len(df_history):]

# initialize xgboost regressor
xg_reg = xgb.XGBRegressor(objective='reg:squarederror', colsample_bytree=0.3, learning_rate=0.1,
                          max_depth=5, alpha=10, n_estimators=10)

# fit regressor to training set and make predictions
xg_reg.fit(x_train, y_train)
preds = xg_reg.predict(x_test)

# compute RMSE
rmse = np.sqrt(mean_squared_error(y_test, preds))
print("RMSE: %f" % (rmse))

# plot feature importance
xgb.plot_importance(xg_reg)
plt.rcParams['figure.figsize'] = [5, 5]
# plt.show()


####### k-fold cross validation #######
# create dictionary for parameters
params = {"objective": "reg:squarederror", 'colsample_bytree': 0.3, 'learning_rate': 0.1,
          'max_depth': 5, 'alpha': 10}

# build 3-fold cross validation model
cv_results = xgb.cv(dtrain=data_dmatrix, params=params, nfold=3,
                    num_boost_round=50, early_stopping_rounds=10, metrics="rmse", as_pandas=True, seed=123)
cv_results.head()

# print final boosting metric
print((cv_results["test-rmse-mean"]).tail(1))


# add projections to aggreagted data
df_today['XGB'] = preds
df_today['XGB'] = df_today['XGB'].apply(lambda x: round(x, 2))
df_today = df_today[['Player', 'Position', 'Team', 'Opponent', 'Salary', 'Date', 'Line',
                     'PP Line', 'Moneyline', 'Over/Under', 'Spread', 'Team Pts', 'FC', 'RW',
                     'NF', 'DFF', 'Avg', 'XGB', 'Actual']]

# export
df_today.to_csv(
    wd + '/nhl/data/aggregate_projections.csv',
    index=False)

df_today[['Player', 'XGB']].to_csv(
    wd + '/nhl/data/fc_upload.csv',
    index=False)
