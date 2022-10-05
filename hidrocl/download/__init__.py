# coding=utf-8

import os
import cdsapi
import tarfile
import pandas as pd
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth


def download_era5land(year, month, day, path):
    """function to download era5-land reanalysis data from CDS

    This functions needs a .cdsapirc file in the home directory with the following content:
    url: https://cds.climate.copernicus.eu/api/v2
    key: <your key>

    Examples:
    ---------
        >>> download_era5land(2000, 6, 1, '/path/to/data')

    Args:
    ---------
        year (int): year of the data to be downloaded
        month (int): month of the data to be downloaded
        day (int): day of the data to be downloaded
        path (str):path to save the data

    Returns:
    ---------
        None

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


def get_imerg(start, end, user, password, timeout=60):
    """function to get IMERG data filenames from jsimpsonhttps.pps.eosdis.nasa.gov

    Examples:
    ---------
        >>> get_imerg('2000-06', '2000-07', 'user@doma.in', 'password')
    ['/imerg/gis/2000/06/3B-HHR-L.MS.MRG.3IMERG.20000608-S000000-E002959.0000.V06B.30min.tif', \n
     '/imerg/gis/2000/06/3B-HHR-L.MS.MRG.3IMERG.20000608-S003000-E005959.0030.V06B.30min.tif', \n
     ...]

    Args:
    ---------
        start (str): start date in the format YYYY-MM
        end (str): start date in the format YYYY-MM
        user (str): username to access jsimpsonhttps.pps.eosdis.nasa.gov
        password (str): password to access jsimpsonhttps.pps.eosdis.nasa.gov
        timeout (int): timeout in seconds

    Returns:
    ---------
        list: a list representing the filename of IMERG data available for the requested period

    Raises:
    ---------
        ValueError: if:
            - start or end are not in the format YYYY-MM
            - start is after end
            - start is less than 2000-06
    """

    start = pd.to_datetime(start+'-01', format="%Y-%m-%d")
    end = pd.to_datetime(end+'-01', format="%Y-%m-%d")

    if start > end:
        raise ValueError("start date should be less than end date")

    if start.year < 2000:
        raise ValueError("start date should be greater than 2000")

    if end.year > datetime.now().year:
        raise ValueError("end date should be less than current year")

    if start.year == 200 and start.month < 6:
        raise ValueError("start date should be greater than 2000-06-01")

    p = pd.period_range(start, end, freq='M')

    final_response = []

    for yyyymm in p:
        year = int(yyyymm.strftime('%Y'))
        month = int(yyyymm.strftime('%m'))

        url = f'https://jsimpsonhttps.pps.eosdis.nasa.gov/text/imerg/gis/{year:04d}/{month:02d}/'

        response = requests.get(url, auth=HTTPBasicAuth(user, password), timeout=timeout)

        vals = str(response.content).split('\\n')

        vals_filtered = [val for val in vals if '3B-HHR-L' in val and '30min.tif' in val]

        final_response.extend(vals_filtered)

    return final_response


def download_imerg(url_extract, folder, user, password, timeout = 60):
    """download IMERG data from jsimpsonhttps.pps.eosdis.nasa.gov.

    It is recommended to use the function get_imerg to get the filenames of the data to be downloaded

    Examples:
    ---------
        >>> download_imerg('/imerg/gis/2000/06/xyz.tif', '/path/to/data',  'user@doma.in', 'password')
    xyz.tif downloaded

        >>> # for multiple files (natural process)
        >>> files = get_imerg('2000-06', '2000-07', 'user@doma.in', 'password')
        >>> for file in files:
        >>>     download_imerg(file, '/path/to/data',  'user@doma.in', 'password')
    xyz1.tif downloaded \n
    xyz2.tif downloaded \n
    ...

    Args:
    ---------
        url_extract (str): extract of url in format '/imerg/gis/2000/06/xyz.tif'
        folder (str): folder to save the data
        user (str): username to access jsimpsonhttps.pps.eosdis.nasa.gov
        password (str): password to access jsimpsonhttps.pps.eosdis.nasa.gov
        timeout (int): timeout in seconds

    Returns:
    ---------
        None
    """

    url = 'https://jsimpsonhttps.pps.eosdis.nasa.gov'+url_extract
    fname = url.split('/')[-1]

    response = requests.get(url, auth=HTTPBasicAuth(user, password), timeout=timeout)
    response.raise_for_status()

    with open(os.path.join(folder, fname), 'wb') as f:
        f.write(response.content)
        print(f'{fname} downloaded')
