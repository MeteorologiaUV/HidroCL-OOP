import hidrocl
import hidrocl_paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

v = gpd.read_file(hcl.hidrocl_agr_sinu)
catchment_names = v.gauge_id.tolist()

agr = hidrocl.HidroCLVariable('agr NDVI',
                              hcl.veg_o_modis_agr_mean_b_none_d1_p0d,
                              hcl.veg_o_modis_agr_mean_b_pc)

agr.catchment_names = v.gauge_id.tolist()

agr.checkdatabase()
agr.checkpcdatabase()

agrndvi = hidrocl.Mod13q1agr(ndvi = agr, product_path=hcl.mod13q1_path,
                             vector_path=hcl.hidrocl_agr_sinu,
                             ndvi_log=hcl.log_veg_o_agr_ndvi_mean)

agrndvi.run_extraction()
