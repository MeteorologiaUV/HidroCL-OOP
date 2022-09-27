# coding=utf-8


import os
import hidrocl
import hidrocl_paths as hcl

files = os.listdir(hcl.satellite_soil_moisture)
files = list(set([file.split('-')[6][:8] for file in files]))

for year in range(2000, 2023):
    for month in range(1, 13):
        for day in range(1, 32):
            print(f'{year:04d}-{month:02d}-{day:02d}')

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
