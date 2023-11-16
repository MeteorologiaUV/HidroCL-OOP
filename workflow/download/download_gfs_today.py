# coding=utf-8

import os
import shutil
import hidrocl
from datetime import datetime
from hidrocl import paths as hcl

product_path = hcl.gfs

today = datetime.utcnow()
year = today.strftime('%Y')
today = today.strftime('%Y%m%d')
folder = f'{today}00'

today_folder = os.path.join(product_path, year, folder)

urls = hidrocl.download.list_gfs()
dates = [val.split('/')[-2].replace('gfs', '') for val in urls]

print(f'GFS download for {today}')

if not os.path.exists(today_folder):
    try:
        pos = dates.index(today)
        hidrocl.download.download_gfs(urls[pos], product_path)
        print('Download done')
    except ValueError:
        print("Today's date is not available for download")
elif len(os.listdir(today_folder)) < 6:
    print('Folder exists but is not complete, deleting and downloading again')
    shutil.rmtree(today_folder)
    try:
        pos = dates.index(today)
        hidrocl.download.download_gfs(urls[pos], product_path)
        print('Download done')
    except ValueError:
        print("Today's date is not available for download")
else:
    print(f'Folder {today_folder} and files already exists')
