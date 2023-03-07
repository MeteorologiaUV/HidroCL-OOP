# coding=utf-8

import os
import gc
import re
import csv
import time
import xarray
import subprocess
import numpy as np
import pandas as pd
from math import ceil
from array import array
from . import tools as t
from sys import platform
import rioxarray as rioxr
from datetime import datetime
from rasterio import errors as rioe
from rioxarray import exceptions as rxre
from rioxarray.merge import merge_arrays

if platform == "linux" or platform == "linux2":
    rscript = "Rscript"
elif platform == "darwin":
    rscript = "RScript"


# elif platform == "win32":
# Windows...


def load_hdf5(file, var):
    """
    Load .HDF5 file with xarray library and slice ver continental Chile

    Args:
        file (str): file path
        var (str): variable to extract

    Returns:
        xarray.DataArray: variable data
    """

    with t.HiddenPrints():
        da = rioxr.open_rasterio(file, engine='h5netcdf')
        da = da[0][var]
        return da.assign_coords({"x": (da.x / 10) - 90}) \
            .assign_coords({"y": (da.y / 10) - 180}) \
            .sel(x=slice(-55, -15), y=slice(-75, -65)) \
            .transpose('band', 'x', 'y') \
            .rio.write_crs(4326) \
            .rename({'x': 'y', 'y': 'x'})


def load_nc(file, var):
    """
    Load .nc files from GLDAS product

    Args:
        file (str): file path
        var (str): variable to extract

    Returns:
        xarray.DataArray: xarray DataArray
    """

    with t.HiddenPrints():
        da = xarray.open_dataset(file, engine="netcdf4")
        da = da[var]
        return da.sel(lat=slice(-55, -15), lon=slice(-75, -65))


def load_era5(file, var, reducer='mean'):
    """
    Load .nc files from ERA5 product

    Args:
        file (str): file path
        var (str): variable to extract
        reducer (str): reducer to use

    Returns:
        xarray.DataArray: xarray.DataArray with the variable
    """

    with t.HiddenPrints():
        da = xarray.open_dataset(file, mask_and_scale=True)
        da = da[var]
        match var:
            case 'tp':
                return da.sel(time=da.time.values[-1])
        match reducer:
            case 'mean':
                da = da.mean(dim='time')
            case 'sum':
                da = da.sum(dim='time')
            case 'min':
                da = da.min(dim='time')
            case 'max':
                da = da.max(dim='time')
            case _:
                raise ValueError("Reducer not supported")
        match var:
            case 't2m':
                da = da - 273.15
            case _:
                pass
        return da


def load_persiann(file):
    """
    Load .bin persiann files

    Args:
        file (str): file path

    Returns:
        xarray.DataArray: xarray.DataArray with the variable
    """
    with t.HiddenPrints():
        da = open(file, 'rb')

        nlon = 9000
        nlat = 3000
        flon = 0.02
        slon = 0.04
        llon = 359.99
        flat = 59.98  # N
        slat = -0.04
        llat = -59.99  # S

        lon = np.arange(flon, llon, slon)
        lat = np.arange(flat, llat, slat)

        bytesize = 4
        overhead = 0
        recl = (nlon * nlat + overhead) * bytesize

        tmp = array('f', da.read(recl))

        data = np.reshape(tmp, (nlat, nlon))
        data[data < -1000] = np.nan

        persiann = xarray.DataArray(data,
                                    coords={'lat': lat,
                                            'lon': lon},
                                    dims=['lat', 'lon'],
                                    attrs=dict(
                                        description='Precipitation',
                                        units='mm'
                                    ))

        persiann.coords['lon'] = (persiann.coords['lon'] + 180) % 360 - 180
        return persiann.sortby(persiann.lon)\
            .sortby(persiann.lat).sel(lat=slice(-55, -15), lon=slice(-75, -65))\
            .rename({'lon': 'x', 'lat': 'y'})


def load_gfs(file, var, day=0):
    """
    Load .nc files from GFS product

    Args:
        file (str): file path
        var (str): variable to extract
        day (int): day to extract

    Returns:
        xarray.DataArray: xarray.DataArray with the variable
    """

    with t.HiddenPrints():
        da = xarray.open_dataset(file, mask_and_scale=True)
        da = da[var]
        da.load()
        da = da.sel(valid_time=slice(da.time+pd.to_timedelta(24*day, unit='H'),
                                     da.time+pd.to_timedelta(24*day + 23, unit='H')))\
            .transpose('valid_time', 'latitude', 'longitude')
        da.coords['longitude'] = (da.coords['longitude'] + 180) % 360 - 180
        return da


def load_imerggis(file, nodata=29999):
    """
    Load .tif files from IMERG product

    Args:
        file (str): file path
        nodata (int, float): nodata value

    Returns:
        xarray.DataArray: xarray.DataArray with the variable
    """

    with t.HiddenPrints():
        da = rioxr.open_rasterio(file)
        da = da.sel(x=slice(-75, -65), y=slice(-15, -55))
        return da.where(da != nodata)


def sum_datasets(dataset_list):
    """
    Function to sum xarray datasets

    Args:
        dataset_list (list): list of xarray datasets

    Returns:
        xarray.Dataset: xarray dataset with the sum of the datasets
    """
    template = dataset_list[0].copy()
    sum_values = sum([d.values for d in dataset_list])
    template.values = sum_values
    return template


def mean_datasets(dataset_list):
    """
    Function to get mean from xarray datasets

    Args:
        dataset_list (list): list of xarray datasets

    Returns:
        xarray.Dataset: xarray dataset with the mean of the datasets
    """
    template = dataset_list[0].copy()
    mean_values = np.mean([d.values for d in dataset_list], axis=0)
    template.values = mean_values
    return template


def max_datasets(dataset_list):
    """
    Function to get max from xarray datasets

    Args:
        dataset_list (list): list of xarray datasets

    Returns:
        xarray.Dataset: xarray dataset with the max of the datasets
    """
    template = dataset_list[0].copy()
    max_values = np.max([d.values for d in dataset_list], axis=0)
    template.values = max_values
    return template


def min_datasets(dataset_list):
    """
    Function to get min from xarray datasets

    Args:
        dataset_list (list): list of xarray datasets

    Returns:
        xarray.Dataset: xarray dataset with the min of the datasets
    """
    template = dataset_list[0].copy()
    min_values = np.min([d.values for d in dataset_list], axis=0)
    template.values = min_values
    return template


def mosaic_raster(raster_list, layer):
    """
    Function to compute mosaic files with rioxarray library

    Args:
        raster_list (list): list of raster files
        layer (str): layer to mosaic

    Returns:
        xarray.DataArray: xarray DataArray with the mosaic
    """
    raster_single = []

    for raster in raster_list:
        with rioxr.open_rasterio(raster, masked=True) as src:
            #raster_single.append(getattr(src, layer))
            raster_single.append(src[layer])

    raster_mosaic = merge_arrays(raster_single)
    return raster_mosaic


def mosaic_nd_raster(raster_list, layer1, layer2):
    """
    Function to compute normalized difference and mosaic files with rioxarray library.
    The normalized difference is computed as:
    normalized_difference = 1000 * (layer1 - layer2) / (layer1 + layer2)

    Args:
        raster_list (list): list of raster files
        layer1 (str): layer to mosaic
        layer2 (str): layer to mosaic

    Returns:
        xarray.DataArray: xarray DataArray with the mosaic
    """
    raster_single = []

    for raster in raster_list:
        with rioxr.open_rasterio(raster, masked=True) as src:
            lyr1 = getattr(src, layer1)
            lyr2 = getattr(src, layer2)
            nd = 1000 * (lyr1 - lyr2) / (lyr1 + lyr2)
            nd.rio.set_nodata(-32768)
            raster_single.append(nd)
    raster_mosaic = merge_arrays(raster_single)
    raster_mosaic = raster_mosaic.where((raster_mosaic <= 1000) & (raster_mosaic >= -1000))
    raster_mosaic = raster_mosaic.where(raster_mosaic != raster_mosaic.rio.nodata)
    return raster_mosaic


def write_line(database, result, catchment_names, file_id, file_date, ncol=1):
    """
    Write line to database

    Args:
        database (str): database path
        result (str): result path
        catchment_names (list): list of catchment names
        file_id (str): file id
        file_date (str): file date
        ncol (int): number of columns

    Returns:
        None
    """
    with open(result) as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        gauge_id_result = []
        value_result = []
        for row in csvreader:
            gauge_id_result.append(row[0])
            value_result.append(row[ncol])
    gauge_id_result = [value for value in gauge_id_result[1:]]
    value_result = [str(ceil(float(value))) if
                    value.replace('.', '', 1).lstrip("-").isdigit() else
                    'NA' for value in
                    value_result[1:] if value]

    if catchment_names == gauge_id_result:
        value_result.insert(0, file_id)
        value_result.insert(1, file_date)
        data_line = ','.join(value_result) + '\n'
        with open(database, 'a') as the_file:
            the_file.write(data_line)
    else:
        print('Inconsistencies with gauge ids!')


def write_log(log_file, file_id, currenttime, time_dif, database):
    """
    Write log file

    Args:
        log_file (str): log file path
        file_id (str): file id
        currenttime (str): current time
        time_dif (str): time difference
        database (str): database path

    Returns:
        None
    """
    with open(log_file, 'a') as txt_file:
        txt_file.write(f'ID {file_id}. Date: {currenttime}. Process time: {time_dif} s. Database: {database}. \n')


def zonal_stats(scene, scenes_path, tempfolder, name,
                catchment_names, log_file, **kwargs):
    """
    Function to extract zonal statistics from raster files

    Args:
        scene (str): scene name
        scenes_path (str): path where scenes are
        tempfolder (str): temporary folder path
        name (str): product name
        catchment_names (list): catchment names
        log_file (str): log file path
        **kwargs: additional arguments

    Keyword Args:
        database (str): Database path
        pcdatabase (str): pcdatabase path
        north_database (str): North database path
        south_database (str): South database path
        north_pcdatabase (str): North pcdatabase path
        south_pcdatabase (str): South pcdatabase path
        vector_path (str): vector path
        north_vector_path (str): north vector path
        south_vector_path (str): south vector path
        layer (Union[str,list]): with layer/layers to extract
        *** Add GFS kwargs ***
        gfs_path (str): GFS path
    Returns:
        Print
    """

    print(f'Processing scene {scene} for {name}')
    r = re.compile('.*' + str(scene) + '.*')
    selected_files = list(filter(r.match, scenes_path))
    start = time.time()
    match name:
        case "imerg":
            file_date = datetime.strptime(scene, '%Y%m%d').strftime('%Y-%m-%d')
        case "imgis":
            file_date = datetime.strptime(scene, '%Y%m%d').strftime('%Y-%m-%d')
        case name if "gldas" in name:
            file_date = datetime.strptime(scene, 'A%Y%m%d').strftime('%Y-%m-%d')
        case "persiann_ccs":
            file_date = datetime.strptime(scene, '%y%j').strftime('%Y-%m-%d')
        case "persiann_ccs_cdr":
            file_date = datetime.strptime(scene, '%y%m%d').strftime('%Y-%m-%d')
        case "pdirnow":
            file_date = datetime.strptime(scene, '%y%m%d').strftime('%Y-%m-%d')
        case name if "era5" in name:
            file_date = datetime.strptime(scene, '%Y%m%d').strftime('%Y-%m-%d')
        case "gfs":
            file_date = datetime.strptime(scene, '%Y%m%d%H').strftime('%Y-%m-%d')
        case _:
            file_date = datetime.strptime(scene, 'A%Y%j').strftime('%Y-%m-%d')

    match name:
        case 'nbr':
            if isinstance(kwargs.get("layer"), list):
                lyrs = kwargs.get("layer")
                try:
                    mos = mosaic_nd_raster(selected_files, lyrs[0], lyrs[1])
                except (rxre.RioXarrayError, rioe.RasterioIOError):
                    return print(f"Error in scene {scene}")
            else:
                "layer argument must be a list"

        case 'snow':
            try:
                mos = mosaic_raster(selected_files, kwargs.get("layer"))
                mos = (mos.where(mos == 200) / 200).fillna(0)
            except (rxre.RioXarrayError, rioe.RasterioIOError):
                return print(f"Error in scene {scene}")

        case 'et':
            try:
                mos = mosaic_raster(selected_files, kwargs.get("layer"))
                mos = mos.where(mos < 3200)
                mos = mos * 10
            except (rxre.RioXarrayError, rioe.RasterioIOError):
                return print(f"Error in scene {scene}")

        case 'imerg':
            try:
                datasets_list = [load_hdf5(ds, kwargs.get("layer")) for ds in selected_files]
                mos = sum_datasets(datasets_list)
            except OSError:
                return print(f"Error in scene {scene}")

        case 'imgis':
            try:
                datasets_list = [load_imerggis(ds) for ds in selected_files]
                mos = sum_datasets(datasets_list)
            except (rxre.RioXarrayError, rioe.RasterioIOError, ValueError):
                return print(f"Error in scene {scene}")

        case 'gfs':
            try:
                days = kwargs.get("days")
                mos_list = []
                for i in range(0,5):
                    if i in days:
                        dataset = load_gfs(selected_files[0], kwargs.get("layer"), day=i)
                        if kwargs.get("aggregation") == "sum":
                            mos_pre = sum_datasets(dataset)
                        elif kwargs.get("aggregation") == "mean":
                            mos_pre = mean_datasets(dataset)
                        elif kwargs.get("aggregation") == "max":
                            mos_pre = max_datasets(dataset)
                        elif kwargs.get("aggregation") == "min":
                            mos_pre = min_datasets(dataset)
                        else:
                            print("aggregation argument must be sum, mean, min or max, and it's needed")
                            return None
                        # scale and unit conversions
                        if kwargs.get("layer") == 'prate':
                            mos_pre = mos_pre * 3600 * 30
                        if kwargs.get("layer") == 'gh':
                            pass
                        if kwargs.get("layer") == 't2m':
                            mos_pre = (mos_pre - 273.15)*10
                        else:
                            mos_pre = mos_pre * 10
                        mos_list.append(mos_pre)
                mos = xarray.Dataset()

                for i in range(0, len(mos_list)):
                    mos[f"day_{i}"] = mos_list[i]

            except (rxre.RioXarrayError, rioe.RasterioIOError, ValueError, IndexError, KeyError):
                return print(f"Error in scene {scene}")

        case name if "gldas" in name:
            match name:
                case name if ("snow" in name) or ("temp" in name) or ("et" in name):
                    if isinstance(kwargs.get("layer"), str):
                        try:
                            datasets_list = [load_nc(ds, kwargs.get("layer")) for ds in selected_files]
                            mos = mean_datasets(datasets_list)
                            mos = mos * 100
                        except OSError:
                            return print(f"Error in scene {scene}")
                    else:
                        return print("layer argument must be a string")

                case name if "soilm" in name:
                    if isinstance(kwargs.get("layer"), list):
                        lyrs = kwargs.get("layer")
                        try:
                            layers_list = []
                            for lyr in lyrs:
                                datasets_list = [load_nc(ds, lyr) for ds in selected_files]
                                layers_list.append(mean_datasets(datasets_list))
                            mos = sum_datasets(layers_list)
                            mos = mos * 100
                        except OSError:
                            return print(f"Error in scene {scene}")
                    else:
                        return print("layer argument must be a list")
        case name if "era5" in name:
            match name:
                case name if "temp" in name:
                    if isinstance(kwargs.get("layer"), str):
                        try:
                            file = selected_files[0]
                            mos = load_era5(file, kwargs.get("layer"), kwargs.get("aggregation"))
                            mos = mos * 10
                        except (OSError, ValueError):
                            return print(f"Error in scene {scene}")
                case name if ("et" in name) or ("pp" in name):
                    if isinstance(kwargs.get("layer"), str):
                        try:
                            file = selected_files[0]
                            mos = load_era5(file, kwargs.get("layer"), "sum")
                            mos = mos * 10000
                        except (OSError, ValueError):
                            return print(f"Error in scene {scene}")
                case name if "snw" in name:
                    if isinstance(kwargs.get("layer"), str):
                        try:
                            file = selected_files[0]
                            mos = load_era5(file, kwargs.get("layer"), "mean")
                            mos = mos * 10000
                        except (OSError, ValueError):
                            return print(f"Error in scene {scene}")
                case name if "soilm" in name:
                    if isinstance(kwargs.get("layer"), list):
                        lyrs = kwargs.get("layer")
                        try:
                            layers_list = []
                            for lyr in lyrs:
                                file = selected_files[0]
                                dataset = load_era5(file, lyr, "mean")
                                layers_list.append(dataset)
                            mos = sum_datasets(layers_list)
                            mos = mos * 1000
                        except (OSError, ValueError):
                            return print(f"Error in scene {scene}")
                    else:
                        return print("layer argument must be a list")
        case name if "persiann" in name:
            if len(selected_files) == 1:
                try:
                    file = selected_files[0]
                    mos = load_persiann(file)
                    mos = mos * 10
                except (OSError, ValueError):
                    return print(f"Error in scene {scene}")
            else:
                print('More than one file for scene, please check files')
        case "pdirnow":
            if len(selected_files) == 1:
                try:
                    file = selected_files[0]
                    mos = load_persiann(file)
                    mos = mos * 10
                except (OSError, ValueError):
                    return print(f"Error in scene {scene}")
            else:
                print('More than one file for scene, please check files')
        case _:
            try:
                mos = mosaic_raster(selected_files, kwargs.get("layer"))
                mos = mos * 0.1
            except (rxre.RioXarrayError, rioe.RasterioIOError):
                return print(f"Error in scene {scene}")

    temporal_raster = os.path.join(tempfolder, name + "_" + scene + ".tif")
    # temporal_raster = os.path.join("/Users/aldotapia/hidrocl_test/", name + "_" + scene + ".tif")
    # result_file = os.path.join("/Users/aldotapia/hidrocl_test/", name + "_" + scene + ".csv")
    result_file = os.path.join(tempfolder, name + "_" + scene + ".csv")
    mos.rio.to_raster(temporal_raster, compress="LZW")
    match name:
        case 'snow':
            subprocess.call([rscript,
                             "--vanilla",
                             "./hidrocl/products/Rfiles/WeightedPercExtraction.R",
                             kwargs.get("north_vector_path"),
                             temporal_raster,
                             result_file])

            write_line(kwargs.get("north_database"), result_file, catchment_names, scene, file_date, ncol=1)
            write_line(kwargs.get("north_pcdatabase"), result_file, catchment_names, scene, file_date, ncol=2)

            subprocess.call([rscript,
                             "--vanilla",
                             "./hidrocl/products/Rfiles/WeightedPercExtraction.R",
                             kwargs.get("south_vector_path"),
                             temporal_raster,
                             result_file])

            write_line(kwargs.get("south_database"), result_file, catchment_names, scene, file_date, ncol=1)
            write_line(kwargs.get("south_pcdatabase"), result_file, catchment_names, scene, file_date, ncol=2)

        case 'gfs':
            subprocess.call([rscript,
                             "--vanilla",
                             "./hidrocl/products/Rfiles/WeightedMeanExtractionGFS.R",
                             kwargs.get("vector_path"),
                             temporal_raster,
                             result_file])


            days = kwargs.get("days")

            if 0 in days:
                write_line(kwargs.get("databases")[0], result_file, catchment_names, scene,
                           file_date, ncol=(days.index(0)+1))
                write_line(kwargs.get("pcdatabases")[0], result_file, catchment_names, scene,
                           file_date, ncol=(days.index(0)+1)+len(days))
            if 1 in days:
                write_line(kwargs.get("databases")[1], result_file, catchment_names, scene,
                           file_date, ncol=(days.index(1)+1))
                write_line(kwargs.get("pcdatabases")[1], result_file, catchment_names, scene,
                           file_date, ncol=(days.index(1)+1)+len(days))
            if 2 in days:
                write_line(kwargs.get("databases")[2], result_file, catchment_names, scene,
                           file_date, ncol=(days.index(2)+1))
                write_line(kwargs.get("pcdatabases")[2], result_file, catchment_names, scene,
                           file_date, ncol=(days.index(2)+1)+len(days))
            if 3 in days:
                write_line(kwargs.get("databases")[3], result_file, catchment_names, scene,
                           file_date, ncol=(days.index(3)+1))
                write_line(kwargs.get("pcdatabases")[3], result_file, catchment_names, scene,
                           file_date, ncol=(days.index(3)+1)+len(days))
            if 4 in days:
                write_line(kwargs.get("databases")[4], result_file, catchment_names, scene,
                           file_date, ncol=(days.index(4)+1))
                write_line(kwargs.get("pcdatabases")[4], result_file, catchment_names, scene,
                           file_date, ncol=(days.index(4)+1)+len(days))

        case _:
            subprocess.call([rscript,
                             "--vanilla",
                             "./hidrocl/products/Rfiles/WeightedMeanExtraction.R",
                             kwargs.get("vector_path"),
                             temporal_raster,
                             result_file])

            write_line(kwargs.get("database"), result_file, catchment_names, scene, file_date, ncol=1)
            write_line(kwargs.get("pcdatabase"), result_file, catchment_names, scene, file_date, ncol=2)

    end = time.time()
    time_dif = str(round(end - start))
    currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Time elapsed for {scene}: {str(round(end - start))} seconds")
    write_log(log_file, scene, currenttime, time_dif, kwargs.get("database"))
    os.remove(temporal_raster)
    os.remove(result_file)
    gc.collect()
