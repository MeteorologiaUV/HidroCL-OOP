import hidrocl
import hidrocl.paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

pp = hidrocl.HidroCLVariable("pp",
                             hcl.pp_o_pers_pp_mean_b_d_p0d,
                             hcl.pp_o_pers_pp_mean_b_pc)

v = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = v.gauge_id.tolist()

pp.catchment_names = catchment_names

pp.checkdatabase()
pp.checkpcdatabase()

persiann = hidrocl.Persiann_ccs(pp, product_path=hcl.persiann,
                                vector_path=hcl.hidrocl_wgs84,
                                pp_log=hcl.log_pp_o_pers_pp_mean)

persiann.run_extraction()
