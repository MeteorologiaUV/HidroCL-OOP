# How-to guides

## How to add a new variable database

Use `HidroCLVariable` to bind a variable name to its CSV database files. Enable automatic creation if the files don't exist yet:

```python
import hidrocl
import hidrocl.paths as hcl

hidrocl.variables.create = True

ndvi = hidrocl.HidroCLVariable(
    "ndvi",
    hcl.veg_o_modis_ndvi_mean_b_d16_p0d,   # observations database
    hcl.veg_o_modis_ndvi_mean_pc            # pixel-count database
)
```

---

## How to extract MODIS vegetation indices (MOD13Q1)

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

mod13.run_maintainer()   # verify files, remove corrupt ones
mod13.run_extraction()   # extract zonal statistics
```

---

## How to extract VIIRS vegetation indices (VNP13Q1)

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

---

## How to extract snow cover (VNP10A1F — VIIRS daily)

```python
import hidrocl
import hidrocl.paths as hcl

nsnow = hidrocl.HidroCLVariable("nsnow",
                                hcl.snw_o_viirs_scaf_cum_n,
                                hcl.snw_o_viirs_scaf_cum_n_pc)
ssnow = hidrocl.HidroCLVariable("ssnow",
                                hcl.snw_o_viirs_scaf_cum_s,
                                hcl.snw_o_viirs_scaf_cum_s_pc)

vnp10 = hidrocl.Vnp10a1f(nsnow, ssnow,
                         product_path=hcl.vnp10a1f_path,
                         north_vector_path=hcl.hidrocl_north,
                         south_vector_path=hcl.hidrocl_south,
                         snow_log=hcl.log_snw_o_viirs_sca_cum)

vnp10.run_maintainer()
vnp10.run_extraction()
```

---

## How to extract LAI and FPAR (VNP15A2H — VIIRS 8-day)

```python
import hidrocl
import hidrocl.paths as hcl

lai  = hidrocl.HidroCLVariable("lai",
                               hcl.veg_o_viirs_lai_mean,
                               hcl.veg_o_viirs_lai_mean_pc)
fpar = hidrocl.HidroCLVariable("fpar",
                               hcl.veg_o_viirs_fpar_mean,
                               hcl.veg_o_viirs_fpar_mean_pc)

vnp15 = hidrocl.Vnp15a2h(lai, fpar,
                         product_path=hcl.vnp15a2h_path,
                         vector_path=hcl.hidrocl_sinusoidal,
                         lai_log=hcl.log_veg_o_viirs_lai_mean,
                         fpar_log=hcl.log_veg_o_viirs_fpar_mean)

vnp15.run_maintainer()
vnp15.run_extraction()
```

---

## How to download ERA5-Land data

```python
import hidrocl

hidrocl.download.download_era5land(
    year=2026, month=3, day=1,
    path='/data/era5land/'
)
```

---

## How to download MODIS/VIIRS products via Earthdata

```python
import hidrocl

# MODIS vegetation (MOD13Q1)
hidrocl.download.earthdata_download(
    'vegetation', '/data/mod13q1/', '2026-01-01', '2026-03-01'
)

# VIIRS snow (VNP10A1F)
hidrocl.download.viirs_download(
    'snow', '/data/vnp10a1f/', '2026-01-01', '2026-03-01',
    bbox=(-73.73, -55.01, -67.05, -17.63)
)
```

Available `what` values for `earthdata_download`: `reflectance`, `vegetation`, `lai`, `albedo`, `lulc`, `et0`, `snow`, `precipitation`, `landdata`.

Available `what` values for `viirs_download`: `snow`, `vegetation`, `lai`, `reflectance`.

---

## How to run the full operational workflow

```bash
cd workflow/server/
python run_all.py   # MODIS, VIIRS, IMERG, ERA5, ERA5-Land (sequential)
python run_gfs.py   # GFS (with automatic retries every 10 min, up to 72 attempts)
```

Exit codes returned by each script:

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Error |
| `4` | Database already up to date |
| `5` | Insufficient data to process |

---

## How to check database status

```python
import hidrocl
import hidrocl.paths as hcl

ndvi = hidrocl.HidroCLVariable("ndvi",
                               hcl.veg_o_modis_ndvi_mean_b_d16_p0d,
                               hcl.veg_o_modis_ndvi_mean_pc)

# Number of records in the database
print(ndvi)

# Valid data percentage per catchment
print(ndvi.valid_data())

# Visualise valid data
ndvi.plot_valid_data_all()
```
