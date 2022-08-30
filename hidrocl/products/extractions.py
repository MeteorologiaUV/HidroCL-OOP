# coding=utf-8

import os
import gc
import re
import csv
import time
import xarray
import subprocess
import numpy as np
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

    :param file: HDF5 raster path
    :param var: variable to extract
    :return:
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


def load_gldas(file, var):
    """
    Load .nc files from GLDAS product

    :param file: str with file path
    :param var: str with variable to extract
    :return:
    """

    with t.HiddenPrints():
        da = xarray.open_dataset(file, engine="netcdf4")
        da = da[var]
        return da.sel(lat=slice(-55, -15), lon=slice(-75, -65))


def load_persiann(file):
    """
    Load .bin persiann files

    :param file: str with file path
    :return: xarray.Dataset with persiann precipitation data
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


def sum_datasets(dataset_list):
    r"""
    Function to sum xarray datasets

    :param dataset_list: list with raster products
    :return: xarray.Dataset with sum of rasters
    """
    template = dataset_list[0].copy()
    sum_values = sum([d.values for d in dataset_list])
    template.values = sum_values
    return template


def mean_datasets(dataset_list):
    r"""
    Function to get mean from xarray datasets

    :param dataset_list: list with raster products
    :return: xarray.Dataset with mean of rasters
    """
    template = dataset_list[0].copy()
    mean_values = np.mean([d.values for d in dataset_list], axis=0)
    template.values = mean_values
    return template


def mosaic_raster(raster_list, layer):
    """
    Function to compute mosaic files with rioxarray library

    :param raster_list: list with raster paths
    :param layer: str with layer to extract
    :return: rioxarray.Dataset with mosaic
    """
    raster_single = []

    for raster in raster_list:
        with rioxr.open_rasterio(raster, masked=True) as src:
            raster_single.append(getattr(src, layer))

    raster_mosaic = merge_arrays(raster_single)
    return raster_mosaic


def mosaic_nd_raster(raster_list, layer1, layer2):
    """
    Function to compute normalized difference and mosaic files with rioxarray library.
    The normalized difference is computed as:
    normalized_difference = 1000 * (layer1 - layer2) / (layer1 + layer2)

    :param raster_list: list with raster paths
    :param layer1: str with layer1 to compute normalized difference
    :param layer2: str with layer2 to compute normalized difference
    :return: rioxarray.Dataset with normalized difference's mosaic
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
    
    :param database: str with database path 
    :param result: pandas.DataFrame with result
    :param catchment_names: list with catchment names
    :param file_id: str with file ID
    :param file_date: str with file date
    :param ncol: int with number of column to extract values
    :return: None
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

    :param log_file: str with log file path
    :param file_id: str with file ID
    :param currenttime: str with current time
    :param time_dif: str with time difference
    :param database: str with database path
    :return: None
    """
    with open(log_file, 'a') as txt_file:
        txt_file.write(f'ID {file_id}. Date: {currenttime}. Process time: {time_dif} s. Database: {database}. \n')


def zonal_stats(scene, scenes_path, tempfolder, name,
                catchment_names, log_file, **kwargs):
    r"""
    Function to extract zonal statistics from raster files

    :param scene: str with scene name
    :param scenes_path: str with scenes path
    :param tempfolder: str with temp folder path
    :param name: str with product name
    :param catchment_names: list with catchment names
    :param log_file: str with log file path
    :param \**kwargs:
        See below
    :Keword Arguments:
        - **database** (str) -- Database path
        - **pcdatabase** (str) -- pcdatabase path
        - **north_database** (str) -- North database path
        - **south_database** (str) -- South database path
        - **north_pcdatabase** (str) -- North pcdatabase path
        - **south_pcdatabase** (str) -- South pcdatabase path
        - **vector_path**: str with vector path
        - **north_vector_path**: str with north vector path
        - **south_vector_path**: str with south vector path
        - **layer**: str or list with layer/layers to extract
    :return: Print
    """

    print(f'Processing scene {scene} for {name}')
    r = re.compile('.*' + scene + '.*')
    selected_files = list(filter(r.match, scenes_path))
    start = time.time()
    match name:
        case "imerg":
            file_date = datetime.strptime(scene, '%Y%m%d').strftime('%Y-%m-%d')
        case name if "gldas" in name:
            file_date = datetime.strptime(scene, 'A%Y%m%d').strftime('%Y-%m-%d')
        case "persiann_ccs":
            file_date = datetime.strptime(scene, '%y%j').strftime('%Y-%m-%d')
        case "persiann_ccs_cdr":
            file_date = datetime.strptime(scene, '%y%m%d').strftime('%Y-%m-%d')
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

        case 'imerg':
            try:
                datasets_list = [load_hdf5(ds, kwargs.get("layer")) for ds in selected_files]
                mos = sum_datasets(datasets_list)
            except OSError:
                return print(f"Error in scene {scene}")

        case name if "gldas" in name:
            match name:
                case name if ("snow" in name) or ("temp" in name) or ("et" in name):
                    if isinstance(kwargs.get("layer"), str):
                        try:
                            datasets_list = [load_gldas(ds, kwargs.get("layer")) for ds in selected_files]
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
                                datasets_list = [load_gldas(ds, lyr) for ds in selected_files]
                                layers_list.append(mean_datasets(datasets_list))
                            mos = sum_datasets(layers_list)
                            mos = mos * 100
                        except OSError:
                            return print(f"Error in scene {scene}")
                    else:
                        return print("layer argument must be a list")
        case name if "persiann" in name:
            if len(selected_files) == 1:
                try:
                    file = selected_files[0]
                    mos = load_persiann(file)
                    mos = mos * 10
                except OSError:
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
    mos.rio.to_raster(temporal_raster, dtype="uint8", compress="LZW")
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
