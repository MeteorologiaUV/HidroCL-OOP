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
product_path = '/Users/aldotapia/Documents/GitHub/HidroCL-OOP/tests/gfs_post2'
temp_files_folder = '/Users/aldotapia/Documents/GitHub/HidroCL-OOP/tests/gfs_temp'

dates = hidrocl.download.list_gfs()

if not isinstance(dates, list):
    print("Error retrieving dates")
    sys.exit()
    
for date in dates:
    try:
        hidrocl.download.download_gfs(date, product_path, temp_files_folder=temp_files_folder)
        print('Download done')
    except ValueError:
        print("Fail")

end = time.time()

print(f'Time elapsed: {end - start} seconds')
print(f'Dates downloaded: {len(dates)}')