# coding=utf-8


import os
import hidrocl
import pandas as pd
import hidrocl_paths as hcl

files = os.listdir(hcl.era5_land_hourly_path)

start = '2000-01-01'
end = '2022-10-01'

p = pd.period_range(pd.to_datetime(start, format="%Y-%m-%d"),
                    pd.to_datetime(end, format="%Y-%m-%d"), freq='D')

for i in p:
    print(i)

    year = int(i.strftime('%Y'))
    month = int(i.strftime('%m'))
    day = int(i.strftime('%d'))

    fname = f'era5-land_{year:04d}{month:02d}{day:02d}.nc'
    if fname in files:
        print('already downloaded')
    else:
        try:
            print('downloading')
            hidrocl.download.download_era5land(year=year,
                                               month=month,
                                               day=day,
                                               path=hcl.era5_land_hourly_path)
        except Exception:
            print('day out of range')
