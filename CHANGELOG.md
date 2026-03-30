# Changelog

### [0.0.37] - 2026-03-30
#### Added
- **VIIRS products**: Added full support for VNP13Q1 (vegetation indices + agricultural NDVI), VNP10A1F (snow cover), and VNP15A2H (LAI/FPAR) through `Vnp13q1`, `Vnp13q1agr`, `Vnp10a1f`, and `Vnp15a2h` classes
- **VIIRS server scripts**: Added operational workflow scripts `vnp13q1.py`, `vnp10a1f.py`, and `vnp15a2h.py` in `workflow/server/`, integrated into `run_all.py`
- **ERA5-Land B variant**: Added `server_era5landB.py` processing script

#### Changed
- **Dependencies**: Updated `cdsapi>=0.7.3`, `requests>=2.32`, added `ecCodes>=2.44.0` and `cfgrib~=0.9.15.1`

### [0.0.36] - 2026-03-29
#### Changed
- **Maintainer**: Module heavily expanded with full maintainer logic for all product classes (`vnp13q1_db_maintainer`, `vnp10a1f_db_maintainer`, `vnp15a2h_db_maintainer`, and others)
- **Products**: `extractions.py` and `tools.py` refactored for improved VIIRS and MODIS handling
- **Products**: `__init__.py` updated with refined class logic
- **Workflow**: ERA5, ERA5-Land, and ERA5-PL server scripts updated

### [0.0.33] - 2026-03-11
#### Fixed
- **GFS**: Fully working after fixes to GFS extraction and download flow
#### Changed
- **Download**: Minor update to download module

### [0.0.31] - 2026-01-18
#### Added
- **VIIRS download**: `viirs_download()` function incorporated into `hidrocl.download`, supporting snow, vegetation, LAI, and reflectance products

### [0.0.30] - 2026-01-15
#### Added
- **VIIRS products**: Added `Vnp13q1`, `Vnp13q1agr`, `Vnp10a1f`, `Vnp15a2h` product classes
- **Dependencies**: Added `ecCodes>=2.44.0` and `cfgrib~=0.9.15.1` for GRIB support
- **Paths**: Added VIIRS-specific database and log paths to `hidrocl.paths`

### [0.0.29] - 2026-01-12
#### Changed
- **GFS download**: Revamped from OpenDAP to GRIB-based download for improved reliability and compatibility

### [0.0.28] - 2025-11-27
#### Fixed
- **MODIS download**: Fixed file reading in `products/tools.py` that caused failures in the MODIS downloading process

### [0.0.27] - 2025-03-10
#### Added
- **Scene selector**: Added ability to process a specific subset of scenes
- **Corrupt scene handling**: Products now detect and skip corrupt scenes during extraction

### [0.0.26] - 2024-12-01
#### Fixed
- **ERA5 download**: Fixed ERA5 download function

### [0.0.25] - 2024-10-16
#### Changed
- **Download**: Updated download functions with improved logic and PEP formatting adjustments

### [0.0.23] - 2024-09-15
#### Changed
- **Dependencies**: Updated `requests>=2.32`, `netcdf4>=1.7` for new cdsapi compatibility
- **cdsapi**: Multiple fixes for compatibility with the new Copernicus CDS API

### [0.0.22] - 2024-09-05
#### Changed
- **cdsapi**: Updated code to work with the new cdsapi authentication and endpoint format

### [0.0.21] - 2024-06-19
#### Fixed
- **GFS**: Fixed GFS extraction errors
- **Paths**: Updated path references

### [0.0.19] - 2024-04-09
#### Changed
- **Refactor**: Removed `__conf__.py`, configuration merged into `__init__.py`
- **Variables**: Improved `HidroCLVariable` methods (`checkdatabase`, `checkpcdatabase`, `valid_data`)
- **Paths**: Simplified path module

### [0.0.18] - 2024-04-08
#### Added
- **MCD12Q1**: Added land cover (LULC) product support via `Mod12q1` class

### [0.0.17] - 2024-04-07
#### Changed
- **Package structure**: Merged `__conf__.py` configuration into `__init__.py`, streamlining package layout

### [0.0.16] - 2024-04-05
#### Added
- **exactextract**: First implementation of `exactextract` for zonal statistics extraction
- **dotenv**: Added `python-dotenv` support for project path configuration via `.env` files
- **Workflow scripts**: Added complete workflow scripts for all products in `workflow/server/`

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