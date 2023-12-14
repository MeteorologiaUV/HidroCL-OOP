import os
import hidrocl
import pandas as pd
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

    downloaded_files = os.listdir(fpath)

    files = [val for val in files if not val.split('/')[-1] in downloaded_files]

    for file in files:
        try:
            hidrocl.download.download_imerg(file, fpath, 'hidrocl@meteo.uv.cl', 'hidrocl@meteo.uv.cl', timeout=120)
        except:
            print('Error downloading file: ', file)
            continue
