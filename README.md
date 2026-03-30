# HidroCL — Hydroclimatological Database Maintainer

----

[![pythonversion](https://img.shields.io/badge/python-v3.10-blue?style=plastic&logo=python&logoColor=yellow)](https://www.python.org/downloads/release/python-3100/)
![packageversion](https://img.shields.io/badge/version-v0.0.37-blue?style=plastic)

**HidroCL** is a Python library for downloading, pre-processing, and extracting hydrometeorological variables from satellite and climate reanalysis products, in order to build and maintain geospatial databases at the catchment scale for Chile.

Developed by the Universidad de Valparaíso and Universidad de La Serena, with funding from ANID through FONDEF IDeA I+D ID21i10093.

**Python minimum version**: 3.10

---

## Installation

```bash
pip install git+https://github.com/MeteorologiaUV/HidroCL-OOP/
```

---

## Modules

| Module | Description |
|---|---|
| `hidrocl.variables` | Management and querying of hydrometeorological variable databases |
| `hidrocl.download` | Download of satellite products and climate reanalysis data |
| `hidrocl.preprocess` | Pre-processing of raw data before extraction |
| `hidrocl.products` | Zonal statistics extraction per catchment |
| `hidrocl.paths` | Path management for databases, products, logs, and vectors |

---

## Supported products

| Category | Product | Class |
|---|---|---|
| Vegetation | MOD13Q1, VNP13Q1 | `Mod13q1`, `Vnp13q1`, `Mod13q1agr`, `Vnp13q1agr` |
| Snow | MOD10A1F, VNP10A1F, MOD10A2 | `Mod10a1f`, `Vnp10a1f`, `Mod10a2` |
| Evapotranspiration | MOD16A2 | `Mod16a2` |
| Land cover | MCD12Q1 | `Mod12q1` |
| Leaf area index | MCD15A2H, VNP15A2H | `Mcd15a2h`, `Vnp15a2h` |
| Precipitation (observed) | GPM IMERG, IMERG GIS, PDIR-NOW | `Gpm_3imrghhl`, `ImergGIS`, `Pdirnow` |
| ERA5 reanalysis | ERA5 hourly | `Era5`, `Era5ppmax`, `Era5pplen`, `Era5_pressure`, `Era5_rh` |
| ERA5-Land reanalysis | ERA5-Land hourly | `Era5_land` |
| GFS forecast | GFS 0.25° | `Gfs` |
| GLDAS reanalysis | GLDAS Noah | `Gldas_noah` |

---

## Configuration

### Set project path

```python
import hidrocl
hidrocl.set_project_path('/path/to/project')
```

### Project directory structure

The project path must follow this structure:

```
project/
├── base/
│   └── boundaries/
│       ├── Agr_ModisSinu.shp
│       ├── HidroCL_boundaries.shp
│       ├── HidroCL_boundaries_sinu.shp
│       ├── HidroCL_boundaries_utm.shp
│       ├── HidroCL_north.shp
│       └── HidroCL_south.shp
├── databases/
│   ├── forecasted/
│   └── observed/
├── logs/
├── pcdatabases/
│   ├── forecasted/
│   └── observed/
└── products/
    └── observed/
```

### Credentials

Two credential files are required in the home directory:

**CDSAPI** (for ERA5/Copernicus products) — `~/.cdsapirc`:
```
url: https://cds.climate.copernicus.eu/api/v2
key: XXXXXXXXXXX
```

**Earthdata** (for MODIS, VIIRS, and GPM products) — `~/.netrc`:
```
machine urs.earthdata.nasa.gov
    login XXXXXXXXXXX
    password XXXXXXXXXXX
```

The server scripts also require a `.env` file in `workflow/server/`:
```
PROJECT_PATH=/path/to/project
DOWNLOAD_SCRIPT_PATH=/path/to/workflow/server
DOWNLOAD_LOG_PATH=/path/to/logs
```

---

## Usage

### Creating a variable

```python
import hidrocl
import hidrocl.paths as hcl

# Enable automatic database creation if files do not exist
hidrocl.variables.create = True

ndvi = hidrocl.HidroCLVariable(
    "ndvi",
    hcl.veg_o_modis_ndvi_mean_b_d16_p0d,
    hcl.veg_o_modis_ndvi_mean_pc
)
```

### Extracting data

```python
import hidrocl
import hidrocl.paths as hcl

ndvi = hidrocl.HidroCLVariable("ndvi",
                               hcl.veg_o_modis_ndvi_mean_b_d16_p0d,
                               hcl.veg_o_modis_ndvi_mean_pc)
evi  = hidrocl.HidroCLVariable("evi",
                               hcl.veg_o_modis_evi_mean_b_d16_p0d,
                               hcl.veg_o_modis_evi_mean_pc)
nbr  = hidrocl.HidroCLVariable("nbr",
                               hcl.veg_o_int_nbr_mean_b_d16_p0d,
                               hcl.veg_o_int_nbr_mean_pc)

mod13 = hidrocl.Mod13q1(ndvi, evi, nbr,
                        product_path=hcl.mod13q1_path,
                        vector_path=hcl.hidrocl_sinusoidal,
                        ndvi_log=hcl.log_veg_o_modis_ndvi_mean,
                        evi_log=hcl.log_veg_o_modis_evi_mean,
                        nbr_log=hcl.log_veg_o_int_nbr_mean)

mod13.run_maintainer()
mod13.run_extraction()
```

### VIIRS example

```python
import hidrocl
import hidrocl.paths as hcl

ndvi = hidrocl.HidroCLVariable("ndvi",
                               hcl.veg_o_viirs_ndvi_mean,
                               hcl.veg_o_viirs_ndvi_mean_pc)
evi  = hidrocl.HidroCLVariable("evi",
                               hcl.veg_o_viirs_evi_mean,
                               hcl.veg_o_viirs_evi_mean_pc)
nbr  = hidrocl.HidroCLVariable("nbr",
                               hcl.veg_o_viirs_nbr2_mean,
                               hcl.veg_o_viirs_nbr2_mean_pc)

vnp13 = hidrocl.Vnp13q1(ndvi, evi, nbr,
                        product_path=hcl.vnp13q1_path,
                        vector_path=hcl.hidrocl_sinusoidal,
                        ndvi_log=hcl.log_veg_o_viirs_indices_mean,
                        evi_log=hcl.log_veg_o_viirs_indices_mean,
                        nbr_log=hcl.log_veg_o_viirs_indices_mean)

vnp13.run_maintainer()
vnp13.run_extraction()
```

### Running the full operational workflow

```bash
cd workflow/server/
python run_all.py   # all satellite + reanalysis products (MODIS, VIIRS, IMERG, ERA5, ERA5-Land)
python run_gfs.py   # GFS forecast (handles retries automatically)
```

---

## Workflow structure

```
workflow/
├── download/       — download scripts for each data source
├── maintain/       — database maintenance (remove corrupt files)
├── organize/       — file organization (move to year subfolders)
├── preprocess/     — ERA5 relative humidity pre-processing
├── process/        — standalone extraction scripts per product
└── server/         — operational scripts integrating download + extraction
    ├── era5.py
    ├── era5land.py
    ├── era5pl.py
    ├── gfs.py
    ├── imerggis.py
    ├── mcd15a2h.py
    ├── mod10a2.py
    ├── mod13q1.py
    ├── pdirnow.py
    ├── run_all.py
    ├── run_gfs.py
    ├── vnp10a1f.py
    ├── vnp13q1.py
    └── vnp15a2h.py
```

---

## Dependencies

```
pandas>=1.4.3
rioxarray>=0.12.0
matplotlib>=3.5.3
geopandas>=0.11.1
netCDF4>=1.6.0
cdsapi>=0.7.3
earthaccess>=0.8.1
beautifulsoup4>=4.11.1
rasterio>=1.3.2
numpy>=1.23.2
xarray>=0.20.1
requests>=2.32
setuptools>=63.4.1
wget>=3.2
exactextract>=0.2.0.dev0
python-dotenv>=1.0.0
ecCodes>=2.44.0
cfgrib~=0.9.15.1
```
