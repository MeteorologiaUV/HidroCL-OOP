# coding=utf-8
from __future__ import absolute_import
from .__version__ import __version__
from .__conf__ import *
import importlib


__title__ = "hidrocl"
__summary__ = "Downloading and processing HidroCL variables"
__uri__ = "https://github.com/aldotapia/HidroCL-OOP"

__author__ = "Aldo Tapia"
__email__ = "aatapia@userena.cl"

__license__ = "MIT"
__copyright__ = "2023 Aldo Tapia"

try:
    from . import download, paths, preprocess
    from .variables import HidroCLVariable
    from .products import Mod13q1, Mod10a2, Mod16a2, Mcd15a2h,\
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
