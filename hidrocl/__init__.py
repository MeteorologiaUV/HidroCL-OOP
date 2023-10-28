# coding=utf-8
from __future__ import absolute_import
from ._version import __version__

__title__ = "hidrocl"
__summary__ = "Downloading and processing HidroCL variables"
__uri__ = "https://github.com/aldotapia/HidroCL-OOP"

__author__ = "Aldo Tapia"
__email__ = "aatapia@userena.cl"

__license__ = "MIT"
__copyright__ = "2022 Aldo Tapia"

try:
    # from . import variables, products
    from . import download, paths, preprocess
    from .variables import HidroCLVariable
    from .products import Mod13q1, Mod10a2, Mod16a2, Mcd15a2h,\
        Gpm_3imrghhl, Gldas_noah, Era5_land, ImergGIS, Gfs, Pdirnow, \
        Mod13q1agr, Era5, Era5_pressure, Era5_rh, Era5ppmax, Era5pplen
except ImportError:
    print("ImportError")
