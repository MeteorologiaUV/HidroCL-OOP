# coding=utf-8

import os
import sys
import time
import shutil
import hidrocl
from datetime import datetime
from hidrocl import paths as hcl
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as tempdirname:
    temp1 = Path(tempdirname)
    with TemporaryDirectory() as tempdirname:
        temp2 = Path(tempdirname)

        start = time.time()

        # product_path = hcl.gfs
        product_path = temp1
        temp_files_folder = temp2

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