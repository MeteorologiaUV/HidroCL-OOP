# coding=utf-8

import os
import sys
from functools import reduce
from ..variables import HidroCLVariable


def compare_indatabase(*args):
    """compare indatabase and return elements that are equal"""
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
    """read product files"""
    match what:
        case "modis":
            return [value for value in os.listdir(productpath) if ".hdf" in value]
        case _:
            print("Unknown product type")
            return None


def get_product_ids(product_files, what="modis"):
    """get product ids"""
    match what:
        case "modis":
            return [value.split(".")[1] for value in product_files]
        case _:
            print("Unknown product type")
            return None


def check_product_files(product_ids):
    """extract uniqu names from product files"""
    files_id = []
    for product_id in product_ids:
        if product_id not in files_id:
            files_id.append(product_id)
    files_id.sort()
    return files_id


def count_scenes_occurrences(all_scenes, product_ids):
    """count self.all_scenes in self.product_ids returning a dictionary"""
    count_scenes = {}
    for scene in all_scenes:
        count_scenes[scene] = product_ids.count(scene)
    return count_scenes


def classify_ocurrences(scenes_occurrences, what="modis"):
    """classify count_scenes based on ocurrences
    :param what: product type
    :type scenes_occurrences: dictionary
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
    """compare scenes that are not in the database
    :type common_elements: list
    :type complete_scenes: list
    """
    scenes_out_of_db = []
    for scene in complete_scenes:
        if scene not in common_elements:
            scenes_out_of_db.append(scene)
    return scenes_out_of_db


class HiddenPrints:
    """hide print statements"""
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def get_scenes_path(product_files, productpath):
    """get scenes path"""
    return [os.path.join(productpath, value) for value in product_files]


def check_instance(*args):
    """Function to check instance of inputs"""

    results = []

    for arg in args:
        results.append(isinstance(arg, HidroCLVariable))

    return all(results)
