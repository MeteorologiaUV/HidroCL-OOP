import hidrocl
import hidrocl_paths as hcl
print(hidrocl.__version__)

lai = hidrocl.HidroCLVariable("lai",
                              hcl.veg_o_modis_lai_mean_b_d8_p0d,
                              hcl.veg_o_modis_lai_mean_b_pc)

fpar = hidrocl.HidroCLVariable("fpar",
                               hcl.veg_o_modis_fpar_mean_b_d8_p0d,
                               hcl.veg_o_modis_fpar_mean_b_pc)

mcd15 = hidrocl.Mcd15a2h(lai, fpar,
                         product_path=hcl.mcd15a2h_path,
                         vector_path=hcl.hidrocl_sinusoidal,
                         lai_log=hcl.log_veg_o_modis_lai_mean,
                         fpar_log=hcl.log_veg_o_modis_fpar_mean)

mcd15.run_extraction()
