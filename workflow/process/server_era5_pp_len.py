import hidrocl
import hidrocl.paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

pp = hidrocl.HidroCLVariable("pp",
                             hcl.pp_o_era5_plen_mean_b_d1_p0d,
                             hcl.pp_o_era5_plen_mean_b_pc)

vc = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = vc.gauge_id.tolist()

pp.catchment_names = catchment_names

pp.checkdatabase()
pp.checkpcdatabase()


era5 = hidrocl.Era5pplen(pplen=pp,
                         product_path=hcl.era5_hourly_path,
                         vector_path=hcl.hidrocl_wgs84,
                         pplen_log=hcl.log_pp_o_era5_plen_mean)

era5.run_extraction()
