import hidrocl
import hidrocl_paths as hcl
print(hidrocl.__version__)

pp = hidrocl.HidroCLVariable("pp",
                             hcl.pp_o_imerg_pp_mean_b_d_p0d,
                             hcl.pp_o_imerg_pp_mean_b_pc)

snow = hidrocl.HidroCLVariable("snow", hcl.snw_o_gldas_swe_cum_b_d8_p0d, hcl.snw_o_gldas_swe_cum_b_pc)
temp = hidrocl.HidroCLVariable("temp", hcl.tmp_f_gldas_tmp_mean_b_d_p0d, hcl.tmp_f_gldas_tmp_mean_b_pc)
et = hidrocl.HidroCLVariable("et", hcl.et_o_gldas_eta_cum_b_d0_p0d, hcl.et_o_gldas_eta_cum_b_pc)
soilm = hidrocl.HidroCLVariable("soilm", hcl.sm_o_gldas_sm_mean_b_d_p0d, hcl.sm_o_gldas_sm_mean_b_pc)

gldas = hidrocl.Gldas_noah(snow, temp, et, soilm,
                           product_path=hcl.gldas_noah025_3h_path,
                           vector_path=hcl.hidrocl_wgs84,
                           snow_log=hcl.log_snw_o_gldas_swe_cum,
                           temp_log=hcl.log_tmp_f_gldas_tmp_mean,
                           et_log=hcl.log_et_o_gldas_eta_cum,
                           soilm_log=hcl.log_sm_o_gldas_sm_mean)

gldas.run_maintainer(hcl.log_file_maintainer)