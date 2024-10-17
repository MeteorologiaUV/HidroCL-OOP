# coding=utf-8
from __future__ import absolute_import
from .__version__ import __version__
import importlib

__title__ = "hidrocl"
__summary__ = "Downloading and processing HidroCL variables"
__uri__ = "https://github.com/MeteorologiaUV/HidroCL-OOP"

__author__ = "Aldo Tapia"
__email__ = "aatapia@userena.cl"

__license__ = "MIT"
__copyright__ = "2024 Aldo Tapia"

__supportcreation__ = False

project_path = ''
github_path = ''
observed_products_path = 'observed'
forecasted_products_path = 'forecasted'
processing_path = ''
hidrocl_root_path = ''
report_emails = ''

try:
    from . import download, paths, preprocess
    from .variables import HidroCLVariable
    from .products import Mod13q1, Mod10a2, Mod16a2, Mcd15a2h, Mod12q1, \
        Gpm_3imrghhl, Gldas_noah, Era5_land, ImergGIS, Gfs, Pdirnow, \
        Mod13q1agr, Era5, Era5_pressure, Era5_rh, Era5ppmax, Era5pplen
except ImportError:
    print("ImportError")


def reload_paths():
    """
    Reloads the paths module

    Returns:
        None
    """
    importlib.reload(paths)
    return None


def set_project_path(path):
    """
    Sets the project path

    Args:
        path (str): path to the project

    Returns:
        None
    """
    global project_path
    project_path = path
    reload_paths()
    return None


def set_processing_path(path):
    """
    Sets the processing path

    Args:
        path (str): path to the processing

    Returns:
        None
    """
    global processing_path
    processing_path = path
    reload_paths()
    return None


def set_observed_products_path(path):
    """
    Sets the observed products path

    Args:
        path (str): path to the observed products

    Returns:
        None
    """
    global observed_products_path
    observed_products_path = path
    reload_paths()
    return None


def set_forecasted_products_path(path):
    """
    Sets the forecasted products path

    Args:
        path (str): path to the forecasted products

    Returns:
        None
    """
    global forecasted_products_path
    forecasted_products_path = path
    reload_paths()
    return None


def prepare_path(path):
    """
    Check if the path exists and if not, creates it
    Args:
        path (str): path to the folder

    Returns:
        print: path checked or created
    """

    import os
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'Path {path} created')
    else:
        print(f'Path {path} exists')
    return None


def get_today_date():
    """
    Returns today's date at 00:00:00

    Returns:
        str: today's date
    """
    from datetime import datetime
    return datetime.fromisoformat(datetime.today().strftime('%Y-%m-%d') + 'T00:00:00')


def temporal_directory():
    """
    Returns the temporal directory

    Returns:
        str: temporal directory
    """
    from tempfile import TemporaryDirectory
    return TemporaryDirectory()
