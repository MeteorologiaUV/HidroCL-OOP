# Preprocessing

Pre-processing classes for deriving variables from raw downloaded data before extraction.

Currently the module provides relative humidity computation from ERA5 hourly data. The `Era5_pre_rh` class reads ERA5 NetCDF files containing 2-metre temperature (`t2m`) and dew-point temperature (`d2m`), computes hourly relative humidity using the Magnus formula, and writes the result as new NetCDF files ready for extraction by `Era5_rh`.

::: hidrocl.preprocess
