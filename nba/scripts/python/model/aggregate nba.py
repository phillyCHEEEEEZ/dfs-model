import csv
import datetime
import pandas as pd
import xlrd
import datetime

# datetime vars
now = datetime.datetime.now()
today = str(now.strftime('%Y-%m-%d'))
timestamp = str(now.strftime('_%Y-%m-%d_%H-%M-%S'))

# filename vars
data_dir = 'c:/dev/Python/Repos/dfs-model/nba/data/'
names_filename = 'master/names.xlsx'
fc_filename = 'fanduel_NBA_projections.csv'
rw_filename = 'rotowire-fanduel-NBA-players.csv'
bm_filename = 'basketball_monster_fanduel.csv'
nf_filename = 'numberfire_fanduel.csv'
dff_filename = 'dff_fanduel.csv'

# read CSVs
names_df = pd.read_excel(data_dir + names_filename)
fc_df = pd.read_csv(data_dir + fc_filename)
rw_df = pd.read_csv(data_dir + rw_filename)
bm_df = pd.read_csv(data_dir + bm_filename)
nf_df = pd.read_csv(data_dir + nf_filename)
dff_df = pd.read_csv(data_dir + dff_filename)

# create aggregate data frame
agg_df = fc_df

# clean up
agg_df = agg_df[['Player', 'Pos', 'Team', 'Opp', 'Salary', 'FC Proj']]

agg_df['Date'] = today

agg_df = agg_df[['Player', 'Pos', 'Team', 'Opp', 'Salary', 'Date', 'FC Proj']]

agg_df.columns = ['Player', 'Position', 'Team',
                  'Opponent', 'Salary', 'Date', 'FC']

agg_df['Opponent'] = agg_df['Opponent'].replace(regex=['@ '], value='')
agg_df['Opponent'] = agg_df['Opponent'].replace(regex=['vs '], value='')

# merge projections
agg_df = agg_df.merge(names_df[['FC', 'RW', 'BM', 'NF', 'DFF']],
                      left_on='Player', right_on='FC', how='left')

del agg_df['FC_y']

agg_df.rename(columns={'FC_x': 'FC'}, inplace=True)

# rotowire
agg_df = agg_df.merge(rw_df[['PLAYER', 'FPTS']],
                      left_on='Player', right_on='PLAYER', how='left')

agg_df['RW'] = agg_df['FPTS']

del agg_df['PLAYER']
del agg_df['FPTS']

# basketballmonster
try:
    agg_df = agg_df.merge(bm_df[['Player', 'Fpts']],
                          left_on='Player', right_on='Player', how='left')
except:
    agg_df = agg_df.merge(bm_df[['Name', 'Fpts']],
                          left_on='Player', right_on='Name', how='left')

agg_df['BM'] = agg_df['Fpts']

del agg_df['Name']
del agg_df['Fpts']

# numberfire
agg_df = agg_df.merge(nf_df[['Name', 'Projection']],
                      left_on='Player', right_on='Name', how='left')

agg_df['NF'] = agg_df['Projection']

del agg_df['Name']
del agg_df['Projection']

# daily fantasy fuel
agg_df = agg_df.merge(dff_df[['Name', 'Projection']],
                      left_on='Player', right_on='Name', how='left')

agg_df['DFF'] = agg_df['Projection']

del agg_df['Name']
del agg_df['Projection']

# average projections
agg_df['Avg'] = round(agg_df[['FC', 'RW', 'BM', 'NF', 'DFF']].mean(axis=1), 2)

# export full CSV and custom FC projections upload CSV
agg_df.to_csv(
    'c:/dev/Python/Repos/dfs-model/nba/data/aggregate_projections.csv',
    index=False)

agg_df[['Player', 'Avg']].to_csv(
    'c:/dev/Python/Repos/dfs-model/nba/data/fc_upload.csv',
    index=False)
