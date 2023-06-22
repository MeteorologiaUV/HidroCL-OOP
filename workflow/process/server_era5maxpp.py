import hidrocl
import hidrocl.paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

maxpp = hidrocl.HidroCLVariable("maxpp",
                                hcl.pp_o_era5_maxpp_mean,
                                hcl.pp_o_era5_maxpp_pc)

vc = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = vc.gauge_id.tolist()

maxpp.catchment_names = catchment_names

maxpp.checkdatabase()
maxpp.checkpcdatabase()

era5 = hidrocl.Era5ppmax(ppmax=maxpp, ppmax_log=hcl.log_pp_o_era5_maxpp_mean,
                         product_path=hcl.era5_hourly_path,
                         vector_path=hcl.hidrocl_wgs84)
era5.run_extraction()
