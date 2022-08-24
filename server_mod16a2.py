import hidrocl
import hidrocl_paths as hcl
print(hidrocl.__version__)

pet = hidrocl.HidroCLVariable("pet",
                               hcl.et_o_modis_eto_cum_b_d8_p0d,
                               hcl.et_o_modis_eto_cum_b_pc)

mod16 = hidrocl.Mod16a2(pet,
                        product_path=hcl.mod16a2_path,
                        vector_path=hcl.hidrocl_sinusoidal,
                        pet_log=hcl.log_veg_o_modis_ndvi_mean)

mod16.run_extraction()