from setuptools import setup, find_packages
from hidrocl import __version__
from hidrocl import __init__

setup(
    name='hidrocl',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'pandas>=1.4.3',
        'rioxarray>=0.12.0',
        'matplotlib>=3.5.3',
        'geopandas>=0.11.1',
        'netCDF4>=1.6.0',
        'cdsapi>=0.5.1',
        'earthaccess>=0.8.1',
        'python-cmr>=0.9.0',
    ],
    python_requires='>=3.10',
)