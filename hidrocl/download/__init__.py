# coding=utf-8

import os
import cdsapi
import tarfile


def download_era5land(year, month, day, path):
    """function to download era5-land reanalysis data from CDS

    Parameters
    ----------
    year : int
        year of the data to be downloaded
    month : int
        month of the data to be downloaded
    day : int
        day of the data to be downloaded
    path : str
        path to save the data
    """

    fname = os.path.join(path, f'era5-land_{year:04d}{month:02d}{day:02d}.nc')

    c = cdsapi.Client()

    c.retrieve(
        'reanalysis-era5-land',
        {
            'format': 'netcdf',
            'variable': [
                '2m_temperature', 'potential_evaporation', 'snow_albedo',
                'snow_cover', 'snow_density', 'snow_depth',
                'snow_depth_water_equivalent', 'total_evaporation', 'total_precipitation',
                'volumetric_soil_water_layer_1', 'volumetric_soil_water_layer_2', 'volumetric_soil_water_layer_3',
                'volumetric_soil_water_layer_4',
            ],
            'month': [
                str(month).zfill(2),
            ],
            'day': [
                str(day).zfill(2),
            ],
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
            'year': [
                str(year).zfill(4),
            ],
            'area': [
                -15, -75, -55,
                -65,
            ],
        },
        fname)


def download_satsoilmoist(year, month, day, path):
    """function to download Soil moisture gridded data from CDS

    Parameters
    ----------
    year : int
        year of the data to be downloaded
    month : int
        month of the data to be downloaded
    day : int
        day of the data to be downloaded
    path : str
        path to save the data
    """

    c = cdsapi.Client()

    c.retrieve(
        'satellite-soil-moisture',
        {
            'format': 'tgz',
            'variable': 'volumetric_surface_soil_moisture',
            'type_of_sensor': [
                'combined_passive_and_active', 'passive',
            ],
            'time_aggregation': 'day_average',
            'month': str(month).zfill(2),
            'year': str(year).zfill(4),
            'day': str(day).zfill(2),
            'type_of_record': 'cdr',
            'version': 'v202012.0.0',
        },
        'download.tar.gz')

    with tarfile.open('download.tar.gz') as tar:
        tar.extractall(path=path)

    os.remove('download.tar.gz')
