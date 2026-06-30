# Download functions

Functions for downloading satellite products, climate reanalysis data, and meteorological forecasts from their respective sources.

| Function | Source | Protocol |
|---|---|---|
| `download_era5` | Copernicus CDS | CDSAPI |
| `download_era5land` | Copernicus CDS | CDSAPI |
| `download_era5pressure` | Copernicus CDS | CDSAPI |
| `earthdata_download` | NASA Earthdata | earthaccess |
| `viirs_download` | NASA Earthdata | earthaccess |
| `get_imerg` / `download_imerg` | NASA GES DISC | HTTPS |
| `download_pdirnow` | CHRS UC Irvine | web scraping |
| `gfs_download` | NOAA NOMADS | GRIB/HTTPS |

Credentials must be configured before use. See the [Home](index.md) page for credential setup.

::: hidrocl.download
