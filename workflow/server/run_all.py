import subprocess

import pandas as pd
import sys


today = pd.Timestamp.today().strftime('%Y%m%d%H%m%s')
log_folder = 'path/to/extraction_logs'

print('Starting run_all.py at', today)

"""
Codes:
    0: success
    1: error
    2: no data to process
    3: No new data to download, although it should be
    4: No new data to download, up to date
    5: Insufficient data to download and process
"""


def run_stuff(file):
    """
    Run stuff in bash

    Args:
        file: path to the file to be run

    Returns:
        code: code of the execution
    """
    try:
        code = subprocess.call(['python', file])
    except:
        sys.exit(1)
    if code == 3:
        sys.exit(1)
    return code


era51 = run_stuff('era5.py')
era52 = run_stuff('era5.py')
era5land1 = run_stuff('era5land.py')
era5land2 = run_stuff('era5land.py')
era5pl1 = run_stuff('era5pl.py')
era5pl2 = run_stuff('era5pl.py')
mcd15a2h1 = run_stuff('mcd15a2h.py')
mcd15a2h2 = run_stuff('mcd15a2h.py')
mod10a21 = run_stuff('mod10a2.py')
mod10a22 = run_stuff('mod10a2.py')
mod13q11 = run_stuff('mod13q1.py')
mod13q12 = run_stuff('mod13q1.py')
pdirnow1 = run_stuff('pdirnow.py')
pdirnow2 = run_stuff('pdirnow.py')
imerggis1 = run_stuff('imerggis.py')
imerggis2 = run_stuff('imerggis.py')
gfs1 = run_stuff('gfs.py')
gfs2 = run_stuff('gfs.py')

pd.DataFrame({'era5': [era51, era52],
              'era5land': [era5land1, era5land2],
              'era5pl': [era5pl1, era5pl2],
              'mcd15a2h': [mcd15a2h1, mcd15a2h2],
              'mod10a2': [mod10a21, mod10a22],
              'mod13q1': [mod13q11, mod13q12],
              'pdirnow': [pdirnow1, pdirnow2],
              'imerggis': [imerggis1, imerggis2],
              'gfs': [gfs1, gfs2]}).to_csv(f'{log_folder}/log_{today}.csv', index=False)
