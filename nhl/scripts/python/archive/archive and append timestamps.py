import datetime
import os
import shutil

# datetime vars
now = datetime.datetime.now()
today = str(now.strftime('%Y-%m-%d'))
timestamp = str(now.strftime('_%Y-%m-%d_%H-%M-%S'))

# datetime adjust
# now = now - datetime.timedelta(days=1)

# working directory and archive directory
working_dir = 'c:/dev/Python/Repos/dfs-model/nhl/data/'
archive_dir = 'c:/dev/Python/Repos/dfs-model/nhl/data/archive/'

# folders
fc_folder = 'fantasy cruncher/'
rw_folder = 'rotowire/'
nf_folder = 'numberfire/'
agg_folder = 'aggregate/'


# archive function
def appendTimestampAndArchive(working_dir, archive_dir, folder, filename, extension, timestamp):
    src = working_dir + filename + '.' + extension
    dst = archive_dir + folder + filename + timestamp + '.' + extension
    shutil.copy(src, dst)
    os.remove(src)


# fantasycruncher
filename = 'fanduel_NHL_' + today + '_players'
extension = 'csv'
appendTimestampAndArchive(working_dir, archive_dir, fc_folder,
                          filename, extension, timestamp)

# rotowire
filename = 'rotowire-fanduel-NHL-players'
extension = 'csv'
appendTimestampAndArchive(working_dir, archive_dir, rw_folder,
                          filename, extension, timestamp)

# numberfire
filename = 'numberfire_fanduel_all'
extension = 'csv'
appendTimestampAndArchive(working_dir, archive_dir, nf_folder,
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
