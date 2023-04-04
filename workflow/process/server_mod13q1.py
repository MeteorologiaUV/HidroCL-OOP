import hidrocl
import hidrocl.paths as hcl
print(hidrocl.__version__)

ndvi = hidrocl.HidroCLVariable("ndvi",
                               hcl.veg_o_modis_ndvi_mean_b_d16_p0d,
                               hcl.veg_o_modis_ndvi_mean_pc)

evi = hidrocl.HidroCLVariable("evi",
                              hcl.veg_o_modis_evi_mean_b_d16_p0d,
                              hcl.veg_o_modis_evi_mean_pc)

nbr = hidrocl.HidroCLVariable("nbr",
                              hcl.veg_o_int_nbr_mean_b_d16_p0d,
                              hcl.veg_o_int_nbr_mean_pc)

mod13 = hidrocl.Mod13q1(ndvi, evi, nbr,
                        product_path=hcl.mod13q1_path,
                        vector_path=hcl.hidrocl_sinusoidal,
                        ndvi_log=hcl.log_veg_o_modis_ndvi_mean,
                        evi_log=hcl.log_veg_o_modis_evi_mean,
                        nbr_log=hcl.log_veg_o_int_nbr_mean)

mod13.run_extraction()