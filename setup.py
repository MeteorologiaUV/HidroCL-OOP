from setuptools import setup, find_packages

setup(
    name='hidrocl',
    version="0.0.42",
    package_dir={'': "src"},
    packages=find_packages("src"),
    install_requires=[
        'pandas==1.4.3',
        'rioxarray>=0.12.0,<0.13',
        'matplotlib==3.5.3',
        'geopandas>=0.11.1,<0.12',
        'netCDF4==1.7',
        'cdsapi>=0.7.3,<0.8',
        'earthaccess>=0.8.1,<0.9',
        'beautifulsoup4==4.11.1',
        'rasterio==1.3.2',
        'numpy==1.23.2',
        'xarray>=0.20.1,<0.21',
        'requests==2.32',
        'charset-normalizer==2.0.0',
        'setuptools==63.4.1',
        'wget==3.2',
        'exactextract>=0.2.0.dev0,<0.3',
        'ecCodes==2.44.0',
        'cfgrib~=0.9.15.1',
    ],
    python_requires='>=3.10',
)