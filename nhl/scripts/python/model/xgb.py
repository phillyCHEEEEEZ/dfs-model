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
df_history = pd.read_csv(
    wd + '/nhl/data/master/aggregate_projections_all.csv')
df_today = pd.read_csv(wd + '/nhl/data/aggregate_projections.csv')

# duplicate data frames
df = df_history
df_preds = df_today

# categorical columns
cat_columns = ['Position']

# one hot encoding
df = pd.get_dummies(df, prefix_sep="_", columns=cat_columns)
df_preds = pd.get_dummies(df_preds, prefix_sep="_", columns=cat_columns)

# drop columns
columns_to_drop = ['Name', 'Team', 'Opponent', 'Date', 'Avg', ]
df.drop(columns_to_drop, axis=1, inplace=True)

columns_to_drop = ['Name', 'Team', 'Opponent', 'Date', 'Avg', 'Actual']
df_preds.drop(columns_to_drop, axis=1, inplace=True)

# reorder
df = df[['Position_C', 'Position_D', 'Position_G', 'Position_W',
         'Salary', 'FC', 'RW', 'NF', 'DFF', 'EV', 'PP', 'ML',
         'O/U', 'Spread', 'TM/P', 'G_RW', 'A_RW', 'PTS_RW', '+/-_RW', 'PIM_RW',
         'SOG_RW', 'GWG_RW', 'PPG_RW', 'PPA_RW', 'SHG_RW', 'SHA_RW', 'Hits_RW',
         'BS_RW', 'W_RW', 'L_RW', 'OTL_RW', 'GA_RW', 'SA_RW', 'SV_RW', 'SV%_RW',
         'SO_RW', 'SOG_NF', 'G_NF', 'A_NF', 'PTS_NF', 'PPG_NF', 'PPA_NF',
         '+/-_NF', 'BS_NF', 'MINS_NF', 'PIM_NF', 'GA_NF', 'SA_NF', 'SV_NF',
         'SO_NF', 'W_NF', 'Actual']]

df_preds = df_preds[['Position_C', 'Position_D', 'Position_G', 'Position_W',
                     'Salary', 'FC', 'RW', 'NF', 'DFF', 'EV', 'PP', 'ML',
                     'O/U', 'Spread', 'TM/P', 'G_RW', 'A_RW', 'PTS_RW', '+/-_RW', 'PIM_RW',
                     'SOG_RW', 'GWG_RW', 'PPG_RW', 'PPA_RW', 'SHG_RW', 'SHA_RW', 'Hits_RW',
                     'BS_RW', 'W_RW', 'L_RW', 'OTL_RW', 'GA_RW', 'SA_RW', 'SV_RW', 'SV%_RW',
                     'SO_RW', 'SOG_NF', 'G_NF', 'A_NF', 'PTS_NF', 'PPG_NF', 'PPA_NF',
                     '+/-_NF', 'BS_NF', 'MINS_NF', 'PIM_NF', 'GA_NF', 'SA_NF', 'SV_NF',
                     'SO_NF', 'W_NF']]

# drop NAs
df.dropna(subset=['Actual'], inplace=True)

# separate target variable from rest of variables
x, y = df.iloc[:, :-1], df.iloc[:, -1]

# convert into Dmatrix
data_dmatrix = xgb.DMatrix(data=x, label=y)


####### basic xgboost #######
# create train and test sets
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=123)

# initialize xgboost regressor
xg_reg = xgb.XGBRegressor(objective='reg:squarederror', colsample_bytree=0.3,
                          learning_rate=0.1, max_depth=5, alpha=10, n_estimators=10)

# fit regressor to training set and make predictions
xg_reg.fit(x_train, y_train)
preds = xg_reg.predict(x_test)

# compute RMSE
rmse = np.sqrt(mean_squared_error(y_test, preds))
print("RMSE: %f" % (rmse))

# plot feature importance
xgb.plot_importance(xg_reg)
plt.rcParams['figure.figsize'] = [10, 10]
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


# calculate projections for today's players
preds_today = xg_reg.predict(df_preds)

# add projections to aggreagted data
df_today['XGB'] = preds_today
df_today['XGB'] = df_today['XGB'].apply(lambda x: round(x, 2))
df_today = df_today[['Name', 'Position', 'Team', 'Opponent', 'Salary', 'Date', 'FC', 'RW', 'NF',
                     'DFF', 'Avg', 'XGB', 'Actual', 'EV', 'PP', 'ML', 'O/U', 'Spread', 'TM/P',
                     'G_RW', 'A_RW', 'PTS_RW', '+/-_RW', 'PIM_RW', 'SOG_RW', 'GWG_RW',
                     'PPG_RW', 'PPA_RW', 'SHG_RW', 'SHA_RW', 'Hits_RW', 'BS_RW', 'W_RW',
                     'L_RW', 'OTL_RW', 'GA_RW', 'SA_RW', 'SV_RW', 'SV%_RW', 'SO_RW',
                     'SOG_NF', 'G_NF', 'A_NF', 'PTS_NF', 'PPG_NF', 'PPA_NF', '+/-_NF',
                     'BS_NF', 'MINS_NF', 'PIM_NF', 'GA_NF', 'SA_NF', 'SV_NF', 'SO_NF', 'W_NF']]

# export
df_today.to_csv(
    wd + '/nhl/data/aggregate_projections.csv',
    index=False)

df_today[['Name', 'XGB']].to_csv(
    wd + '/nhl/data/fc_upload.csv',
    index=False)
