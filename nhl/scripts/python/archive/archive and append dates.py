import datetime
import os
import shutil

# datetime vars
now = datetime.datetime.now()
# now = now - datetime.timedelta(days=1)

today = str(now.strftime('%Y-%m-%d'))
timestamp = str(now.strftime('_%Y-%m-%d_%H-%M-%S'))

# working directory and archive directory
wd = 'c:/dev/Python/Repos/dfs-model/nhl/data/'
ad = 'c:/dev/Python/Repos/dfs-model/nhl/data/archive/'

# folders
fc_folder = 'fantasy cruncher/'
rw_folder = 'rotowire/'
nf_folder = 'numberfire/'
dff_folder = 'daily fantasy fuel/'
agg_folder = 'aggregate/'


# archive function
def appendDateAndArchive(working_dir, archive_dir, folder, filename, extension, date=''):
    src = wd + filename + '.' + extension
    dst = ad + folder + filename + date + '.' + extension
    shutil.copy(src, dst)
    os.remove(src)


# fantasycruncher
filename = 'fanduel_NHL_projections'
extension = 'csv'
appendDateAndArchive(wd, ad, fc_folder,
                     filename, extension, '_' + today)

# fc upload
filename = 'fc_upload'
extension = 'csv'
appendDateAndArchive(wd, ad, fc_folder,
                     filename, extension, '_' + today)

# rotowire
filename = 'rotowire-fanduel-NHL-all'
extension = 'csv'
appendDateAndArchive(wd, ad, rw_folder,
                     filename, extension, '_' + today)

# numberfire
filename = 'numberfire_fanduel_all'
extension = 'csv'
appendDateAndArchive(wd, ad, nf_folder,
                     filename, extension, '_' + today)

# daily fantasy fuel
filename = 'dff_fanduel_all'
extension = 'csv'
appendDateAndArchive(wd, ad, dff_folder,
                     filename, extension, '_' + today)

# aggregate
filename = 'aggregate_projections'
extension = 'csv'
appendDateAndArchive(wd, ad, agg_folder,
                     filename, extension, '_' + today)
