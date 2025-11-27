# coding=utf-8

import os
import sys
from pathlib import Path
from functools import reduce
from ..variables import HidroCLVariable


def compare_indatabase(*args):
    """
    Function to compare if a variable is in a database.

    Args:
        args: lists of indatabase to compare

    Returns:
        list: list with common elements in all lists
    """
    for arg in args:
        if isinstance(arg, list):
            arg.sort()
        else:
            match arg:
                case "":
                    print(f"Argument has 0 items")
                case _:
                    raise TypeError("Argument should be a list or an empty string. Are databases created?")

    indb = [set(value) for value in args]

    return list(reduce((lambda x, y: x & y), indb))


def read_product_files(productpath, what="modis", variable=None):
    """
    Read remote sensing/modeling product files

    Args:
        productpath: str with product path
        what: str with product type
        variable: str with variable name

    Returns:
        list: list with file names for asked product
    """
    match what:
        case "modis":
            return [value for value in os.listdir(productpath) if value.endswith(".hdf")]
        case "imerg":
            return [value for value in os.listdir(productpath) if value.endswith(".HDF5")]
        case "imgis":
            return [str(value.relative_to(productpath)) for value in Path(productpath).rglob("*.tif")]
        case "gldas":
            return [value for value in os.listdir(productpath) if ".nc4" in value]
        case "gfs":
            if variable:
                return [str(value.relative_to(productpath)) for value in Path(productpath).rglob('*_'+variable+'_*.nc')]
            else:
                print('Variable not defined')
                return None
        case "persiann_ccs_cdr":
            return [value for value in os.listdir(productpath) if "PCCSCDR" in value
                    and ".bin" in value and ".gz" not in value]
        case "persiann_ccs":
            return [value for value in os.listdir(productpath) if "rgccs" in value
                    and ".bin" in value and ".gz" not in value]
        case "pdirnow":
            return [value for value in os.listdir(productpath) if "pdirnow" in value
                    and ".bin" in value and ".gz" not in value]
        case "era5":
            return [str(value.relative_to(productpath)) for value in Path(productpath).rglob('*.nc')]
        case _:
            print("Unknown product type")
            return None


def get_product_ids(product_files, what="modis"):
    """
    Get product IDs from product files

    Args:
        product_files: list with product files
        what: str with product type

    Returns:
        list: list with product IDs
    """
    match what:
        case "modis":
            return [value.split(".")[1] for value in product_files]
        case "imerg":
            return [value.split(".")[4].split("-")[0] for value in product_files]
        case "imgis":
            return [value.split(".")[4].split("-")[0] for value in product_files]
        case "gldas":
            return [value.split(".")[1] for value in product_files]
        case ("persiann_ccs_cdr" | "persiann_ccs" | "pdirnow"):
            return [value.split(".")[0].split('1d')[1] for value in product_files]
        case "gfs":
            return [value.split("_")[-1].split('.')[0] for value in product_files]
        case "era5":
            return [value.split("_")[1].split(".")[0] for value in product_files]
        case _:
            print("Unknown product type")
            return None


def check_product_files(product_ids):
    """
    Extract unique product IDs from product files

    Args:
        product_ids: list with product IDs

    Returns:
        list: list with unique product IDs
    """
    return list(set(product_ids))


def count_scenes_occurrences(all_scenes, product_ids):
    """
    Count all_scenes in product_ids returning a dictionary with product IDs and number of occurrences

    Args:
        all_scenes: list with name of all scenes
        product_ids: list with product IDs

    Returns:
        dict: dictionary with product IDs and number of occurrences
    """
    return {value: product_ids.count(value) for value in all_scenes}


def classify_occurrences(scenes_occurrences, what="modis"):
    """
    classify count_scenes based on occurrences

    Args:
        scenes_occurrences: dict with product occurrences
        what: str with product type

    Returns:
        list: list with overpopulated scenes
        list: list with complete scenes
        list: list with incomplete scenes
    """

    overpopulated_scenes = []
    incomplete_scenes = []
    complete_scenes = []

    match what:
        case "modis":
            correctvalue = 9
        case "imerg":
            correctvalue = 48
        case "imgis":
            correctvalue = 48
        case "gldas":
            correctvalue = 8
        case ("persiann_ccs_cdr" | "persiann_ccs" | "era5" | "gfs" | "pdirnow"):
            correctvalue = 1
        case _:
            print("Unknown product type")
            return None

    for scene, occurrences in scenes_occurrences.items():
        if occurrences > correctvalue:
            overpopulated_scenes.append(scene)
        if occurrences == correctvalue:
            complete_scenes.append(scene)
        if occurrences < correctvalue:
            incomplete_scenes.append(scene)

    return overpopulated_scenes, complete_scenes, incomplete_scenes


def get_scenes_out_of_db(complete_scenes, common_elements, what='modis'):
    """
    Get scenes out of database

    Args:
        complete_scenes: list with complete scenes
        common_elements: list with common elements
        what: str with product name

    Returns:
        list: list with scenes out of database
    """

    match what:
        case "modis":
            idlenght = 7
        case "imerg":
            idlenght = 8
        case "imgis":
            idlenght = 8
        case "gldas":
            idlenght = 8
        case "persiann_ccs":
            idlenght = 5
        case "persiann_ccs_cdr":
            idlenght = 6
        case "pdirnow":
            idlenght = 6
        case "era5":
            idlenght = 8
        case "gfs":
            idlenght = 10
        case _:
            idlenght = 7

    match len(common_elements):
        case 0:
            lst = complete_scenes
            lst.sort()
            return lst
        case _:
            common_elements_b = [str(value).zfill(idlenght) if
                                 isinstance(value, int) else value for value in common_elements]
            lst = list(set(complete_scenes) - set(common_elements_b))
            lst.sort()
            return lst


class HiddenPrints:
    """
    Context manager to suppress stdout and stderr.
    """
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr


def get_scenes_path(product_files, productpath):
    """
    Get scenes path from product files

    Args:
        product_files: list with product files
        productpath: str with product path

    Returns:
        list: list with scenes path
    """
    return [os.path.join(productpath, value) for value in product_files]


def check_instance(*args):
    """
    Check if arguments are instances of HidroCLVariable

    Args:
        *args: list with arguments

    Returns:
        list: list with arguments
    """
    for arg in args:
        if not isinstance(arg, HidroCLVariable):
            raise TypeError("Argument should be an instance of HidroCLVariable")

    return args
