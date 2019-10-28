import time
import datetime
import os
import shutil
import pandas as pd

from datetime import date, timedelta

# datetime vars
now = datetime.datetime.now()
today = str(now.strftime('%Y-%m-%d'))
yesterday = (now - timedelta(days=1)).strftime('%Y-%m-%d')

# working directory and archive directory
wd = 'c:/dev/Python/Repos/dfs-model/nhl/data/'
ad = 'c:/dev/Python/Repos/dfs-model/nhl/data/archive/'
md = 'c:/dev/Python/Repos/dfs-model/nhl/data/master/'

# folders
agg_daily_folder = 'aggregate/'
fc_actual_folder = 'fantasy cruncher/'

# filenames
agg_master_filename = 'aggregate_projections_all.csv'
agg_daily_filename = 'aggregate_projections_' + yesterday + '.csv'
fc_actual_filename = 'fanduel_NHL_actual.csv'

# import data
agg_master_df = pd.read_csv(md + agg_master_filename)
agg_daily_df = pd.read_csv(ad + agg_daily_folder + agg_daily_filename)
fc_actual_df = pd.read_csv(wd + fc_actual_filename)

# merge actual results
agg_daily_df = agg_daily_df.merge(fc_actual_df[['Player', 'Actual Score']],
                                  left_on='Player', right_on='Player', how='left')

# clean up
agg_daily_df['Actual'] = agg_daily_df['Actual Score']
del agg_daily_df['Actual Score']

# append daily data to master
agg_master_df = agg_master_df.append(agg_daily_df, ignore_index=True)


# archive function
def appendDateAndArchive(working_dir, archive_dir, folder, filename, extension, date=''):
    src = wd + filename + '.' + extension
    dst = ad + folder + filename + date + '.' + extension
    shutil.copy(src, dst)
    os.remove(src)


# actual scores
filename = 'fanduel_NHL_actual'
extension = 'csv'
appendDateAndArchive(wd, ad, fc_actual_folder,
                     filename, extension, '_' + yesterday)

# remove NAs
agg_daily_df.dropna(subset=['Actual'], inplace=True)
agg_master_df.dropna(subset=['Actual'], inplace=True)

# export
agg_daily_df.to_csv(ad + agg_daily_folder + agg_daily_filename, index=False)
agg_master_df.to_csv(md + 'aggregate_projections_all.csv', index=False)
