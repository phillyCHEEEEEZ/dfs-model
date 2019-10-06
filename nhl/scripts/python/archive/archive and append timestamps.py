import datetime
import os
import shutil

# datetime vars
now = datetime.datetime.now()
today = str(now.strftime('%Y-%m-%d'))
timestamp = str(now.strftime('_%Y-%m-%d_%H-%M-%S'))

# working directory and archive directory
working_dir = 'c:/dev/Python/Repos/dfs-model/nhl/data/'
archive_dir = 'c:/dev/Python/Repos/dfs-model/nhl/data/archive/'


# archive function
def appendTimestampAndArchive(working_dir, archive_dir, filename, extension, timestamp):
    src = working_dir + filename + '.' + extension
    dst = archive_dir + filename + timestamp + '.' + extension
    shutil.copy(src, dst)
    os.remove(src)


# fantasycruncher
filename = 'fanduel_NHL_' + today + '_players'
extension = 'csv'
appendTimestampAndArchive(working_dir, archive_dir,
                          filename, extension, timestamp)

# rotowire
filename = 'rotowire-fanduel-NHL-players'
extension = 'csv'
appendTimestampAndArchive(working_dir, archive_dir,
                          filename, extension, timestamp)

# numberfire
filename = 'numberfire_fanduel_all'
extension = 'csv'
appendTimestampAndArchive(working_dir, archive_dir,
                          filename, extension, timestamp)
