import hidrocl
import hidrocl_paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

temp = hidrocl.HidroCLVariable("temp",
                               hcl.tmp_o_era5_tmp_mean_b_none_d1_p0d,
                               hcl.tmp_o_era5_tmp_mean_b_pc)

tempmin = hidrocl.HidroCLVariable("tempmin",
                               hcl.tmp_o_era5_tmp_min_b_none_d1_p0d,
                               hcl.tmp_o_era5_tmp_min_b_pc)

tempmax = hidrocl.HidroCLVariable("tempmax",
                               hcl.tmp_o_era5_tmp_max_b_none_d1_p0d,
                               hcl.tmp_o_era5_tmp_max_b_pc)

pp = hidrocl.HidroCLVariable("pp",
                             hcl.pp_o_era5_pp_mean_b_d_p0d,
                             hcl.pp_o_era5_pp_mean_b_pc)

eto = hidrocl.HidroCLVariable("eto",
                              hcl.et_o_era5_eto_cum_b_d_p0d,
                              hcl.et_o_gldas_eta_cum_b_pc)

et = hidrocl.HidroCLVariable("et",
                             hcl.et_o_era5_et_cum_b_d_p0d,
                             hcl.et_o_era5_et_cum_b_pc)

sca = hidrocl.HidroCLVariable("sca",
                              hcl.snow_o_era5_sca_mean_b_d_p0d,
                              hcl.snow_o_era5_sca_mean_b_pc)

sna = hidrocl.HidroCLVariable("sna",
                              hcl.snow_o_era5_sna_mean_b_d_p0d,
                              hcl.snow_o_era5_sna_mean_b_pc)

snr = hidrocl.HidroCLVariable("snr",
                              hcl.snow_o_era5_snr_mean_b_d_p0d,
                              hcl.snow_o_era5_snr_mean_b_pc)

snd = hidrocl.HidroCLVariable("snd",
                              hcl.snow_o_era5_snd_mean_b_d_p0d,
                              hcl.snow_o_era5_snd_mean_b_pc)

sm = hidrocl.HidroCLVariable("sm",
                             hcl.sm_o_era5_sm_mean_b_d_p0d,
                             hcl.sm_o_era5_sm_mean_b_pc)

v = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = v.gauge_id.tolist()

pp.catchment_names = catchment_names
temp.catchment_names = catchment_names
tempmin.catchment_names = catchment_names
tempmax.catchment_names = catchment_names
eto.catchment_names = catchment_names
et.catchment_names = catchment_names
sca.catchment_names = catchment_names
sna.catchment_names = catchment_names
snr.catchment_names = catchment_names
snd.catchment_names = catchment_names
sm.catchment_names = catchment_names

pp.checkdatabase()
pp.checkpcdatabase()
temp.checkdatabase()
temp.checkpcdatabase()
tempmin.checkdatabase()
tempmin.checkpcdatabase()
tempmax.checkdatabase()
tempmax.checkpcdatabase()
eto.checkdatabase()
eto.checkpcdatabase()
et.checkdatabase()
et.checkpcdatabase()
sca.checkdatabase()
sca.checkpcdatabase()
sna.checkdatabase()
sna.checkpcdatabase()
snr.checkdatabase()
snr.checkpcdatabase()
snd.checkdatabase()
snd.checkpcdatabase()
sm.checkdatabase()
sm.checkpcdatabase()

era5 = hidrocl.Era5_land(temp=temp, tempmin=tempmin,
                         tempmax=tempmax, pp=pp,
                         et=et, pet=eto,
                         snw=sca, snwa=sna,
                         snwdn=snr, snwdt=snd,soilm=sm,
                         pp_log=hcl.log_pp_o_era5_pp_mean,
                         temp_log=hcl.log_tmp_o_era5_tmp_mean,
                         tempmin_log=hcl.log_tmp_o_era5_tmp_min,
                         tempmax_log=hcl.log_tmp_o_era5_tmp_max,
                         et_log=hcl.log_et_o_era5_et_cum,
                         pet_log=hcl.log_et_o_era5_eto_cum,
                         snw_log=hcl.log_snow_o_era5_sca,
                         snwa_log=hcl.log_snow_o_era5_sna,
                         snwdn_log=hcl.log_snow_o_era5_snr,
                         snwdt_log=hcl.log_snow_o_era5_snd,
                         soilm_log=hcl.log_sm_o_era5_sm_mean,
                         product_path=hcl.era5_land_hourly_path,
                         vector_path=hcl.hidrocl_wgs84)

era5.run_extraction()
