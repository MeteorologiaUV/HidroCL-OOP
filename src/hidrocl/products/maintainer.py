# coding=utf-8

import os
import re
import gc
import pandas as pd
import time
import xarray
from . import tools as t
import rioxarray as rioxr
from rasterio import errors as rioe
from rioxarray import exceptions as rxre


def test_load_hdf5(file):
    """
    Open .HDF5 to test file

    Args:
        file (str): file path

    Returns:
        None
    """

    with t.HiddenPrints():
        da = rioxr.open_rasterio(file, engine='h5netcdf')
        da = da[0]
        pass


def test_load_gldas(file):
    """
    Open .nc to test file

    Args:
        file (str): file path

    Returns:
        None
    """

    with t.HiddenPrints():
        da = xarray.open_dataset(file, engine="netcdf4")
        pass


def test_load_persiann(file):
    """
    Load .bin to test file

    Args:
        file (str): file path

    Returns:
        None
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

    Args:
        log_file (str): str with log file path
        file (str): str with file path

    Returns:
        None
    """
    currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(log_file, 'a') as txt_file:
        txt_file.write(f'File {file} deleted. Date: {currenttime}\n')


def test_open_raster(raster_list):
    """
    Function test files with rioxarray

    Args:
        raster_list (list): list with raster paths

    Returns:
        None
    """

    if isinstance(raster_list, list):
        for raster in raster_list:
            with rioxr.open_rasterio(raster, masked=True) as src:
                pass
    else:
        with rioxr.open_rasterio(raster_list, masked=True) as src:
            pass


def file_maintainer(scene, scenes_path, name, log_file=None):
    """
    Function to maintain files in the directory

    Args:
        scene (str): str with scene id to process
        scenes_path (list): list with path to scenes
        name (str): str withname of the product
        log_file (str): str with log path

    Returns:
        Print
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
                    if log_file:
                        write_del_log(log_file, file)
            case 'imgis':
                try:
                    test_load_imerggis(file)
                except (rxre.RioXarrayError, rioe.RasterioIOError, ValueError):
                    print(f'Removing {file}')
                    os.remove(file)
                    if log_file:
                        write_del_log(log_file, file)
            case 'gldas':
                try:
                    test_load_gldas(file)
                except OSError:
                    print(f'Removing {file}')
                    os.remove(file)
                    if log_file:
                        write_del_log(log_file, file)
            case name if "persiann" in name:
                try:
                    test_load_persiann(file)
                except (OSError, ValueError):
                    print(f'Removing {file}')
                    os.remove(file)
                    if log_file:
                        write_del_log(log_file, file)
            case name if "pdirnow" in name:
                try:
                    test_load_persiann(file)
                except (OSError, ValueError):
                    print(f'Removing {file}')
                    os.remove(file)
                    if log_file:
                        write_del_log(log_file, file)
            case "era5":
                try:
                    test_load_era5(file)
                except (OSError, ValueError):
                    print(f'Removing {file}')
                    os.remove(file)
                    if log_file:
                        write_del_log(log_file, file)
            case _:
                try:
                    test_open_raster(file)
                except (rxre.RioXarrayError, rioe.RasterioIOError):
                    print(f'Removing {file}')
                    os.remove(file)
                    if log_file:
                        write_del_log(log_file, file)
    gc.collect()


def db_maintainer(path):
    """
    Read a CSV database, drop duplicate rows by name_id, sort by date, and write back.

    Args:
        path (str): path to the CSV database file

    Returns:
        None
    """
    df = pd.read_csv(path, dtype={'name_id': str})
    before = len(df)
    df = df.drop_duplicates(subset='name_id')
    df = df.sort_values('date')
    df.to_csv(path, index=False)
    removed = before - len(df)
    if removed:
        print(f'{path}: removed {removed} duplicate(s), {len(df)} records remaining')
    else:
        print(f'{path}: {len(df)} records, no duplicates found')


def _clean_variable(variable):
    db_maintainer(variable.database)
    db_maintainer(variable.pcdatabase)


def mod13q1_db_maintainer(product):
    """
    Clean databases for Mod13q1 product (ndvi, evi, nbr).

    Args:
        product (Mod13q1): Mod13q1 product instance

    Returns:
        None
    """
    _clean_variable(product.ndvi)
    _clean_variable(product.evi)
    _clean_variable(product.nbr)


def vnp13q1_db_maintainer(product):
    """
    Clean databases for Vnp13q1 product (ndvi, evi, nbr).

    Args:
        product (Vnp13q1): Vnp13q1 product instance

    Returns:
        None
    """
    _clean_variable(product.ndvi)
    _clean_variable(product.evi)
    _clean_variable(product.nbr)


def mod13q1agr_db_maintainer(product):
    """
    Clean databases for Mod13q1agr product (ndvi).

    Args:
        product (Mod13q1agr): Mod13q1agr product instance

    Returns:
        None
    """
    _clean_variable(product.ndvi)


def vnp13q1agr_db_maintainer(product):
    """
    Clean databases for Vnp13q1agr product (ndvi).

    Args:
        product (Vnp13q1agr): Vnp13q1agr product instance

    Returns:
        None
    """
    _clean_variable(product.ndvi)


def mod10a2_db_maintainer(product):
    """
    Clean databases for Mod10a2 product (nsnow, ssnow).

    Args:
        product (Mod10a2): Mod10a2 product instance

    Returns:
        None
    """
    _clean_variable(product.nsnow)
    _clean_variable(product.ssnow)


def mod10a1f_db_maintainer(product):
    """
    Clean databases for Mod10a1f product (nsnow, ssnow).

    Args:
        product (Mod10a1f): Mod10a1f product instance

    Returns:
        None
    """
    _clean_variable(product.nsnow)
    _clean_variable(product.ssnow)


def vnp10a1f_db_maintainer(product):
    """
    Clean databases for Vnp10a1f product (nsnow, ssnow).

    Args:
        product (Vnp10a1f): Vnp10a1f product instance

    Returns:
        None
    """
    _clean_variable(product.nsnow)
    _clean_variable(product.ssnow)


def mod16a2_db_maintainer(product):
    """
    Clean databases for Mod16a2 product (pet, et).

    Args:
        product (Mod16a2): Mod16a2 product instance

    Returns:
        None
    """
    _clean_variable(product.pet)
    _clean_variable(product.et)


def mod12q1_db_maintainer(product):
    """
    Clean databases for Mod12q1 product (brn, crp, csh, cvm, dbf, dnf, ebf, enf,
    grs, mxf, osh, pwt, snw, svn, urb, wat, wsv).

    Args:
        product (Mod12q1): Mod12q1 product instance

    Returns:
        None
    """
    for var in [product.brn, product.crp, product.csh, product.cvm,
                product.dbf, product.dnf, product.ebf, product.enf,
                product.grs, product.mxf, product.osh, product.pwt,
                product.snw, product.svn, product.urb, product.wat,
                product.wsv]:
        _clean_variable(var)


def mcd15a2h_db_maintainer(product):
    """
    Clean databases for Mcd15a2h product (lai, fpar).

    Args:
        product (Mcd15a2h): Mcd15a2h product instance

    Returns:
        None
    """
    _clean_variable(product.lai)
    _clean_variable(product.fpar)


def vnp15a2h_db_maintainer(product):
    """
    Clean databases for Vnp15a2h product (lai, fpar).

    Args:
        product (Vnp15a2h): Vnp15a2h product instance

    Returns:
        None
    """
    _clean_variable(product.lai)
    _clean_variable(product.fpar)


def gpm_3imrghhl_db_maintainer(product):
    """
    Clean databases for Gpm_3imrghhl product (pp).

    Args:
        product (Gpm_3imrghhl): Gpm_3imrghhl product instance

    Returns:
        None
    """
    _clean_variable(product.pp)


def imerggis_db_maintainer(product):
    """
    Clean databases for ImergGIS product (pp).

    Args:
        product (ImergGIS): ImergGIS product instance

    Returns:
        None
    """
    _clean_variable(product.pp)


def gldas_noah_db_maintainer(product):
    """
    Clean databases for Gldas_noah product (snow, temp, et, soilm).

    Args:
        product (Gldas_noah): Gldas_noah product instance

    Returns:
        None
    """
    _clean_variable(product.snow)
    _clean_variable(product.temp)
    _clean_variable(product.et)
    _clean_variable(product.soilm)


def pdirnow_db_maintainer(product):
    """
    Clean databases for Pdirnow product (pp).

    Args:
        product (Pdirnow): Pdirnow product instance

    Returns:
        None
    """
    _clean_variable(product.pp)


def era5_land_db_maintainer(product):
    """
    Clean databases for Era5_land product (et, pet, snw, snwa, snwdn, snwdt, soilm).

    Args:
        product (Era5_land): Era5_land product instance

    Returns:
        None
    """
    for var in [product.et, product.pet, product.snw, product.snwa,
                product.snwdn, product.snwdt, product.soilm]:
        _clean_variable(var)


def era5_db_maintainer(product):
    """
    Clean databases for Era5 product (pp, temp, tempmin, tempmax, dew, pres, u, v).

    Args:
        product (Era5): Era5 product instance

    Returns:
        None
    """
    for var in [product.pp, product.temp, product.tempmin, product.tempmax,
                product.dew, product.pres, product.u, product.v]:
        _clean_variable(var)


def era5ppmax_db_maintainer(product):
    """
    Clean databases for Era5ppmax product (ppmax).

    Args:
        product (Era5ppmax): Era5ppmax product instance

    Returns:
        None
    """
    _clean_variable(product.ppmax)


def era5pplen_db_maintainer(product):
    """
    Clean databases for Era5pplen product (pplen).

    Args:
        product (Era5pplen): Era5pplen product instance

    Returns:
        None
    """
    _clean_variable(product.pplen)


def era5_pressure_db_maintainer(product):
    """
    Clean databases for Era5_pressure product (z).

    Args:
        product (Era5_pressure): Era5_pressure product instance

    Returns:
        None
    """
    _clean_variable(product.z)


def era5_rh_db_maintainer(product):
    """
    Clean databases for Era5_rh product (rh).

    Args:
        product (Era5_rh): Era5_rh product instance

    Returns:
        None
    """
    _clean_variable(product.rh)


def gfs_db_maintainer(product):
    """
    Clean databases for Gfs product (db0, db1, db2, db3, db4).

    Args:
        product (Gfs): Gfs product instance

    Returns:
        None
    """
    for var in [product.db0, product.db1, product.db2, product.db3, product.db4]:
        _clean_variable(var)
