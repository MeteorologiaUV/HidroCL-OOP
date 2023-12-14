# Changelog

### [0.0.13] - 2023-11-16
#### Added
- **ERA5**: Added ERA5 product
- **ERA pressure levels**: Added ERA5 pressure levels product
- **ERA relative humidity**: RH computation from ERA5 

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