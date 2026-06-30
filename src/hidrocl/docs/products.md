# Product processors

Classes for extracting zonal statistics from satellite and reanalysis products at the catchment scale. Each class receives one or more `HidroCLVariable` objects and provides two main methods:

- **`run_extraction()`** — processes all pending scenes and writes results to the linked CSV databases.
- **`run_maintainer()`** — verifies product files (removes corrupt ones) and cleans the databases (removes duplicates, sorts by date).

Supported products: MOD13Q1, VNP13Q1, MOD10A2, MOD10A1F, VNP10A1F, MCD15A2H, VNP15A2H, MOD16A2, MCD12Q1, GPM IMERG, IMERG GIS, PDIR-NOW, ERA5, ERA5-Land, GFS, GLDAS.

::: hidrocl.products
