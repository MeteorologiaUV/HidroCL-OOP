# coding=utf-8

import os
import gc
import re
import csv
import time
import subprocess
from math import ceil
import rioxarray as rioxr
from rioxarray import exceptions as rxre
from datetime import datetime
from rioxarray.merge import merge_arrays


def mosaic_raster(raster_list, layer):
    """function to mosaic files with rioxarray library"""
    raster_single = []

    for raster in raster_list:
        with rioxr.open_rasterio(raster, masked=True) as src:
            raster_single.append(getattr(src, layer))

    raster_mosaic = merge_arrays(raster_single)
    return raster_mosaic


def mosaic_nd_raster(raster_list, layer1, layer2):
    """function to compute normalized difference and mosaic files with rioxarray library"""
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


def write_line(database, result, catchment_names, file_id, file_date, nrow=1):
    """Write line in database"""
    with open(result) as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        gauge_id_result = []
        value_result = []
        for row in csvreader:
            gauge_id_result.append(row[0])
            value_result.append(row[nrow])
    gauge_id_result = [value for value in gauge_id_result[1:]]
    value_result = [str(ceil(float(value))) if value.replace('.', '', 1).isdigit() else 'NA' for value in
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
    """write log file"""
    with open(log_file, 'a') as txt_file:
        txt_file.write(f'ID {file_id}. Date: {currenttime}. Process time: {time_dif} s. Database: {database}. \n')


def weighted_mean_modis(scene, scenes_path, tempfolder,
                        name, vector_path,
                        database, pcdatabase,
                        catchment_names, log_file, **kwargs):
    """function to calculate weighted mean of scenes"""

    print(f'Processing scene {scene} for {name}')
    r = re.compile('.*' + scene + '.*')
    selected_files = list(filter(r.match, scenes_path))
    start = time.time()
    file_date = datetime.strptime(scene, 'A%Y%j').strftime('%Y-%m-%d')

    match name:
        case 'nbr':
            try:
                mos = mosaic_nd_raster(selected_files, kwargs.get("layer1"), kwargs.get("layer2"))
            except rxre.RioXarrayError:
                return print(f"Error in scene {scene}")

        case _:
            try:
                mos = mosaic_raster(selected_files, kwargs.get("layer"))
                mos = mos * 0.1
            except rxre.RioXarrayError:
                return print(f"Error in scene {scene}")

    # temporal_raster = os.path.join(tempfolder, name + "_" + scene + ".tif")
    temporal_raster = os.path.join("/Users/aldotapia/hidrocl_test/", name + "_" + scene + ".tif")
    result_file = os.path.join("/Users/aldotapia/hidrocl_test/", name + "_" + scene + ".csv")
    # result_file = os.path.join(tempfolder, name + "_" + scene + ".csv")
    mos.rio.to_raster(temporal_raster, compress="LZW")
    subprocess.call(["RScript",
                     "--vanilla",
                     "./hidrocl/products/Rfiles/WeightedMeanExtraction.R",
                     vector_path,
                     temporal_raster,
                     result_file])

    write_line(database, result_file, catchment_names, scene, file_date, nrow=1)
    write_line(pcdatabase, result_file, catchment_names, scene, file_date, nrow=2)
    end = time.time()
    time_dif = str(round(end - start))
    currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Time elapsed for {scene}: {str(round(end - start))} seconds")
    write_log(log_file, scene, currenttime, time_dif, database)
    # os.remove(temporal_raster)
    # os.remove(result_file)
    gc.collect()
