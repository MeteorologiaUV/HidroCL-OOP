import hidrocl
import hidrocl.paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

eto = hidrocl.HidroCLVariable("eto",
                              hcl.et_o_era5_eta_mean,
                              hcl.et_o_era5_eta_pc)

et = hidrocl.HidroCLVariable("et",
                             hcl.et_o_era5_eto_mean,
                             hcl.et_o_era5_eto_pc)

sca = hidrocl.HidroCLVariable("sca",
                              hcl.snw_o_era5_sca_mean,
                              hcl.snw_o_era5_sca_pc)

sna = hidrocl.HidroCLVariable("sna",
                              hcl.snw_o_era5_sna_mean,
                              hcl.snw_o_era5_sna_pc)
# density
snr = hidrocl.HidroCLVariable("snr",
                              hcl.snw_o_era5_snr_mean,
                              hcl.snw_o_era5_snr_pc)
# depth
snd = hidrocl.HidroCLVariable("snd",
                              hcl.snw_o_era5_snd_mean,
                              hcl.snw_o_era5_snd_pc)

sm = hidrocl.HidroCLVariable("sm",
                             hcl.swc_o_era5_sm_mean,
                             hcl.swc_o_era5_sm_pc)

v = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = v.gauge_id.tolist()

eto.catchment_names = catchment_names
et.catchment_names = catchment_names
sca.catchment_names = catchment_names
sna.catchment_names = catchment_names
snr.catchment_names = catchment_names
snd.catchment_names = catchment_names
sm.catchment_names = catchment_names

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

era5 = hidrocl.Era5_land(et=et, pet=eto,
                         snw=sca, snwa=sna,
                         snwdn=snr, snwdt=snd, soilm=sm,
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
