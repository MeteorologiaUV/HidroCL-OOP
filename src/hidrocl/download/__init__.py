# coding=utf-8

import os
import wget
import gzip
import time
import shutil
import ftplib
import cdsapi
import tarfile
import logging
import requests
import earthaccess
import pandas as pd
import xarray as xr
from . import tools as t
from datetime import datetime
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth


def download_era5land(year, month, day, path, timeout=60, retry_max=10, sleep_max=120):
    """function to download era5-land reanalysis data from CDS

    This functions needs a .cdsapirc file in the home directory with the following content:
    url: https://cds.climate.copernicus.eu/api/v2
    key: <your key>

    Examples:
        >>> download_era5land(2000, 6, 1, '/path/to/data')

    Args:
        year (int): year of the data to be downloaded
        month (int): month of the data to be downloaded
        day (int): day of the data to be downloaded
        path (str):path to save the data
        timeout (int):

    Returns:
        None

    """

    fname = os.path.join(path, f'era5-land_{year:04d}{month:02d}{day:02d}.nc')

    dataset = 'reanalysis-era5-land'

    request = {
            'data_format': 'netcdf',
            'download_format': 'unarchived',
            'product_type': ['reanalysis'],
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
        }

    client = cdsapi.Client(timeout=timeout, retry_max=retry_max, sleep_max=sleep_max)
    client.retrieve(dataset, request, fname)


def download_era5(year, month, day, path):
    """function to download era5 reanalysis data from CDS

    This functions needs a .cdsapirc file in the home directory with the following content:
    url: https://cds.climate.copernicus.eu/api/v2
    key: <your key>

    Examples:
        >>> download_era5(2000, 6, 1, '/path/to/data')

    Args:
        year (int): year of the data to be downloaded
        month (int): month of the data to be downloaded
        day (int): day of the data to be downloaded
        path (str):path to save the data

    Returns:
        None

    """

    fname = os.path.join(path, f'era5_{year:04d}{month:02d}{day:02d}.nc')


    dataset = 'reanalysis-era5-single-levels'

    request = {
            'data_format': 'netcdf',
            'download_format': 'unarchived',
            'product_type': ['reanalysis'],
            'variable': [
                '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_dewpoint_temperature',
                '2m_temperature', 'surface_pressure', 'total_precipitation',
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
        }

    client = cdsapi.Client(retry_max=10)
    client.retrieve(dataset, request, fname)


def download_era5pressure(year, month, day, path):
    """function to download era5 pressure levels reanalysis data from CDS

    This functions needs a .cdsapirc file in the home directory with the following content:
    url: https://cds.climate.copernicus.eu/api/v2
    key: <your key>

    Examples:
        >>> download_era5pressure(2000, 6, 1, '/path/to/data')

    Args:
        year (int): year of the data to be downloaded
        month (int): month of the data to be downloaded
        day (int): day of the data to be downloaded
        path (str):path to save the data

    Returns:
        None

    """

    fname = os.path.join(path, f'era5-pressure_{year:04d}{month:02d}{day:02d}.nc')

    dataset = 'reanalysis-era5-pressure-levels'

    request = {
            'data_format': 'netcdf',
            'download_format': 'unarchived',
            'product_type': ['reanalysis'],
            'variable': ['geopotential'],
            'pressure_level': ['500'],
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
        }

    client = cdsapi.Client(retry_max=10)
    client.retrieve(dataset, request, fname)


def get_imerg(start, end, user, password, timeout=60):
    """function to get IMERG data filenames from jsimpsonhttps.pps.eosdis.nasa.gov

    Examples:
        >>> get_imerg('2000-06', '2000-07', 'user@doma.in', 'password')
        ['/imerg/gis/2000/06/3B-HHR-L.MS.MRG.3IMERG.20000608-S000000-E002959.0000.V06B.30min.tif',
         '/imerg/gis/2000/06/3B-HHR-L.MS.MRG.3IMERG.20000608-S003000-E005959.0030.V06B.30min.tif',
         ...]

    Args:
        start (str): start date in the format YYYY-MM
        end (str): start date in the format YYYY-MM
        user (str): username to access jsimpsonhttps.pps.eosdis.nasa.gov
        password (str): password to access jsimpsonhttps.pps.eosdis.nasa.gov
        timeout (int): timeout in seconds

    Returns:
        list: a list representing the filename of IMERG data available for the requested period

    Raises:
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


def download_imerg(url_extract, folder, user, password, timeout=60):
    """download IMERG data from jsimpsonhttps.pps.eosdis.nasa.gov.

    It is recommended to use the function get_imerg to get the filenames of the data to be downloaded

    Examples:
        >>> download_imerg('/imerg/gis/2000/06/xyz.tif', '/path/to/data',  'user@doma.in', 'password')
        xyz.tif downloaded

        >>> # for multiple files (natural process)
        >>> files = get_imerg('2000-06', '2000-07', 'user@doma.in', 'password')
        >>> for file in files:
        >>>     download_imerg(file, '/path/to/data',  'user@doma.in', 'password')
        xyz1.tif downloaded
        xyz2.tif downloaded
        ...

    Args:
        url_extract (str): extract of url in format '/imerg/gis/2000/06/xyz.tif'
        folder (str): folder to save the data
        user (str): username to access jsimpsonhttps.pps.eosdis.nasa.gov
        password (str): password to access jsimpsonhttps.pps.eosdis.nasa.gov
        timeout (int): timeout in seconds

    Returns:
        None
    """

    url = 'https://jsimpsonhttps.pps.eosdis.nasa.gov'+url_extract
    fname = url.split('/')[-1]

    response = requests.get(url, auth=HTTPBasicAuth(user, password), timeout=timeout)
    response.raise_for_status()

    with open(os.path.join(folder, fname), 'wb') as f:
        f.write(response.content)
        print(f'{fname} downloaded')


def list_gfs():
    """
    List the available GFS 0.5 products in nomads

    Examples:
        >>> list_gfs()

    Returns:
        list: a list of available GFS products or the status code if the request fails
    """

    baseurl = 'https://nomads.ncep.noaa.gov/dods/gfs_0p50'

    response = requests.get(baseurl)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        variables = soup.find_all('a')
        urls = [val.get('href') + '/gfs_0p50_00z' for val in variables if 'gfs_0p50/' in val.get('href')]
        return urls
    else:
        print('Error: ', response.status_code)
        return response.status_code


def download_gfs(url, product_path):
    """
    Download a GFS product from nomads

    Examples:
        >>> download_gfs('https://nomads.ncep.noaa.gov/dods/gfs_0p50/gfs20200601/gfs_0p50_00z', '/path/to/data')

    Args:
        url: url of the product
        product_path: path to save the product

    Returns:
        None
    """

    dic = {'ugrd10m': 'u10',
           'vgrd10m': 'v10',
           'pratesfc': 'prate',
           'tmp2m': 't2m',
           'rh2m': 'r2',
           'hgt0c': 'gh'}

    dims = {'time': 'valid_time',
            'lat': 'latitude',
            'lon': 'longitude'}

    dims.update(dic)

    leveltype = {'u10': 'heightAboveGround',
                 'v10': 'heightAboveGround',
                 'prate': 'surface',
                 't2m': 'heightAboveGround',
                 'r2': 'heightAboveGround',
                 'gh': 'isothermZero'}

    steptype = {'u10': 'instant',
                'v10': 'instant',
                'prate': 'avg',
                't2m': 'instant',
                'r2': 'instant',
                'gh': 'instant'}

    date = url.split('/')[-2].replace('gfs', '')
    year = date[:4]
    date = date + '00'

    if not os.path.exists(os.path.join(product_path, year)):
        os.makedirs(os.path.join(product_path, year))
    else:
        print(f'Folder {year} already exists')
    if not os.path.exists(os.path.join(product_path, year, date)):
        os.makedirs(os.path.join(product_path, year, date))
    else:
        print(f'Folder {date} already exists')

    logging.info(url)

    with t.HiddenPrints():
        ds = xr.open_dataset(url)

        ds = ds.sel(lev=500)[list(dic.keys())].drop('lev')
        ds = ds.rename(dims)
        ds = ds.sel(latitude=slice(-61, -13), longitude=slice(281, 297),
                    valid_time=slice(ds.valid_time[0].values,
                                     ds.valid_time[0].values + pd.to_timedelta(24 * 5, unit='H')))
        # create a new coordinate
        ds = ds.assign_coords({'time': ds.valid_time.values[0]})

        for var in dic.values():
            name = f'GFS0.5_{var}_{leveltype.get(var)}_{steptype.get(var)}_{date}.nc'
            ds[var].to_netcdf(os.path.join(product_path, year, date, name))
            print(f'{date} {var} saved')


def earthdata_download(what, product_path, start, end):
    """
    Download data from earthdata.nasa.gov

    Examples:
        >>> earthdata_download('reflectance', '/path/to/data', '2019-01-01', '2019-01-31')

    Args:
        what: one of the following: reflectance, vegetation, lai, albedo, lulc, et0, snow, precipitation, landdata
        product_path: path to save the downloaded files
        start: start date in format YYYY-MM-DD
        end: start date in format YYYY-MM-DD

    Returns:
        None

    """

    earthdata_products = {
        'reflectance': 'MOD09A1',
        'vegetation': 'MOD13Q1',
        'lai': 'MCD15A2H',
        'albedo': 'MCD43A3',
        'lulc': 'MCD12Q1',
        'et0': 'MOD16A2',
        'snow': 'MOD10A2',
        'precipitation': 'GPM_3IMERGHHL',
        'landdata': 'GLDAS_NOAH025_3H',
    }

    earthdata_platform = {
        'reflectance': 'modis',
        'vegetation': 'modis',
        'lai': 'modis',
        'albedo': 'modis',
        'lulc': 'modis',
        'et0': 'modis',
        'snow': 'modis',
        'precipitation': 'mixed',
        'landdata': 'model',
    }

    earthdata_version = {
        'reflectance': '061',
        'vegetation': '061',
        'lai': '061',
        'albedo': '061',
        'lulc': '061',
        'et0': '061',
        'snow': '61',
        'precipitation': '06',
        'landdata': '2.1',
    }

    earthdata_file_extension = {
        'reflectance': 'hdf',
        'vegetation': '.hdf',
        'lai': '.hdf',
        'albedo': '.hdf',
        'lulc': '.hdf',
        'et0': '.hdf',
        'snow': '.hdf',
        'precipitation': '.hdf5',
        'landdata': '.nc4',
    }

    try:
        what = what.lower()
    except AttributeError:
        raise ValueError("what must be a string")

    if what not in earthdata_products.keys():
        raise ValueError("what must be one of the following: reflectance, vegetation,",
                         "lai, albedo, lulc, et0, snow, precipitation, landdata")

    try:
        start = pd.to_datetime(start, format="%Y-%m-%d")
        end = pd.to_datetime(end, format="%Y-%m-%d")
    except ValueError:
        raise ValueError("start and end must be in format YYYY-MM-DD")

    if start > end:
        raise ValueError("start must be before end")

    grids = ['h13v14', 'h14v14', 'h12v13', 'h13v13', 'h11v12',
             'h12v12', 'h11v11', 'h12v11', 'h11v10']

    earthaccess.login()

    results = earthaccess.granule_query().short_name(earthdata_products[what]).\
        bounding_box(-73.73, -55.01, -67.05, -17.63).version(earthdata_version[what]).\
        temporal(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")).get_all()

    if len(results) == 0:
        print('No results found')
        return

    results = [value for value in results if any(substring in value.data_links()[0] for substring in grids)]

    if earthdata_platform[what] == 'modis':
        results = [value for value in results if any(substring in value.data_links()[0] for substring in grids)]

    downloaded_files = earthaccess.download(results,
                                            local_path=product_path)

    print('Downloaded finished')

def download_pdirnow(start, end, product_path, check_ppath = False):
    """
    Download PDIRNow data from CHRS FTP server.

    Args:
        start: start date in YYYY-MM-DD format
        end: end date in YYYY-MM-DD format
        product_path: path to the folder where the files will be downloaded
        check_ppath: if True, check the files in product_path and download only the missing ones (default: False).

    Returns:
        None
    """

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    ftp_server = 'persiann.eng.uci.edu'
    ftp_path = 'CHRSdata/PDIRNow/PDIRNowdaily'

    while True:
        try:
            ftp = ftplib.FTP(ftp_server)
            ftp.login()
            ftp.cwd(ftp_path)
            break
        except:
            print('FTP connection failed. Trying again in 5 seconds...')
            time.sleep(5)
            continue

    dir_list = []
    ftp.dir(dir_list.append)
    files_list = [value.split(' ')[-1] for value in dir_list if 'bin' in value]

    dates = [val.split('1d')[1].split('.')[0] for val in files_list]
    dates = [pd.to_datetime(val, format='%y%m%d') for val in dates]
    files_list = [files_list[i] for i in range(len(files_list)) if dates[i] >= start and dates[i] <= end]

    if check_ppath:
        files_list = [value for value in files_list if value.split('.gz')[0] not in os.listdir(product_path)]

    while True:
        try:
            for file_name in files_list:
                print(f'Downloading {file_name}')
                wget.download(f'ftp://{ftp_server}/{ftp_path}/{file_name}', out=product_path)
                print(f'Unzipping {file_name}')
                with gzip.open(f'{product_path}/{file_name}', 'rb') as f_in:
                    with open(f'{product_path}/{file_name.split(".gz")[0]}', 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(f'{product_path}/{file_name}')
            break
        except:
            print('FTP connection failed. Trying again in 5 seconds...')
            ftp.close()
            time.sleep(5)
            ftp = ftplib.FTP(ftp_server)
            ftp.login()
            ftp.cwd(ftp_path)
            continue
    ftp.close()
