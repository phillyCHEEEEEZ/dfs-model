import csv
import datetime
import pandas as pd

# datetime vars
now = datetime.datetime.now()
today = str(now.strftime('%Y-%m-%d'))
timestamp = str(now.strftime('_%Y-%m-%d_%H-%M-%S'))

# filename vars
data_dir = 'c:/dev/Python/Repos/dfs-model/nhl/data/'
fc_filename = 'fanduel_NHL_' + today + '_players.csv'
rw_filename = 'rotowire-fanduel-NHL-players.csv'
nf_filename = 'numberfire_fanduel_skaters.csv'

# read CSVs
fc_df = pd.read_csv(data_dir + fc_filename)
rw_df = pd.read_csv(data_dir + rw_filename)
nf_df = pd.read_csv(data_dir + nf_filename)
