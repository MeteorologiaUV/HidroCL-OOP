
import os
import hidrocl
import pandas as pd
from pathlib import Path
import hidrocl.paths as hcl

fpath = hcl.imerggis_path

start = '2022-01-01'
end = '2024-10-01'

period = pd.period_range(pd.to_datetime(start, format="%Y-%m-%d"),
                         pd.to_datetime(end, format="%Y-%m-%d"), freq='M')

for date in period:
    try:
        files = hidrocl.download.get_imerg(str(date), str(date), 'hidrocl@meteo.uv.cl',
                                           'hidrocl@meteo.uv.cl', timeout=120)
    except:
        continue

    for file in files:

        year = file.split('/')[-1].split('.')[4][:4]
        ffile = Path(os.path.join(fpath, year, file.split('/')[-1]))

        if ffile.is_file():
            print('already downloaded')
        else:
            try:
                hidrocl.download.download_imerg(file, fpath, 'hidrocl@meteo.uv.cl', 'hidrocl@meteo.uv.cl', timeout=120)
            except:
                print('Error downloading file: ', file)
                continue
