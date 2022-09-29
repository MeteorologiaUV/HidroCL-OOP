# coding=utf-8


import os
import hidrocl
import pandas as pd
import hidrocl_paths as hcl

files = os.listdir(hcl.satellite_soil_moisture)
files = list(set([file.split('-')[6][:8] for file in files]))

start = '2000-01-01'
end = '2022-10-01'

p = pd.period_range(pd.to_datetime(start, format="%Y-%m-%d"),
                    pd.to_datetime(end, format="%Y-%m-%d"), freq='D')

for i in p:
    print(i)

    year = int(i.strftime('%Y'))
    month = int(i.strftime('%m'))
    day = int(i.strftime('%d'))

    fname = f'{year:04d}{month:02d}{day:02d}'

    if fname in files:
        print('already downloaded')
    else:
        try:
            print('downloading')
            hidrocl.download.download_satsoilmoist(year=year,
                                                   month=month,
                                                   day=day,
                                                   path=hcl.satellite_soil_moisture)
        except Exception:
            print('day out of range')
