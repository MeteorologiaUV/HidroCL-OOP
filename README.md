# HidroCL database maintainer

----

[![pythonversion](https://img.shields.io/badge/python-v3.10-blue?style=plastic&logo=python&logoColor=yellow)](https://www.python.org/downloads/release/python-3100/)
[![packageversion](https://img.shields.io/badge/r-v4.1.2-blue?style=plastic&logo=r&logoColor=9cf)](https://anaconda.org/conda-forge/r-base?version=4.2.1)
![packageversion](https://img.shields.io/badge/version-v0.0.10-blue?style=plastic)

## Data download

*to do: add description about data downloading* 

## Data extraction

*to do: add description about data extraction*

**Note**: In macOS, the command for running R is `RScript`, while in Linux is `Rscript`.

**Access to documentation [here](https://aldotapia.github.io/HidroCL-OOP/)**

----

## TODO list

- [ ] complete README.md
- [x] hidrocl basic variable
  - [x] add old code
  - [x] adapt code to modules OOP approach
  - [x] test locally
  - [x] test on nas
    > **Notes:**
    > 
    > Values in Pixel count aren't consistent with `NA` values in the database.
    >
    > **Solved**: there was a bug in write_line function.
- [x] GLDAS_NOAHH25_3H processing
  - [x] test locally
  - [x] test on nas
- [x] GPM_3IMERGHHL processing
  - [x] test locally
  - [x] test on nas
- [ ] MCD12Q1 processing (*Land cover type, last update was on 2020*)
- [x] MCD15A2H processing
  - [x] test locally
  - [x] test on nas
  > **Notes:**
  > 
  > There are several invalid images.
  > 
  > **To do**: create a image maintainer removing the invalid files.
- [ ] ~~MCD43A3 processing~~ *out of database for now*
- [ ] MOD09A1 processing (*reflectance product, to evaluate later*)
- [x] MOD10A2 processing
  - [x] test locally
  - [x] test on nas
- [x] MOD13Q1 processing
  - [x] test locally
  - [x] test on nas
- [x] MOD16A2 processing
  - [x] test locally
  - [x] test on nas
- [x] PERSIANN processing
  - [x] test locally
  - [x] test on nas
- [x] ERA5-Land processing
  - [x] test locally
  - [x] test on nas
- [x] GFS processing
  - [x] test locally
  - [x] test on nas
- [ ] Download functions refactoring
  - [ ] PERSIANN (FTP approach)
  - [ ] Earthdata (API approach)
  - [ ] MODIS web scraping (include?)
  - [x] ERA5-Land hourly (API approach)
  - [x] soil moisture (API approach)
  - [x] IMERG GIS (HTTPS approach)
  - [ ] test download functions  
- [ ] Add documentation
  - [x] add variables documentation
  - [x] add products documentation
    - [x] MOD13Q1
    - [x] MOD10A2
    - [x] MCD15A2H
    - [x] MOD16A2
    - [x] GPM_3IMERGHHL
    - [x] GLDAS_NOAHH25_3H
    - [x] PERSIANN
    - [x] ERA5-Land
- [ ] Add tests
- [ ] Add examples
- [ ] Add flowcharts

----
## Packages used

**Conda:**

`rpi2` not working with `sf`: [![packageversion](https://img.shields.io/badge/rpi2-v3.5.1-green?style=plastic)](https://anaconda.org/conda-forge/rpy2?version=3.5.1)

*R Libraries*


[![packageversion](https://img.shields.io/badge/r--terra-v1.5.21-green?style=plastic)](https://anaconda.org/conda-forge/r-terra)
[![packageversion](https://img.shields.io/badge/r--sf-v1.0.6-green?style=plastic)](https://anaconda.org/conda-forge/r-sf)
[![packageversion](https://img.shields.io/badge/r--exactextractr-v0.9.0-green?style=plastic)](https://anaconda.org/conda-forge/r-exactextractr)
[![packageversion](https://img.shields.io/badge/tibble-v3.1.8-green?style=plastic)](https://anaconda.org/conda-forge/r-tibble)

*Interactive code*

[![packageversion](https://img.shields.io/badge/jupyter-v1.0.0-green?style=plastic)](https://anaconda.org/conda-forge/jupyter)

*Python*

[![packageversion](https://img.shields.io/badge/pandas-v1.4.3-green?style=plastic)](https://anaconda.org/conda-forge/pandas)
[![packageversion](https://img.shields.io/badge/rioxarray-v0.12.0-green?style=plastic)](https://anaconda.org/conda-forge/rioxarray)
[![packageversion](https://img.shields.io/badge/matplotlib-v3.5.3-green?style=plastic)](https://anaconda.org/conda-forge/matplotlib)
[![packageversion](https://img.shields.io/badge/geopandas-v0.11.1-green?style=plastic)](https://anaconda.org/conda-forge/geopandas)
[![packageversion](https://img.shields.io/badge/netCDF4-v1.6.0-green?style=plastic)](https://anaconda.org/conda-forge/netcdf4)
[![packageversion](https://img.shields.io/badge/earthdata-v0.4.1-green?style=plastic)](https://anaconda.org/conda-forge/earthdata)

*Documentation*

[![packageversion](https://img.shields.io/badge/mkdocs-v1.4.0-green?style=plastic)](https://www.mkdocs.org)
[![packageversion](https://img.shields.io/badge/mkdocstrings-v0.19.0-green?style=plastic)](https://mkdocstrings.github.io)
[![packageversion](https://img.shields.io/badge/mkdocstrings-v8.5.6-green?style=plastic)](https://squidfunk.github.io/mkdocs-material/)
[![packageversion](https://img.shields.io/badge/mkdocstrings--python-v0.7.1-green?style=plastic)](https://pypi.org/project/mkdocstrings-python/)

Installation commands:
**Environment creation and first steps:**
```bash
# installing Python and R
conda create -n hidrocl python=3.10  # R is installed with the r-sf package
conda activate hidrocl
# installing needed R packages
conda install -c conda-forge r-sf r-terra r-exactextractr r-tibble
# for running tests
conda install -c conda-forge jupyter
#  installing python libraries
conda install -c conda-forge pandas rioxarray matplotlib geopandas netCDF4 earthdata
# installing CDS api
pip install cdsapi
# documenting with mkdocs
pip install mkdocs
pip install mkdocstrings
pip install mkdocs-material
pip install mkdocstrings-python
```

**R package needed for sf/terra messages**

```R
install.packages("codetools", dependencies = TRUE)
install.packages("tibble", dependencies = TRUE)
```

----

## Changelog

### [0.0.12] - 2023-01-23
#### Changed
- **Era5Land**: Added temp min and max in the extraction
- **GFS**: added min reducer

#### Removed
- **PERSIANN**: removed PERSIANN CCS and PERSIANN-CCS-CDR product

### [0.0.11] - 2022-12-21
#### Added
- **PDIR-Nor**: Added support to PDIR-Now product

#### Changed
- Fixed some GFS bugs, now it's working properly

#### To do
- Add GFS maintainer

### [0.0.10] - 2022-12-20
#### Added
- **GFS processing**: processing of GFS to multiple databases depending of valid time (up to 5 days)
- **IMERG GIS processing**: processing of TIF files to multiple

### [0.0.9] - 2022-10-19
#### Added
- **ERA5-Land processing**: processing of temp, pp, evapotranspiration (potential and total) snow (cover, albedo, density and depth), soil moisture from ERA5-Land product
- **mkdocs documentation**: documentation of the package with mkdocs

#### Removed
- **sphinx documentation**: now it works with mkdocs

### [0.0.8] - 2022-09-26
#### Added
- **download_era5land**: function to download era5 files using .cdsapirc credentials. This is the first of a series of functions of the same time.

### [0.0.7] - 2022-08-30
#### Added
- **run_maintainer**: function to test files inside product path folder and delete corrupt files.

#### To do
- Add for each product a download function complementing maintainer function.

### [0.0.6] - 2022-08-29
#### Added
- **GLDAS_NOAHH25_3H processing**: processing for snow, temperature, evapotranspiration, and soil moisture extraction.
- **PERSIANN processing**: processing for precipitation extraction.
- **zonal_stats**: function refactored, now multiple rasters by date and variable (GLDAS and IMERG)

### [0.0.5] - 2022-08-25
#### Added
- **GPM_3IMRGHHL processing**: processing for IMERG precipitation (PP) product. Documentation updated
- **zonal_stats**: function refactored, now supports IMERG (HDF5)

### [0.0.4] - 2022-08-24
#### Added
- **MOD16A2 processing**: processing for potential evapotranspiration (PET) modis product. Documentation updated
- **MCD15A2H processing**: processing for LAI and FPAR modis product. Documentation updated.
- **run_extraction**: now the output list is sorted (*to do* from 0.0.3)

### [0.0.3] - 2022-08-23
#### Added
- **MOD10A2 processing**: processing for north and south face snow cover extension extraction.
- **Documentation**: added documentation which can be accessed from [here](https://aldotapia.github.io/HidroCL-OOP/). Although the documentation is not complete, it is a good starting point.

#### Changed
- **run_extraction**: function refactored. Looking foward for changing names and adding more options.
- **Check `NA`s**: check if `NA`s values in database are coherent with raster images.

#### To do
- **run_extraction**: run function with sorted files from later to recent.


### [0.0.2] - 2022-08-22
#### Added
- **MOD13Q1 processing**: temporal folder and file remove actions are commented for testing purposes. After running and analyzing the results, uncomment the actions.


### [0.0.1] - 2022-08-18
#### Added
- HidroCLVariable object refactored from [hidroclabc.py](https://github.com/aldotapia/HidroCL-DBCreation/blob/main/Class%20tests/hidroclabc.py)
- [local](https://github.com/aldotapia/HidroCL-OOP/blob/main/local_tests.ipynb) and [nas](https://github.com/aldotapia/HidroCL-OOP/blob/main/nas_tests.ipynb) tests for HidroCLVariable object