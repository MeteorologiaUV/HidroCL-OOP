# coding=utf-8

import os
import re
import sys
import wget
import gzip
import time
import shutil
import ftplib
import cdsapi
import tarfile
import logging
import zipfile
import requests
import tempfile
import earthaccess
import pandas as pd
import xarray as xr
from . import tools as t
from pathlib import Path
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

    fname = os.path.join(path, f'era5-land_{year:04d}{month:02d}{day:02d}.zip')
    pth = os.path.join(path, f'era5-land_{year:04d}{month:02d}{day:02d}')
    fnameout = os.path.join(path, f'era5-land_{year:04d}{month:02d}{day:02d}.nc')

    dataset = 'reanalysis-era5-land'

    request = {
            'data_format': 'netcdf',
            'download_format': 'zip',
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

    with zipfile.ZipFile(fname, 'r') as zip_ref:
        zip_ref.extractall(pth)

    os.remove(fname)

    ds0 = xr.open_dataset(os.path.join(pth, 'data_0.nc'))
    ds1 = xr.open_dataset(os.path.join(pth, 'data_1.nc'))
    ds2 = xr.open_dataset(os.path.join(pth, 'data_2.nc'))

    ds = xr.merge([ds0, ds1, ds2], join='override')
    ds = ds.drop_vars(['number', 'expver'])
    ds.to_netcdf(fnameout)

    shutil.rmtree(pth)


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

    fname = os.path.join(path, f'era5_{year:04d}{month:02d}{day:02d}.zip')
    pth = os.path.join(path, f'era5_{year:04d}{month:02d}{day:02d}')
    fnameout = os.path.join(path, f'era5_{year:04d}{month:02d}{day:02d}.nc')

    dataset = 'reanalysis-era5-single-levels'

    request = {
            'data_format': 'netcdf',
            'download_format': 'zip',
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
    client.retrieve(dataset, request,fname)#.download()#, fname)

    with zipfile.ZipFile(fname, 'r') as zip_ref:
        zip_ref.extractall(pth)

    os.remove(fname)

    ds0 = xr.open_dataset(os.path.join(pth, 'data_stream-oper_stepType-instant.nc'))
    ds1 = xr.open_dataset(os.path.join(pth, 'data_stream-oper_stepType-accum.nc'))

    ds = xr.merge([ds0, ds1], join='override')
    ds = ds.drop_vars(['number', 'expver'])
    ds.to_netcdf(fnameout)

    shutil.rmtree(pth)

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

    baseurl = 'https://nomads.ncep.noaa.gov/gribfilter.php?ds=gfs_0p50'

    response = requests.get(baseurl)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        variables = soup.find_all('span', string=re.compile(r"^gfs\."))
        dates = [val.text.split('.')[1] for val in variables]
        dates = [f'{val[:4]}-{val[4:6]}-{val[6:]}' for val in dates]
        return dates
    else:
        print('Error: ', response.status_code)
        return response.status_code


def download_gfs(date, product_path, days=5, temp_files_folder=None):
    """
    Download a GFS product from NOMADS server using GRIB data access

    Examples:
        >>> download_gfs('2025-12-31', '/path/to/data')

    Args:
        date: date of the product in the format YYYY-MM-DD
        product_path: path to save the product

    Returns:
        None
    """

    hours = range(0, days * 24 + 3, 3)

    date_str = date.replace('-', '')

    vars = ['u10', 'v10', 'prate', 't2m', 'r2', 'gh']

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
    
    with tempfile.TemporaryDirectory() as tmpdir:
        if temp_files_folder is None:
            tmpdir = Path(tmpdir)
        else:
            tmpdir = Path(temp_files_folder)
        
        for hour in hours:
            url1 = f'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.{date_str}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f{hour:03d}&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&subregion=&toplat=-13&leftlon=-79&rightlon=-63&bottomlat=-61'
            url2 = f'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.{date_str}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f{hour:03d}&var_PRATE=on&lev_surface=on&subregion=&toplat=-13&leftlon=-79&rightlon=-63&bottomlat=-61'
            url3 = f'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.{date_str}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f{hour:03d}&var_RH=on&var_TMP=on&lev_2_m_above_ground=on&subregion=&toplat=-13&leftlon=-79&rightlon=-63&bottomlat=-61'
            url4 = f'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.{date_str}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f{hour:03d}&var_HGT=on&lev_0C_isotherm=on&subregion=&toplat=-13&leftlon=-79&rightlon=-63&bottomlat=-61'
    
            urls = [url1, url2, url3, url4]
            
            for i in range(4):
                response = requests.get(urls[i])
                
                if response.status_code != 200:
                    print(f'Failed to download from {urls[i]}. Status code: {response.status_code}')
                    sys.exit(3)

                path_name = tmpdir / f'gfs_part{i+1}_d{date_str}_f{hour:03d}.grb2'
                
                if path_name.exists():
                    print(f'File {path_name} already exists. Skipping download.')
                    continue
                with open(path_name, 'wb') as f:
                    f.write(response.content)
                print(f'Downloaded {path_name}')
                time.sleep(1)
        
        files = os.listdir(tmpdir)

        parts = []
    
        for k in range(1, 5):
            
            files_temp = [f for f in files if f.startswith(f'gfs_part{k}_d{date_str}')]
                
            files_temp = sorted(files_temp)
            files_temp = [f for f in files_temp if f.endswith('.grb2')]
        
            l = []
        
            for file in files_temp:
                if k == 2:            
                    ds_temp = xr.open_dataset(os.path.join(tmpdir, file), engine='cfgrib', 
                                                backend_kwargs={'filter_by_keys': {'stepType': 'instant'}})
                else:
                    ds_temp = xr.open_dataset(os.path.join(tmpdir, file), engine='cfgrib')
                l.append(ds_temp)
            
            ds_part = xr.concat(l, dim='valid_time')
            parts.append(ds_part)
        
        ds_gfs = xr.merge(parts, compat='override')
        
        ds_gfs = xr.merge(parts, compat='override')
        ds_gfs = ds_gfs.sortby(['valid_time', 'latitude', 'longitude'])
        
        ds_gfs = ds_gfs.drop_vars(['step', 'heightAboveGround', 'surface', 'isothermZero'])

        ds_gfs = ds_gfs.sel(latitude=slice(-61, -13), longitude=slice(281, 297),
                    valid_time=slice(ds_gfs.valid_time[0].values,
                                     ds_gfs.valid_time[0].values + pd.to_timedelta(24 * 5, unit='H')))
        
        ds_gfs = ds_gfs.assign_coords({'time': ds_gfs.valid_time.values[0]})

        date_name = date.replace('-', '') + '00'
        year = date.split('-')[0]
        
        if not os.path.exists(os.path.join(product_path, year)):
            os.makedirs(os.path.join(product_path, year))
        else:
            print(f'Folder {year} already exists')
        if not os.path.exists(os.path.join(product_path, year, date_name)):
            os.makedirs(os.path.join(product_path, year, date_name))
        else:
            print(f'Folder {date_name} already exists')
        
        for var in vars:
            name = f'GFS0.5_{var}_{leveltype.get(var)}_{steptype.get(var)}_{date_name}.nc'
            ds_gfs[var].to_netcdf(os.path.join(product_path, year, date_name, name))
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


def download_pdirnow(start, end, product_path, check_ppath=False):
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

    i = 0

    while i < 5:
        try:
            ftp = ftplib.FTP(ftp_server)
            ftp.login()
            ftp.cwd(ftp_path)
            break
        except:
            print('FTP connection failed. Trying again in 5 seconds...')
            time.sleep(5)
            i += 1
            continue

    if i == 5:
        print('FTP connection failed. Please try again later')
        return

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
