# coding=utf-8

import os
import sys
import time
import shutil
import hidrocl
from datetime import datetime
from hidrocl import paths as hcl

start = time.time()

#product_path = hcl.gfs
product_path = "/Users/aldotapia/Documents/GitHub/HidroCL-OOP/tests/gfs"

today = datetime.utcnow()
year = today.strftime('%Y')
today = today.strftime('%Y%m%d')
folder = f'{today}00'

today_folder = os.path.join(product_path, year, folder)

dates = hidrocl.download.list_gfs()

if not isinstance(dates, list):
    print("Error retrieving dates")
    sys.exit()

if today not in dates:
    print("Today's date is not available for download")
    sys.exit()


print(f'GFS download for {today}')

if not os.path.exists(today_folder):
    try:
        hidrocl.download.download_gfs(today, product_path)
        print('Download done')
    except ValueError:
        print("Today's date is not available for download")
elif len(os.listdir(today_folder)) < 6:
    print('Folder exists but is not complete, deleting and downloading again')
    shutil.rmtree(today_folder)
    try:
        hidrocl.download.download_gfs(today, product_path)
        print('Download done')
    except ValueError:
        print("Today's date is not available for download")
else:
    print(f'Folder {today_folder} and files already exists')

end = time.time()
print(f'Time elapsed: {end - start} seconds')