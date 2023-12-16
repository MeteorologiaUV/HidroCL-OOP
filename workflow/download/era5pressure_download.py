# coding=utf-8


import os
import hidrocl
import pandas as pd
from pathlib import Path
import hidrocl.paths as hcl

product_path = hcl.era5_pressure_levels_hourly_path
files = os.listdir(product_path)

start = '2022-01-01'
end = '2024-01-01'

p = pd.period_range(pd.to_datetime(start, format="%Y-%m-%d"),
                    pd.to_datetime(end, format="%Y-%m-%d"), freq='D')

for i in p:
    print(i)

    year = int(i.strftime('%Y'))
    month = int(i.strftime('%m'))
    day = int(i.strftime('%d'))

    fname = f'era5-pressure_{year:04d}{month:02d}{day:02d}.nc'
    file = Path(os.path.join(product_path, f'{year:04d}', fname))

    if file.is_file():
        print('already downloaded')
    else:
        try:
            print('downloading')
            hidrocl.download.download_era5pressure(year=year,
                                                   month=month,
                                                   day=day,
                                                   path=product_path)
        except Exception:
            print('day out of range')
