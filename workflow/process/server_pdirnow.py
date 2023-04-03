import hidrocl
import hidrocl_paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

pp = hidrocl.HidroCLVariable("pp",
                             hcl.pp_o_pdir_pp_mean_b_none_d1_p0d,
                             hcl.pp_o_pdir_pp_mean_b_pc)

v = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = v.gauge_id.tolist()

pp.catchment_names = catchment_names

pp.checkdatabase()
pp.checkpcdatabase()

pdirnow = hidrocl.Pdirnow(pp, product_path=hcl.pdirnow,
                          vector_path=hcl.hidrocl_wgs84,
                          pp_log=hcl.log_pp_o_pdir_pp_mean)

pdirnow.run_extraction()
