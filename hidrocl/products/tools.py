# coding=utf-8

import os
import sys
from functools import reduce
from ..variables import HidroCLVariable


def compare_indatabase(*args):
    """
    Function to compare if a variable is in a database.

    :param args: lists of indatabase to compare
    :return: list
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


def read_product_files(productpath, what="modis"):
    """
    Read remote sensing/modeling product files

    :param productpath: str with product path
    :param what: str with product type
    :return: list with file names for asked product
    """
    match what:
        case "modis":
            return [value for value in os.listdir(productpath) if ".hdf" in value]
        case _:
            print("Unknown product type")
            return None


def get_product_ids(product_files, what="modis"):
    """
    Get product IDs from product files

    :param product_files: list with product files
    :param what: str with product type
    :return: list with product IDs
    """
    match what:
        case "modis":
            return [value.split(".")[1] for value in product_files]
        case _:
            print("Unknown product type")
            return None


def check_product_files(product_ids):
    """
    Extract unique product IDs from product files

    :param product_ids:
    :return: list with unique product IDs
    """
    return list(set(product_ids))


def count_scenes_occurrences(all_scenes, product_ids):
    """
    Count all_scenes in product_ids returning a dictionary
    with product IDs and number of occurrences

    :param all_scenes: list with name of all scenes
    :param product_ids: list with product IDs
    :return: dictionary with product IDs and number of occurrences
    """
    return {value: product_ids.count(value) for value in all_scenes}


def classify_occurrences(scenes_occurrences, what="modis"):
    """
    classify count_scenes based on occurrences

    :param scenes_occurrences: dict with product occurrences
    :param what: str with product type
    :return:
       - list - overpopulated scenes
       - list - complete scenes
       - list - incomplete scenes
    """

    overpopulated_scenes = []
    incomplete_scenes = []
    complete_scenes = []

    match what:
        case "modis":
            correctvalue = 9
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


def get_scenes_out_of_db(complete_scenes, common_elements):
    """
    Get scenes out of database

    :param complete_scenes: list with complete scenes
    :param common_elements: list with common elements
    :return: list with scenes out of database
    """
    match len(common_elements):
        case 0:
            lst = complete_scenes
            lst.sort()
            return lst
        case _:
            lst = list(set(complete_scenes) - set(common_elements))
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

    :param product_files: list with product files
    :param productpath: str with product path
    :return: list with scenes path
    """
    return [os.path.join(productpath, value) for value in product_files]


def check_instance(*args):
    """
    Check if arguments are instances of HidroCLVariable

    :param args: list with arguments
    :return: list with arguments
    """
    for arg in args:
        if not isinstance(arg, HidroCLVariable):
            raise TypeError("Argument should be an instance of HidroCLVariable")

    return args
