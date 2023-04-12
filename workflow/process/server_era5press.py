import hidrocl
import hidrocl.paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

gh = hidrocl.HidroCLVariable("gh",
                             hcl.atm_o_era5_z_mean_b_none_d1_p0d,
                             hcl.atm_o_era5_z_mean_b_pc)

v = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = v.gauge_id.tolist()

gh.catchment_names = catchment_names

gh.checkdatabase()
gh.checkpcdatabase()

era5 = hidrocl.Era5_pressure(z=gh,
                             z_log=hcl.log_atm_o_era5_z_mean,
                             product_path=hcl.era5_pressure_levels_hourly_path,
                             vector_path=hcl.hidrocl_wgs84)

era5.run_extraction()
