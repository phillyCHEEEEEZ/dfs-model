import csv
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
rw_filename = 'rotowire-fanduel-NBA-all.csv'
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
agg_df['Date'] = today

agg_df = agg_df[['Player', 'Pos', 'Team', 'Opp', 'Salary', 'Date', 'FC Proj',
                 'Floor', 'Ceiling', 'FPPG', 'FPPM', 'AVG/36', 'STDV/36',
                 'STDV', 'ProjSTDV', 'USG', 'FGA', 'MPG', 'Proj Mins']]

agg_df.columns = ['Player', 'Position', 'Team', 'Opponent', 'Salary', 'Date',
                  'FC', 'Floor_FC', 'Ceiling_FC', 'FPPG_FC', 'FPPM_FC', 'AVG/36_FC',
                  'STDV/36_FC', 'STDV_FC', 'ProjSTDV_FC', 'USG_FC', 'FGA_FC',
                  'MPG_FC', 'Mins_FC']

agg_df['Opponent'] = agg_df['Opponent'].replace(regex=['@ '], value='')
agg_df['Opponent'] = agg_df['Opponent'].replace(regex=['vs '], value='')

# merge projections
agg_df = agg_df.merge(names_df[['FC', 'RW', 'BM', 'NF', 'DFF']],
                      left_on='Player', right_on='FC', how='left')

del agg_df['FC_y']

agg_df.rename(columns={'FC_x': 'FC'}, inplace=True)

agg_df = agg_df[['Player', 'Position', 'Team', 'Opponent', 'Salary', 'Date',
                 'FC', 'RW', 'BM', 'NF', 'DFF', 'Floor_FC', 'Ceiling_FC',
                 'FPPG_FC', 'FPPM_FC', 'AVG/36_FC', 'STDV/36_FC', 'STDV_FC',
                 'ProjSTDV_FC', 'USG_FC', 'FGA_FC', 'MPG_FC', 'Mins_FC']]

# rotowire
agg_df = agg_df.merge(rw_df[['PLAYER', 'FPTS', 'ML', 'O/U', 'SPRD', 'TM/P', 'L5 FPTS',
                             'AVG FPTS', 'CEIL', 'VAL', 'L5 VAL', 'AVG VAL', 'MINS',
                             'L5 MINS', 'AVG MINS', 'FPM', 'L5 FPM', 'AVG FPM', 'PTS',
                             'REB', 'AST', 'STL', 'BLK', 'TO', 'FGM', 'FGA', 'FG%', '3PM',
                             '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB']],
                      left_on='Player', right_on='PLAYER', how='left')

agg_df['RW'] = agg_df['FPTS']

del agg_df['PLAYER']
del agg_df['FPTS']

agg_df.columns = ['Player', 'Position', 'Team', 'Opponent', 'Salary', 'Date',
                  'FC', 'RW', 'BM', 'NF', 'DFF', 'Floor_FC', 'Ceiling_FC', 'FPPG_FC',
                  'FPPM_FC', 'AVG/36_FC', 'STDV/36_FC', 'STDV_FC', 'ProjSTDV_FC',
                  'USG_FC', 'FGA_FC', 'MPG_FC', 'Mins_FC', 'ML_RW', 'O/U_RW', 'SPRD_RW',
                  'TM/P_RW', 'L5_FPTS_RW', 'AVG_FPTS_RW', 'CEIL_RW', 'VAL_RW',
                  'L5_VAL_RW', 'AVG_VAL_RW', 'MINS_RW', 'L5_MINS_RW', 'AVG_MINS_RW',
                  'FPM_RW', 'L5_FPM_RW', 'AVG_FPM_RW', 'PTS_RW', 'REB_RW', 'AST_RW',
                  'STL_RW', 'BLK_RW', 'TO_RW', 'FGM_RW', 'FGA_RW', 'FG%_RW', '3PM_RW',
                  '3PA_RW', '3P%_RW', 'FTM_RW', 'FTA_RW', 'FT%_RW', 'OREB_RW', 'DREB_RW']

# basketballmonster
try:
    agg_df = agg_df.merge(bm_df[['Player', 'Fpts', 'minutes', 'points', 'threes',
                                 ' threes_attempted', 'rebounds', 'assists', 'steals',
                                 'blocks', 'turnovers', 'twos', 'free throws',
                                 'free_throws_missed', ' field goals', 'field_goals_missed',
                                 'double doubles', 'triple doubles', 'usage']],
                          left_on='Player', right_on='Player', how='left')
except:
    agg_df = agg_df.merge(bm_df[['Name', 'Fpts', 'minutes', 'points', 'threes',
                                 ' threes_attempted', 'rebounds', 'assists', 'steals',
                                 'blocks', 'turnovers', 'twos', 'free throws',
                                 'free_throws_missed', ' field goals', 'field_goals_missed',
                                 'double doubles', 'triple doubles', 'usage']],
                          left_on='Player', right_on='Name', how='left')

agg_df['BM'] = agg_df['Fpts']

del agg_df['Name']
del agg_df['Fpts']

agg_df.columns = ['Player', 'Position', 'Team', 'Opponent', 'Salary', 'Date',
                  'FC', 'RW', 'BM', 'NF', 'DFF', 'Floor_FC', 'Ceiling_FC', 'FPPG_FC',
                  'FPPM_FC', 'AVG/36_FC', 'STDV/36_FC', 'STDV_FC', 'ProjSTDV_FC',
                  'USG_FC', 'FGA_FC', 'MPG_FC', 'Mins_FC', 'ML_RW', 'O/U_RW', 'SPRD_RW',
                  'TM/P_RW', 'L5_FPTS_RW', 'AVG_FPTS_RW', 'CEIL_RW', 'VAL_RW',
                  'L5_VAL_RW', 'AVG_VAL_RW', 'MINS_RW', 'L5_MINS_RW', 'AVG_MINS_RW',
                  'FPM_RW', 'L5_FPM_RW', 'AVG_FPM_RW', 'PTS_RW', 'REB_RW', 'AST_RW',
                  'STL_RW', 'BLK_RW', 'TO_RW', 'FGM_RW', 'FGA_RW', 'FG%_RW', '3PM_RW',
                  '3PA_RW', '3P%_RW', 'FTM_RW', 'FTA_RW', 'FT%_RW', 'OREB_RW', 'DREB_RW',
                  'minutes_BBM', 'points_BBM', 'threes_BBM', 'threes_attempted_BBM',
                  'rebounds_BBM', 'assists_BBM', 'steals_BBM', 'blocks_BBM',
                  'turnovers_BBM', 'twos_BBM', 'free throws_BBM', 'free_throws_missed_BBM',
                  'field goals_BBM', 'field_goals_missed_BBM', 'double doubles_BBM',
                  'triple doubles_BBM', 'usage_BBM']

# numberfire
agg_df = agg_df.merge(nf_df[['Name', 'Projection', 'Minutes', 'Points', 'Rebounds',
                             'Assists', 'Steals', 'Blocks', 'Turnovers']],
                      left_on='Player', right_on='Name', how='left')

agg_df['NF'] = agg_df['Projection']

del agg_df['Name']
del agg_df['Projection']

agg_df.columns = ['Player', 'Position', 'Team', 'Opponent', 'Salary', 'Date',
                  'FC', 'RW', 'BM', 'NF', 'DFF', 'Floor_FC', 'Ceiling_FC', 'FPPG_FC',
                  'FPPM_FC', 'AVG/36_FC', 'STDV/36_FC', 'STDV_FC', 'ProjSTDV_FC',
                  'USG_FC', 'FGA_FC', 'MPG_FC', 'Mins_FC', 'ML_RW', 'O/U_RW', 'SPRD_RW',
                  'TM/P_RW', 'L5_FPTS_RW', 'AVG_FPTS_RW', 'CEIL_RW', 'VAL_RW',
                  'L5_VAL_RW', 'AVG_VAL_RW', 'MINS_RW', 'L5_MINS_RW', 'AVG_MINS_RW',
                  'FPM_RW', 'L5_FPM_RW', 'AVG_FPM_RW', 'PTS_RW', 'REB_RW', 'AST_RW',
                  'STL_RW', 'BLK_RW', 'TO_RW', 'FGM_RW', 'FGA_RW', 'FG%_RW', '3PM_RW',
                  '3PA_RW', '3P%_RW', 'FTM_RW', 'FTA_RW', 'FT%_RW', 'OREB_RW', 'DREB_RW',
                  'minutes_BBM', 'points_BBM', 'threes_BBM', 'threes_attempted_BBM',
                  'rebounds_BBM', 'assists_BBM', 'steals_BBM', 'blocks_BBM',
                  'turnovers_BBM', 'twos_BBM', 'free throws_BBM', 'free_throws_missed_BBM',
                  'field goals_BBM', 'field_goals_missed_BBM', 'double doubles_BBM',
                  'triple doubles_BBM', 'usage_BBM', 'Minutes_NF', 'Points_NF',
                  'Rebounds_NF', 'Assists_NF', 'Steals_NF', 'Blocks_NF', 'Turnovers_NF']

# daily fantasy fuel
agg_df = agg_df.merge(dff_df[['Name', 'Projection']],
                      left_on='Player', right_on='Name', how='left')

agg_df['DFF'] = agg_df['Projection']

del agg_df['Name']
del agg_df['Projection']

# average projections
agg_df['Avg'] = round(agg_df[['FC', 'RW', 'BM', 'NF', 'DFF']].mean(axis=1), 2)

# actual projections placeholder
agg_df['Actual'] = ""

# rename and reorder
agg_df = agg_df[['Player', 'Position', 'Team', 'Opponent', 'Salary', 'Date',
                 'FC', 'RW', 'BM', 'NF', 'DFF', 'Avg', 'Actual', 'Floor_FC',
                 'Ceiling_FC', 'FPPG_FC', 'FPPM_FC', 'AVG/36_FC', 'STDV/36_FC',
                 'STDV_FC', 'ProjSTDV_FC', 'USG_FC', 'FGA_FC', 'MPG_FC',
                 'Mins_FC', 'ML_RW', 'O/U_RW', 'SPRD_RW', 'TM/P_RW', 'L5_FPTS_RW',
                 'AVG_FPTS_RW', 'CEIL_RW', 'VAL_RW', 'L5_VAL_RW', 'AVG_VAL_RW',
                 'MINS_RW', 'L5_MINS_RW', 'AVG_MINS_RW', 'FPM_RW', 'L5_FPM_RW',
                 'AVG_FPM_RW', 'PTS_RW', 'REB_RW', 'AST_RW', 'STL_RW', 'BLK_RW',
                 'TO_RW', 'FGM_RW', 'FGA_RW', 'FG%_RW', '3PM_RW', '3PA_RW',
                 '3P%_RW', 'FTM_RW', 'FTA_RW', 'FT%_RW', 'OREB_RW', 'DREB_RW',
                 'minutes_BBM', 'points_BBM', 'threes_BBM', 'threes_attempted_BBM',
                 'rebounds_BBM', 'assists_BBM', 'steals_BBM', 'blocks_BBM',
                 'turnovers_BBM', 'twos_BBM', 'free throws_BBM', 'free_throws_missed_BBM',
                 'field goals_BBM', 'field_goals_missed_BBM', 'double doubles_BBM',
                 'triple doubles_BBM', 'usage_BBM', 'Minutes_NF', 'Points_NF',
                 'Rebounds_NF', 'Assists_NF', 'Steals_NF', 'Blocks_NF', 'Turnovers_NF']]

agg_df.columns = ['Name', 'Position', 'Team', 'Opponent', 'Salary', 'Date',
                  'FC', 'RW', 'BM', 'NF', 'DFF', 'Avg', 'Actual', 'Floor_FC',
                  'Ceiling_FC', 'FPPG_FC', 'FPPM_FC', 'AVG/36_FC', 'STDV/36_FC',
                  'STDV_FC', 'ProjSTDV_FC', 'USG_FC', 'FGA_FC', 'MPG_FC',
                  'Mins_FC', 'ML_RW', 'O/U_RW', 'SPRD_RW', 'TM/P_RW', 'L5_FPTS_RW',
                  'AVG_FPTS_RW', 'CEIL_RW', 'VAL_RW', 'L5_VAL_RW', 'AVG_VAL_RW',
                  'MINS_RW', 'L5_MINS_RW', 'AVG_MINS_RW', 'FPM_RW', 'L5_FPM_RW',
                  'AVG_FPM_RW', 'PTS_RW', 'REB_RW', 'AST_RW', 'STL_RW', 'BLK_RW',
                  'TO_RW', 'FGM_RW', 'FGA_RW', 'FG%_RW', '3PM_RW', '3PA_RW',
                  '3P%_RW', 'FTM_RW', 'FTA_RW', 'FT%_RW', 'OREB_RW', 'DREB_RW',
                  'minutes_BBM', 'points_BBM', 'threes_BBM', 'threes_attempted_BBM',
                  'rebounds_BBM', 'assists_BBM', 'steals_BBM', 'blocks_BBM',
                  'turnovers_BBM', 'twos_BBM', 'free throws_BBM', 'free_throws_missed_BBM',
                  'field goals_BBM', 'field_goals_missed_BBM', 'double doubles_BBM',
                  'triple doubles_BBM', 'usage_BBM', 'Minutes_NF', 'Points_NF',
                  'Rebounds_NF', 'Assists_NF', 'Steals_NF', 'Blocks_NF', 'Turnovers_NF']

# export full CSV and custom FC projections upload CSV
agg_df.to_csv(
    'c:/dev/Python/Repos/dfs-model/nba/data/aggregate_projections.csv',
    index=False)

# agg_df[['Player', 'Avg']].to_csv(
#     'c:/dev/Python/Repos/dfs-model/nba/data/fc_upload.csv',
#     index=False)
