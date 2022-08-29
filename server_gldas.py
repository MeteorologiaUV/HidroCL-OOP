import hidrocl
import hidrocl_paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

v = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = v.gauge_id.tolist()

pp = hidrocl.HidroCLVariable("pp",
                             hcl.pp_o_imerg_pp_mean_b_d_p0d,
                             hcl.pp_o_imerg_pp_mean_b_pc)

snow = hidrocl.HidroCLVariable("snow", hcl.snw_o_gldas_swe_cum_b_d8_p0d, hcl.snw_o_gldas_swe_cum_b_pc)
temp = hidrocl.HidroCLVariable("temp", hcl.tmp_f_gldas_tmp_mean_b_d_p0d, hcl.tmp_f_gldas_tmp_mean_b_pc)
et = hidrocl.HidroCLVariable("et", hcl.et_o_gldas_eta_cum_b_d0_p0d, hcl.et_o_gldas_eta_cum_b_pc)
soilm = hidrocl.HidroCLVariable("soilm", hcl.sm_o_gldas_sm_mean_b_d_p0d, hcl.sm_o_gldas_sm_mean_b_pc)

snow.catchment_names = catchment_names
temp.catchment_names = catchment_names
et.catchment_names = catchment_names
soilm.catchment_names = catchment_names

snow.checkdatabase()
snow.checkpcdatabase()
temp.checkdatabase()
temp.checkpcdatabase()
et.checkdatabase()
et.checkpcdatabase()
soilm.checkdatabase()
soilm.checkpcdatabase()

gldas = hidrocl.Gldas_noah(snow, temp, et, soilm,
                           product_path=hcl.gldas_noah025_3h_path,
                           vector_path=hcl.hidrocl_wgs84,
                           snow_log=hcl.log_snw_o_gldas_swe_cum,
                           temp_log=hcl.log_tmp_f_gldas_tmp_mean,
                           et_log=hcl.log_et_o_gldas_eta_cum,
                           soilm_log=hcl.log_sm_o_gldas_sm_mean)

gldas.run_extraction()
