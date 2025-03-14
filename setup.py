from setuptools import setup, find_packages

setup(
    name='hidrocl',
    version="0.0.27",
    package_dir={'':"src"},
    packages=find_packages("src"),
    install_requires=[
        'pandas>=1.4.3',
        'rioxarray>=0.12.0',
        'matplotlib>=3.5.3',
        'geopandas>=0.11.1',
        'netCDF4>=1.6.0',
        'cdsapi>=0.7.3',
        'earthaccess>=0.8.1',
        'beautifulsoup4>=4.11.1',
        'rasterio>=1.3.2',
        'numpy>=1.23.2',
        'xarray>=0.20.1',
        'requests>=2.28.1',
        'setuptools>=63.4.1',
        'wget>=3.2',
        'exactextract>=0.2.0.dev0',
        'python-dotenv>=1.0.0',
        'netcdf4>=1.7'
    ],
    python_requires='>=3.10',
)
