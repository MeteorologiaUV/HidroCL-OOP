# coding=utf-8


import os
import hidrocl
import hidrocl_paths as hcl

files = os.listdir(hcl.era5_land_hourly_path)

for year in range(2000, 2023):
    for month in range(1, 13):
        for day in range(1, 32):
            print(f'{year:04d}-{month:02d}-{day:02d}')

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
