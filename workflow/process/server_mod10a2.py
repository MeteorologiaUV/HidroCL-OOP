import hidrocl
import hidrocl.paths as hcl
print(hidrocl.__version__)

nsnow = hidrocl.HidroCLVariable("nsnow",
                                hcl.snw_o_modis_sca_cum_n_d8_p0d,
                                hcl.snw_o_modis_sca_cum_n_pc)

ssnow = hidrocl.HidroCLVariable("ssnow",
                                hcl.snw_o_modis_sca_cum_s_d8_p0d,
                                hcl.snw_o_modis_sca_cum_s_pc)

mod10 = hidrocl.Mod10a2(nsnow, ssnow,
                        product_path=hcl.mod10a2_path,
                        north_vector_path=hcl.hidrocl_north,
                        south_vector_path=hcl.hidrocl_south,
                        snow_log=hcl.log_snw_o_modis_sca_cum)

mod10.run_extraction()
