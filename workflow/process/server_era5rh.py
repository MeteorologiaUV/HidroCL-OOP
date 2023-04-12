import hidrocl
import hidrocl.paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

rh = hidrocl.HidroCLVariable("rh",
                             hcl.awc_o_era5_rh_mean_b_none_d1_p0d,
                             hcl.awc_o_era5_rh_mean_b_pc)

v = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = v.gauge_id.tolist()

rh.catchment_names = catchment_names

rh.checkdatabase()
rh.checkpcdatabase()

era5 = hidrocl.Era5_rh(rh=rh,
                       rh_log=hcl.log_awc_f_gfs_rh_mean_log,
                       product_path=hcl.era5_relative_humidity_path,
                       vector_path=hcl.hidrocl_wgs84)

era5.run_extraction()
