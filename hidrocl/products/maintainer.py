# coding=utf-8

import os
import re
import gc
import time
import xarray
from . import tools as t
import rioxarray as rioxr
from rasterio import errors as rioe
from rioxarray import exceptions as rxre


def test_load_hdf5(file):
    """
    Open .HDF5 to test file

    :param file: HDF5 raster path
    :return: None
    """

    with t.HiddenPrints():
        da = rioxr.open_rasterio(file, engine='h5netcdf')
        da = da[0]
        pass


def test_load_gldas(file):
    """
    Open .nc to test file

    :param file: str with file path
    :return: None
    """

    with t.HiddenPrints():
        da = xarray.open_dataset(file, engine="netcdf4")
        pass


def test_load_persiann(file):
    """
    Load .bin to test file

    :param file: str with file path
    :return: None
    """
    with t.HiddenPrints():
        da = open(file, 'rb')
        pass


def test_load_era5(file):
    """
    Load .nc to test file

    Args:
        file (str): file path

    Returns:
        None
    """
    with t.HiddenPrints():
        da = xarray.open_dataset(file, mask_and_scale=True)
        pass


def test_load_imerggis(file):
    """
    Load .tiff to test file

    Args:
        file (str): file path

    Returns:
        None
    """

    with t.HiddenPrints():
        da = rioxr.open_rasterio(file)
        pass


def load_tif(file):
    """
    Load .tif to test file

    Args:
        file (str): file path

    Returns:
        None
    """

    with t.HiddenPrints():
        da = rioxr.open_rasterio(file)
        pass


def write_del_log(log_file, file):
    """
    Write log file for deleted files

    :param log_file: str with log file path
    :param file: str with file path
    :return: None
    """
    currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(log_file, 'a') as txt_file:
        txt_file.write(f'File {file} deleted. Date: {currenttime}\n')


def test_open_raster(raster_list):
    """
    Function test files with rioxarray

    :param raster_list: list with raster paths
    :return: None
    """

    if isinstance(raster_list, list):
        for raster in raster_list:
            with rioxr.open_rasterio(raster, masked=True) as src:
                pass
    else:
        with rioxr.open_rasterio(raster_list, masked=True) as src:
            pass


def file_maintainer(scene, scenes_path, name, log_file):
    """

    :param scene: str with scene id to process
    :param scenes_path: list with path to scenes
    :param name: str withname of the product
    :param log_file: str with log path
    :return: Print
    """

    r = re.compile('.*' + scene + '.*')
    selected_files = list(filter(r.match, scenes_path))

    for file in selected_files:
        match name:
            case 'imerg':
                try:
                    test_load_hdf5(file)
                except OSError:
                    print(f'Removing {file}')
                    os.remove(file)
                    write_del_log(log_file, file)
            case 'imgis':
                try:
                    test_load_imerggis(file)
                except (rxre.RioXarrayError, rioe.RasterioIOError):
                    print(f'Removing {file}')
                    os.remove(file)
                    write_del_log(log_file, file)
            case 'gldas':
                try:
                    test_load_gldas(file)
                except OSError:
                    print(f'Removing {file}')
                    os.remove(file)
                    write_del_log(log_file, file)
            case name if "persiann" in name:
                try:
                    test_load_persiann(file)
                except (OSError, ValueError):
                    print(f'Removing {file}')
                    os.remove(file)
                    write_del_log(log_file, file)
            case "era5":
                try:
                    test_load_era5(file)
                except (OSError, ValueError):
                    print(f'Removing {file}')
                    os.remove(file)
                    write_del_log(log_file, file)
            case _:
                try:
                    test_open_raster(file)
                except (rxre.RioXarrayError, rioe.RasterioIOError):
                    print(f'Removing {file}')
                    os.remove(file)
                    write_del_log(log_file, file)
    gc.collect()
