import datetime
import os
import shutil

# datetime vars
now = datetime.datetime.now()
# now = now - datetime.timedelta(days=1)

today = str(now.strftime('%Y-%m-%d'))
timestamp = str(now.strftime('_%Y-%m-%d_%H-%M-%S'))


# working directory and archive directory
working_dir = 'c:/dev/Python/Repos/dfs-model/nba/data/'
archive_dir = 'c:/dev/Python/Repos/dfs-model/nba/data/archive/'

# folders
fc_folder = 'fantasy cruncher/'
rw_folder = 'rotowire/'
bm_folder = 'basketball monster/'
nf_folder = 'numberfire/'
dff_folder = 'daily fantasy fuel/'
agg_folder = 'aggregate/'


# archive function
def appendTimestampAndArchive(working_dir, archive_dir, folder, filename, extension, timestamp):
    src = working_dir + filename + '.' + extension
    dst = archive_dir + folder + filename + timestamp + '.' + extension
    shutil.copy(src, dst)
    os.remove(src)


# fantasycruncher
filename = 'fanduel_NBA_projections'
extension = 'csv'
appendTimestampAndArchive(working_dir, archive_dir, fc_folder,
                          filename, extension, timestamp)

# rotowire
filename = 'rotowire-fanduel-NBA-players'
extension = 'csv'
appendTimestampAndArchive(working_dir, archive_dir, rw_folder,
                          filename, extension, timestamp)

# basketball monster
filename = 'basketball_monster_fanduel'
extension = 'csv'
appendTimestampAndArchive(working_dir, archive_dir, bm_folder,
                          filename, extension, timestamp)

# numberfire
filename = 'numberfire_fanduel'
extension = 'csv'
appendTimestampAndArchive(working_dir, archive_dir, nf_folder,
                          filename, extension, timestamp)

# daily fantasy fuel
filename = 'dff_fanduel'
extension = 'csv'
appendTimestampAndArchive(working_dir, archive_dir, dff_folder,
                          filename, extension, timestamp)

# aggregate
filename = 'aggregate_projections'
extension = 'csv'
appendTimestampAndArchive(working_dir, archive_dir, agg_folder,
                          filename, extension, timestamp)

# fc upload
filename = 'fc_upload'
extension = 'csv'
appendTimestampAndArchive(working_dir, archive_dir, fc_folder,
                          filename, extension, timestamp)
