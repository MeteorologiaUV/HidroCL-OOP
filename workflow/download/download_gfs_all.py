# coding=utf-8

import os
import shutil
import hidrocl
from datetime import datetime
from hidrocl import paths as hcl

product_path = hcl.gfs

urls = hidrocl.download.list_gfs()

for url in urls:
    date = url.split('/')[-2].replace('gfs', '')
    try:
        hidrocl.download.download_gfs(url, product_path)
        print('Download done')
    except ValueError:
        print("Fail")
