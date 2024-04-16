import os

from .. import project_path, observed_products_path, forecasted_products_path, processing_path

mcd12q1_path = os.path.join(processing_path, observed_products_path, 'MCD12Q1/')  # lulc
mcd15a2h_path = os.path.join(processing_path, observed_products_path, 'MCD15A2H/')  # lai/fpar
mcd43a3_path = os.path.join(processing_path, observed_products_path, 'MCD43A3/')  # albedo
mod10a2_path = os.path.join(processing_path, observed_products_path, 'MOD10A2/')  # snow
mod13q1_path = os.path.join(processing_path, observed_products_path, 'MOD13Q1/')  # vegetation
mod16a2_path = os.path.join(processing_path, observed_products_path, 'MOD16A2/')  # et
# imerghhl_path = os.path.join(processing_path, observed_products_path, 'GPM_3IMERGHHL/')  # pp + other
imerggis_path = os.path.join(processing_path, observed_products_path, 'IMERG_GIS')  # pp
persiann = os.path.join(processing_path, observed_products_path, 'PERSIANN/')  # pp
gldas_noah025_3h_path = os.path.join(processing_path, observed_products_path, 'GLDAS_NOAH025_3H/')  # land data
era5_land_hourly_path = os.path.join(processing_path, observed_products_path, 'ERA5_LAND_HOURLY/')  # era5 land data
era5_hourly_path = os.path.join(processing_path, observed_products_path, 'ERA5_HOURLY/')  # era5 data
era5_pressure_levels_hourly_path = os.path.join(processing_path, observed_products_path,
                                                'ERA5_PRESSURE_LEVELS_HOURLY/')  # era5 pressure levels data
era5_relative_humidity_path = os.path.join(processing_path, observed_products_path,
                                           'ERA5_RH/')  # era5 pressure levels data
satellite_soil_moisture = os.path.join(processing_path, observed_products_path,
                                       'SATELLITE_SOIL_MOISTURE/')  # satellite soil moisture
pdirnow = os.path.join(processing_path, observed_products_path, 'PDIRNOW/')  # pdirnow

# forecasted
gfs = os.path.join(processing_path, forecasted_products_path)  # only forecasted variable

# path to files
hidrocl_sinusoidal = os.path.join(project_path,
                                  'base/boundaries/HidroCL_boundaries_sinu.shp')  # polys with sinusoidal projection
hidrocl_utm = os.path.join(project_path, 'base/boundaries/HidroCL_boundaries_utm.shp')
hidrocl_wgs84 = os.path.join(project_path, 'base/boundaries/HidroCL_boundaries.shp')
hidrocl_north = os.path.join(project_path, 'base/boundaries/HidroCL_north.shp')
hidrocl_south = os.path.join(project_path, 'base/boundaries/HidroCL_south.shp')
hidrocl_agr_sinu = os.path.join(project_path, 'base/boundaries/Agr_ModisSinu.shp')

# ----
# databases
# ----
# static
# not for this module

# new variables
pp_o_pdir_pp_mean_b_none_d1_p0d = os.path.join(project_path, 'databases/observed/pp_o_pdir_pp_mean_b_none_d1_p0d.csv')

# observed
snw_o_modis_sca_cum_n_d8_p0d = os.path.join(project_path, 'databases/observed/snw_o_modis_sca_tot_n_none_d1_p0d.csv')
snw_o_modis_sca_cum_s_d8_p0d = os.path.join(project_path, 'databases/observed/snw_o_modis_sca_tot_s_none_d1_p0d.csv')
veg_o_modis_ndvi_mean_b_d16_p0d = os.path.join(project_path,
                                               'databases/observed/veg_o_modis_ndvi_mean_b_none_d1_p0d.csv')
veg_o_modis_evi_mean_b_d16_p0d = os.path.join(project_path, 'databases/observed/veg_o_modis_evi_mean_b_none_d1_p0d.csv')
veg_o_int_nbr_mean_b_d16_p0d = os.path.join(project_path, 'databases/observed/veg_o_modis_nbr_mean_b_none_d1_p0d.csv')
# sun_o_modis_al_mean_b_d16_p0d = os.path.join(nas_path, 'databases/observed/sun_o_modis_al_mean_b_d16_p0d.csv')
# sun_o_modis_al_p10_b_d16_p0d = os.path.join(nas_path, 'databases/observed/sun_o_modis_al_p10_b_d16_p0d.csv')
# sun_o_modis_al_p25_b_d16_p0d = os.path.join(nas_path, 'databases/observed/sun_o_modis_al_p25_b_d16_p0d.csv')
# sun_o_modis_al_median_b_d16_p0d = os.path.join(nas_path, 'databases/observed/sun_o_modis_al_median_b_d16_p0d.csv')
# sun_o_modis_al_p75_b_d16_p0d = os.path.join(nas_path, 'databases/observed/sun_o_modis_al_p75_b_d16_p0d.csv')
# sun_o_modis_al_p90_b_d16_p0d = os.path.join(nas_path, 'databases/observed/sun_o_modis_al_p90_b_d16_p0d.csv')
et_o_modis_eto_cum_b_d8_p0d = os.path.join(project_path, 'databases/observed/et_o_modis_eto_cum_b_d8_p0d.csv')
et_o_modis_eta_cum_b_d8_p0d = os.path.join(project_path, 'databases/observed/et_o_modis_eta_cum_b_d8_p0d.csv')
veg_o_modis_lai_mean_b_d8_p0d = os.path.join(project_path, 'databases/observed/veg_o_modis_lai_mean_b_d8_p0d.csv')
veg_o_modis_fpar_mean_b_d8_p0d = os.path.join(project_path, 'databases/observed/veg_o_modis_fpar_mean_b_d8_p0d.csv')
pp_o_imerg_pp_mean_b_d_p0d = os.path.join(project_path, 'databases/observed/pp_o_imerg_pp_mean_b_none_d1_p0d.csv')
# GLDAS products:
snw_o_gldas_swe_cum_b_d8_p0d = os.path.join(project_path, 'databases/observed/snw_o_gldas_swe_cum_b_d8_p0d.csv')
tmp_f_gldas_tmp_mean_b_d_p0d = os.path.join(project_path, 'databases/observed/tmp_f_gldas_tmp_mean_b_d_p0d.csv')
et_o_gldas_eta_cum_b_d0_p0d = os.path.join(project_path, 'databases/observed/et_o_gldas_eta_cum_b_d0_p0d.csv')
sm_o_gldas_sm_mean_b_d_p0d = os.path.join(project_path, 'databases/observed/sm_o_gldas_sm_mean_b_d_p0d.csv')
pp_o_pers_pp_mean_b_d_p0d = os.path.join(project_path, 'databases/observed/pp_o_pers_pp_mean_b_d_p0d.csv')
pp_o_pcdr_pp_mean_b_d_p0d = os.path.join(project_path, 'databases/observed/pp_o_pcdr_pp_mean_b_d_p0d.csv')
# ERA5 products:
tmp_o_era5_tmp_mean_b_none_d1_p0d = os.path.join(project_path,
                                                 'databases/observed/tmp_o_era5_tmp_mean_b_none_d1_p0d.csv')
tmp_o_era5_tmp_min_b_none_d1_p0d = os.path.join(project_path, 'databases/observed/tmp_o_era5_tmp_min_b_none_d1_p0d.csv')
tmp_o_era5_tmp_max_b_none_d1_p0d = os.path.join(project_path, 'databases/observed/tmp_o_era5_tmp_max_b_none_d1_p0d.csv')
pp_o_era5_pp_mean_b_d_p0d = os.path.join(project_path, 'databases/observed/pp_o_era5_pp_mean_b_d_p0d.csv')
et_o_era5_eto_cum_b_d_p0d = os.path.join(project_path, 'databases/observed/et_o_era5_eto_cum_b_d_p0d.csv')
et_o_era5_et_cum_b_d_p0d = os.path.join(project_path, 'databases/observed/et_o_era5_et_cum_b_d_p0d.csv')
snow_o_era5_sca_mean_b_d_p0d = os.path.join(project_path, 'databases/observed/snow_o_era5_sca_mean_b_d_p0d.csv')
snow_o_era5_sna_mean_b_d_p0d = os.path.join(project_path,
                                            'databases/observed/snow_o_era5_sna_mean_b_d_p0d.csv')  # snow albedo
snow_o_era5_snr_mean_b_d_p0d = os.path.join(project_path,
                                            'databases/observed/snow_o_era5_snr_mean_b_d_p0d.csv')  # snow density
snow_o_era5_snd_mean_b_d_p0d = os.path.join(project_path,
                                            'databases/observed/snow_o_era5_snd_mean_b_d_p0d.csv')  # snow depth
sm_o_era5_sm_mean_b_d_p0d = os.path.join(project_path,
                                         'databases/observed/sm_o_era5_sm_mean_b_d_p0d.csv')  # soil moisture
pp_o_pdir_pp_mean_b_none_d1_p0d = os.path.join(project_path,
                                               'databases/observed/pp_o_pdir_pp_mean_b_none_d1_p0d.csv')  # new persiann
pp_o_era5_plen_mean_b_d1_p0d = os.path.join(project_path,
                                            'databases/observed/pp_o_era5_plen_mean_b_none_d1_p0d.csv')  # pp length

## new variables with new names
veg_o_modis_agr_mean_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/veg_o_modis_agr_mean_b_none_d1_p0d.csv')
pp_o_era5_pp_mean_b_none_d1_p0d = os.path.join(project_path, 'databases/observed/pp_o_era5_pp_mean_b_none_d1_p0d.csv')
tmp_o_era5_dew_mean_b_none_d1_p0d = os.path.join(project_path,
                                                 'databases/observed/tmp_o_era5_dew_mean_b_none_d1_p0d.csv')
wind_o_era5_u10_mean_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/wind_o_era5_u10_mean_b_none_d1_p0d.csv')
wind_o_era5_v10_mean_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/wind_o_era5_v10_mean_b_none_d1_p0d.csv')
atm_o_era5_pres_mean_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/atm_o_era5_pres_mean_b_none_d1_p0d.csv')
atm_o_era5_z_mean_b_none_d1_p0d = os.path.join(project_path, 'databases/observed/atm_o_era5_z_mean_b_none_d1_p0d.csv')
awc_o_era5_rh_mean_b_none_d1_p0d = os.path.join(project_path, 'databases/observed/awc_o_era5_rh_mean_b_none_d1_p0d.csv')

# forecasted
pp_f_gfs_pp_mean_b_none_d1_p0d = os.path.join(project_path, 'databases/forecasted/pp_f_gfs_pp_mean_b_none_d1_p0d.csv')
pp_f_gfs_pp_mean_b_none_d1_p1d = os.path.join(project_path, 'databases/forecasted/pp_f_gfs_pp_mean_b_none_d1_p1d.csv')
pp_f_gfs_pp_mean_b_none_d1_p2d = os.path.join(project_path, 'databases/forecasted/pp_f_gfs_pp_mean_b_none_d1_p2d.csv')
pp_f_gfs_pp_mean_b_none_d1_p3d = os.path.join(project_path, 'databases/forecasted/pp_f_gfs_pp_mean_b_none_d1_p3d.csv')
pp_f_gfs_pp_mean_b_none_d1_p4d = os.path.join(project_path, 'databases/forecasted/pp_f_gfs_pp_mean_b_none_d1_p4d.csv')
pp_f_gfs_pp_max_b_none_d1_p0d = os.path.join(project_path, 'databases/forecasted/pp_f_gfs_pp_max_b_none_d1_p0d.csv')
pp_f_gfs_pp_max_b_none_d1_p1d = os.path.join(project_path, 'databases/forecasted/pp_f_gfs_pp_max_b_none_d1_p1d.csv')
pp_f_gfs_pp_max_b_none_d1_p2d = os.path.join(project_path, 'databases/forecasted/pp_f_gfs_pp_max_b_none_d1_p2d.csv')
pp_f_gfs_pp_max_b_none_d1_p3d = os.path.join(project_path, 'databases/forecasted/pp_f_gfs_pp_max_b_none_d1_p3d.csv')
pp_f_gfs_pp_max_b_none_d1_p4d = os.path.join(project_path, 'databases/forecasted/pp_f_gfs_pp_max_b_none_d1_p4d.csv')
awc_f_gfs_rh_mean_b_none_d1_p0d = os.path.join(project_path, 'databases/forecasted/awc_f_gfs_rh_mean_b_none_d1_p0d.csv')
awc_f_gfs_rh_mean_b_none_d1_p1d = os.path.join(project_path, 'databases/forecasted/awc_f_gfs_rh_mean_b_none_d1_p1d.csv')
awc_f_gfs_rh_mean_b_none_d1_p2d = os.path.join(project_path, 'databases/forecasted/awc_f_gfs_rh_mean_b_none_d1_p2d.csv')
awc_f_gfs_rh_mean_b_none_d1_p3d = os.path.join(project_path, 'databases/forecasted/awc_f_gfs_rh_mean_b_none_d1_p3d.csv')
awc_f_gfs_rh_mean_b_none_d1_p4d = os.path.join(project_path, 'databases/forecasted/awc_f_gfs_rh_mean_b_none_d1_p4d.csv')
tmp_f_gfs_tmp_mean_b_none_d1_p0d = os.path.join(project_path,
                                                'databases/forecasted/tmp_f_gfs_tmp_mean_b_none_d1_p0d.csv')
tmp_f_gfs_tmp_mean_b_none_d1_p1d = os.path.join(project_path,
                                                'databases/forecasted/tmp_f_gfs_tmp_mean_b_none_d1_p1d.csv')
tmp_f_gfs_tmp_mean_b_none_d1_p2d = os.path.join(project_path,
                                                'databases/forecasted/tmp_f_gfs_tmp_mean_b_none_d1_p2d.csv')
tmp_f_gfs_tmp_mean_b_none_d1_p3d = os.path.join(project_path,
                                                'databases/forecasted/tmp_f_gfs_tmp_mean_b_none_d1_p3d.csv')
tmp_f_gfs_tmp_mean_b_none_d1_p4d = os.path.join(project_path,
                                                'databases/forecasted/tmp_f_gfs_tmp_mean_b_none_d1_p4d.csv')
atm_f_gfs_gh_mean_b_none_d1_p0d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_gh_mean_b_none_d1_p0d.csv')
atm_f_gfs_gh_mean_b_none_d1_p1d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_gh_mean_b_none_d1_p1d.csv')
atm_f_gfs_gh_mean_b_none_d1_p2d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_gh_mean_b_none_d1_p2d.csv')
atm_f_gfs_gh_mean_b_none_d1_p3d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_gh_mean_b_none_d1_p3d.csv')
atm_f_gfs_gh_mean_b_none_d1_p4d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_gh_mean_b_none_d1_p4d.csv')
atm_f_gfs_uw_mean_b_none_d1_p0d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_uw_mean_b_none_d1_p0d.csv')
atm_f_gfs_uw_mean_b_none_d1_p1d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_uw_mean_b_none_d1_p1d.csv')
atm_f_gfs_uw_mean_b_none_d1_p2d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_uw_mean_b_none_d1_p2d.csv')
atm_f_gfs_uw_mean_b_none_d1_p3d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_uw_mean_b_none_d1_p3d.csv')
atm_f_gfs_uw_mean_b_none_d1_p4d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_uw_mean_b_none_d1_p4d.csv')
atm_f_gfs_vw_mean_b_none_d1_p0d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_vw_mean_b_none_d1_p0d.csv')
atm_f_gfs_vw_mean_b_none_d1_p1d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_vw_mean_b_none_d1_p1d.csv')
atm_f_gfs_vw_mean_b_none_d1_p2d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_vw_mean_b_none_d1_p2d.csv')
atm_f_gfs_vw_mean_b_none_d1_p3d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_vw_mean_b_none_d1_p3d.csv')
atm_f_gfs_vw_mean_b_none_d1_p4d = os.path.join(project_path, 'databases/forecasted/atm_f_gfs_vw_mean_b_none_d1_p4d.csv')
tmp_f_gfs_tmp_min_b_none_d1_p0d = os.path.join(project_path, 'databases/forecasted/tmp_f_gfs_tmp_min_b_none_d1_p0d.csv')
tmp_f_gfs_tmp_min_b_none_d1_p1d = os.path.join(project_path, 'databases/forecasted/tmp_f_gfs_tmp_min_b_none_d1_p1d.csv')
tmp_f_gfs_tmp_min_b_none_d1_p2d = os.path.join(project_path, 'databases/forecasted/tmp_f_gfs_tmp_min_b_none_d1_p2d.csv')
tmp_f_gfs_tmp_min_b_none_d1_p3d = os.path.join(project_path, 'databases/forecasted/tmp_f_gfs_tmp_min_b_none_d1_p3d.csv')
tmp_f_gfs_tmp_min_b_none_d1_p4d = os.path.join(project_path, 'databases/forecasted/tmp_f_gfs_tmp_min_b_none_d1_p4d.csv')
tmp_f_gfs_tmp_max_b_none_d1_p0d = os.path.join(project_path, 'databases/forecasted/tmp_f_gfs_tmp_max_b_none_d1_p0d.csv')
tmp_f_gfs_tmp_max_b_none_d1_p1d = os.path.join(project_path, 'databases/forecasted/tmp_f_gfs_tmp_max_b_none_d1_p1d.csv')
tmp_f_gfs_tmp_max_b_none_d1_p2d = os.path.join(project_path, 'databases/forecasted/tmp_f_gfs_tmp_max_b_none_d1_p2d.csv')
tmp_f_gfs_tmp_max_b_none_d1_p3d = os.path.join(project_path, 'databases/forecasted/tmp_f_gfs_tmp_max_b_none_d1_p3d.csv')
tmp_f_gfs_tmp_max_b_none_d1_p4d = os.path.join(project_path, 'databases/forecasted/tmp_f_gfs_tmp_max_b_none_d1_p4d.csv')
pp_f_gfs_plen_mean_b_none_d1_p0d = os.path.join(project_path,
                                                'databases/forecasted/pp_f_gfs_plen_mean_b_none_d1_p0d.csv')
pp_f_gfs_plen_mean_b_none_d1_p1d = os.path.join(project_path,
                                                'databases/forecasted/pp_f_gfs_plen_mean_b_none_d1_p1d.csv')
pp_f_gfs_plen_mean_b_none_d1_p2d = os.path.join(project_path,
                                                'databases/forecasted/pp_f_gfs_plen_mean_b_none_d1_p2d.csv')
pp_f_gfs_plen_mean_b_none_d1_p3d = os.path.join(project_path,
                                                'databases/forecasted/pp_f_gfs_plen_mean_b_none_d1_p3d.csv')
pp_f_gfs_plen_mean_b_none_d1_p4d = os.path.join(project_path,
                                                'databases/forecasted/pp_f_gfs_plen_mean_b_none_d1_p4d.csv')

#
# new names
#

pp_o_era5_pp_mean = os.path.join(project_path, 'databases/observed/pp_o_era5_pp_mean_b_none_d1_p0d.csv')
pp_o_era5_maxpp_mean = os.path.join(project_path, 'databases/observed/pp_o_era5_maxpp_mean_b_none_d1_p0d.csv')
snw_o_era5_snr_mean = os.path.join(project_path, 'databases/observed/snw_o_era5_snr_mean_b_none_d1_p0d.csv')
snw_o_era5_snd_mean = os.path.join(project_path, 'databases/observed/snw_o_era5_snd_mean_b_none_d1_p0d.csv')
snw_o_era5_sca_mean = os.path.join(project_path, 'databases/observed/snw_o_era5_sca_mean_b_none_d1_p0d.csv')
snw_o_era5_sna_mean = os.path.join(project_path, 'databases/observed/snw_o_era5_sna_mean_b_none_d1_p0d.csv')
atm_o_era5_pres_mean = os.path.join(project_path, 'databases/observed/atm_o_era5_pres_mean_b_none_d1_p0d.csv')
atm_o_era5_z_mean = os.path.join(project_path, 'databases/observed/atm_o_era5_z_mean_b_none_d1_p0d.csv')
atm_o_era5_uw_mean = os.path.join(project_path, 'databases/observed/atm_o_era5_uw_mean_b_none_d1_p0d.csv')
atm_o_era5_vw_mean = os.path.join(project_path, 'databases/observed/atm_o_era5_vw_mean_b_none_d1_p0d.csv')
awc_o_era5_rh_mean = os.path.join(project_path, 'databases/observed/awc_o_era5_rh_mean_b_none_d1_p0d.csv')
tmp_o_era5_tmp_mean = os.path.join(project_path, 'databases/observed/tmp_o_era5_tmp_mean_b_none_d1_p0d.csv')
tmp_o_era5_tmin_mean = os.path.join(project_path, 'databases/observed/tmp_o_era5_tmin_mean_b_none_d1_p0d.csv')
tmp_o_era5_tmax_mean = os.path.join(project_path, 'databases/observed/tmp_o_era5_tmax_mean_b_none_d1_p0d.csv')
tmp_o_era5_dew_mean = os.path.join(project_path, 'databases/observed/tmp_o_era5_dew_mean_b_none_d1_p0d.csv')
et_o_era5_eta_mean = os.path.join(project_path, 'databases/observed/et_o_era5_eta_mean_b_none_d1_p0d.csv')
et_o_era5_eto_mean = os.path.join(project_path, 'databases/observed/et_o_era5_eto_mean_b_none_d1_p0d.csv')
swc_o_era5_sm_mean = os.path.join(project_path, 'databases/observed/swc_o_era5_sm_mean_b_none_d1_p0d.csv')
veg_o_modis_fpar_mean = os.path.join(project_path, 'databases/observed/veg_o_modis_fpar_mean_b_none_d1_p0d.csv')
veg_o_modis_lai_mean = os.path.join(project_path, 'databases/observed/veg_o_modis_lai_mean_b_none_d1_p0d.csv')
lulc_o_modis_brn_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_brn_frac_b_none_d1_p0d.csv')
lulc_o_modis_crp_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_crp_frac_b_none_d1_p0d.csv')
lulc_o_modis_csh_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_csh_frac_b_none_d1_p0d.csv')
lulc_o_modis_cvm_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_cvm_frac_b_none_d1_p0d.csv')
lulc_o_modis_dbf_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_dbf_frac_b_none_d1_p0d.csv')
lulc_o_modis_dnf_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_dnf_frac_b_none_d1_p0d.csv')
lulc_o_modis_ebf_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_ebf_frac_b_none_d1_p0d.csv')
lulc_o_modis_enf_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_enf_frac_b_none_d1_p0d.csv')
lulc_o_modis_grs_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_grs_frac_b_none_d1_p0d.csv')
lulc_o_modis_mxf_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_mxf_frac_b_none_d1_p0d.csv')
lulc_o_modis_osh_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_osh_frac_b_none_d1_p0d.csv')
lulc_o_modis_pwt_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_pwt_frac_b_none_d1_p0d.csv')
lulc_o_modis_snw_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_snw_frac_b_none_d1_p0d.csv')
lulc_o_modis_svn_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_svn_frac_b_none_d1_p0d.csv')
lulc_o_modis_urb_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_urb_frac_b_none_d1_p0d.csv')
lulc_o_modis_wat_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_wat_frac_b_none_d1_p0d.csv')
lulc_o_modis_wsv_frac_b_none_d1_p0d = os.path.join(project_path,
                                                   'databases/observed/lulc_o_modis_wsv_frac_b_none_d1_p0d.csv')
lulc_o_modis_brn_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_brn_sum_b_none_d1_p0d.csv')
lulc_o_modis_crp_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_crp_sum_b_none_d1_p0d.csv')
lulc_o_modis_csh_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_csh_sum_b_none_d1_p0d.csv')
lulc_o_modis_cvm_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_cvm_sum_b_none_d1_p0d.csv')
lulc_o_modis_dbf_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_dbf_sum_b_none_d1_p0d.csv')
lulc_o_modis_dnf_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_dnf_sum_b_none_d1_p0d.csv')
lulc_o_modis_ebf_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_ebf_sum_b_none_d1_p0d.csv')
lulc_o_modis_enf_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_enf_sum_b_none_d1_p0d.csv')
lulc_o_modis_grs_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_grs_sum_b_none_d1_p0d.csv')
lulc_o_modis_mxf_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_mxf_sum_b_none_d1_p0d.csv')
lulc_o_modis_osh_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_osh_sum_b_none_d1_p0d.csv')
lulc_o_modis_pwt_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_pwt_sum_b_none_d1_p0d.csv')
lulc_o_modis_snw_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_snw_sum_b_none_d1_p0d.csv')
lulc_o_modis_svn_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_svn_sum_b_none_d1_p0d.csv')
lulc_o_modis_urb_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_urb_sum_b_none_d1_p0d.csv')
lulc_o_modis_wat_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_wat_sum_b_none_d1_p0d.csv')
lulc_o_modis_wsv_sum_b_none_d1_p0d = os.path.join(project_path,
                                                  'databases/observed/lulc_o_modis_wsv_sum_b_none_d1_p0d.csv')

lulc_o_modis_brn_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_brn_frac_pc.csv')
lulc_o_modis_crp_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_crp_frac_pc.csv')
lulc_o_modis_csh_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_csh_frac_pc.csv')
lulc_o_modis_cvm_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_cvm_frac_pc.csv')
lulc_o_modis_dbf_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_dbf_frac_pc.csv')
lulc_o_modis_dnf_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_dnf_frac_pc.csv')
lulc_o_modis_ebf_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_ebf_frac_pc.csv')
lulc_o_modis_enf_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_enf_frac_pc.csv')
lulc_o_modis_grs_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_grs_frac_pc.csv')
lulc_o_modis_mxf_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_mxf_frac_pc.csv')
lulc_o_modis_osh_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_osh_frac_pc.csv')
lulc_o_modis_pwt_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_pwt_frac_pc.csv')
lulc_o_modis_snw_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_snw_frac_pc.csv')
lulc_o_modis_svn_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_svn_frac_pc.csv')
lulc_o_modis_urb_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_urb_frac_pc.csv')
lulc_o_modis_wat_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_wat_frac_pc.csv')
lulc_o_modis_wsv_frac_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_wsv_frac_pc.csv')

lulc_o_modis_brn_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_brn_sum_pc.csv')
lulc_o_modis_crp_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_crp_sum_pc.csv')
lulc_o_modis_csh_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_csh_sum_pc.csv')
lulc_o_modis_cvm_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_cvm_sum_pc.csv')
lulc_o_modis_dbf_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_dbf_sum_pc.csv')
lulc_o_modis_dnf_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_dnf_sum_pc.csv')
lulc_o_modis_ebf_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_ebf_sum_pc.csv')
lulc_o_modis_enf_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_enf_sum_pc.csv')
lulc_o_modis_grs_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_grs_sum_pc.csv')
lulc_o_modis_mxf_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_mxf_sum_pc.csv')
lulc_o_modis_osh_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_osh_sum_pc.csv')
lulc_o_modis_pwt_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_pwt_sum_pc.csv')
lulc_o_modis_snw_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_snw_sum_pc.csv')
lulc_o_modis_svn_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_svn_sum_pc.csv')
lulc_o_modis_urb_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_urb_sum_pc.csv')
lulc_o_modis_wat_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_wat_sum_pc.csv')
lulc_o_modis_wsv_sum_pc = os.path.join(project_path, 'pcdatabases/observed/lulc_o_modis_wsv_sum_pc.csv')

pp_o_era5_pp_pc = os.path.join(project_path, 'pcdatabases/observed/pp_o_era5_pp_pc.csv')
pp_o_era5_maxpp_pc = os.path.join(project_path, 'pcdatabases/observed/pp_o_era5_maxpp_pc.csv')
snw_o_era5_snr_pc = os.path.join(project_path, 'pcdatabases/observed/snw_o_era5_snr_pc.csv')
snw_o_era5_snd_pc = os.path.join(project_path, 'pcdatabases/observed/snw_o_era5_snd_pc.csv')
snw_o_era5_sca_pc = os.path.join(project_path, 'pcdatabases/observed/snw_o_era5_sca_pc.csv')
snw_o_era5_sna_pc = os.path.join(project_path, 'pcdatabases/observed/snw_o_era5_sna_pc.csv')
atm_o_era5_pres_pc = os.path.join(project_path, 'pcdatabases/observed/atm_o_era5_pres_pc.csv')
atm_o_era5_z_pc = os.path.join(project_path, 'pcdatabases/observed/atm_o_era5_z_pc.csv')
atm_o_era5_uw_pc = os.path.join(project_path, 'pcdatabases/observed/atm_o_era5_uw_pc.csv')
atm_o_era5_vw_pc = os.path.join(project_path, 'pcdatabases/observed/atm_o_era5_vw_pc.csv')
awc_o_era5_rh_pc = os.path.join(project_path, 'pcdatabases/observed/awc_o_era5_rh_pc.csv')
tmp_o_era5_tmp_pc = os.path.join(project_path, 'pcdatabases/observed/tmp_o_era5_tmp_pc.csv')
tmp_o_era5_tmin_pc = os.path.join(project_path, 'pcdatabases/observed/tmp_o_era5_tmin_pc.csv')
tmp_o_era5_tmax_pc = os.path.join(project_path, 'pcdatabases/observed/tmp_o_era5_tmax_pc.csv')
tmp_o_era5_dew_pc = os.path.join(project_path, 'pcdatabases/observed/tmp_o_era5_dew_pc.csv')
et_o_era5_eta_pc = os.path.join(project_path, 'pcdatabases/observed/et_o_era5_eta_pc.csv')
et_o_era5_eto_pc = os.path.join(project_path, 'pcdatabases/observed/et_o_era5_eto_pc.csv')
swc_o_era5_sm_pc = os.path.join(project_path, 'pcdatabases/observed/swc_o_era5_sm_pc.csv')
veg_o_modis_fpar_pc = os.path.join(project_path, 'pcdatabases/observed/veg_o_modis_fpar_pc.csv')
veg_o_modis_lai_pc = os.path.join(project_path, 'pcdatabases/observed/veg_o_modis_lai_pc.csv')

log_tmp_o_era5_tmp_mean = os.path.join(project_path, 'logs/log_tmp_o_era5_tmp_mean.txt')
log_tmp_o_era5_tmin_mean = os.path.join(project_path, 'logs/log_tmp_o_era5_tmin_mean.txt')
log_tmp_o_era5_tmax_mean = os.path.join(project_path, 'logs/log_tmp_o_era5_tmax_mean.txt')
log_pp_o_era5_maxpp_mean = os.path.join(project_path, 'logs/log_tmp_o_era5_tmax_mean.txt')

# ----
# pixel count databases
# ----
# static

# observed
veg_o_modis_ndvi_mean_pc = os.path.join(project_path, 'pcdatabases/observed/veg_o_modis_ndvi_mean_pc.csv')
veg_o_modis_evi_mean_pc = os.path.join(project_path, 'pcdatabases/observed/veg_o_modis_evi_mean_pc.csv')
veg_o_int_nbr_mean_pc = os.path.join(project_path, 'pcdatabases/observed/veg_o_int_nbr_mean_pc.csv')
snw_o_modis_sca_cum_n_pc = os.path.join(project_path, 'pcdatabases/observed/snw_o_modis_sca_cum_n_pc.csv')
snw_o_modis_sca_cum_s_pc = os.path.join(project_path, 'pcdatabases/observed/snw_o_modis_sca_cum_s_pc.csv')
et_o_modis_eto_cum_b_pc = os.path.join(project_path, 'pcdatabases/observed/et_o_modis_eto_cum_b_pc.csv')
et_o_modis_eta_cum_b_pc = os.path.join(project_path, 'pcdatabases/observed/et_o_modis_eta_cum_b_pc.csv')
veg_o_modis_lai_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/veg_o_modis_lai_mean_b_pc.csv')
veg_o_modis_fpar_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/veg_o_modis_fpar_mean_b_pc.csv')
pp_o_imerg_pp_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/pp_o_imerg_pp_mean_b_pc.csv')
## new names
veg_o_modis_agr_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/veg_o_modis_agr_mean_b_pc.csv')
# GLDAS products:
snw_o_gldas_swe_cum_b_pc = os.path.join(project_path, 'pcdatabases/observed/snw_o_gldas_swe_cum_b_pc.csv')
tmp_f_gldas_tmp_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/tmp_f_gldas_tmp_mean_b_pc.csv')
et_o_gldas_eta_cum_b_pc = os.path.join(project_path, 'pcdatabases/observed/et_o_gldas_eta_cum_b_pc.csv')
sm_o_gldas_sm_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/sm_o_gldas_sm_mean_b_pc.csv')
pp_o_pers_pp_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/pp_o_pers_pp_mean_b_pc.csv')
pp_o_pcdr_pp_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/pp_o_pcdr_pp_mean_b_pc.csv')
pp_o_pdir_pp_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/pp_o_pdir_pp_mean_b_pc.csv')
# ERA5 products:
tmp_o_era5_tmp_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/tmp_o_era5_tmp_mean_b_pc.csv')
tmp_o_era5_tmp_min_b_pc = os.path.join(project_path, 'pcdatabases/observed/tmp_o_era5_tmp_min_b_pc.csv')
tmp_o_era5_tmp_max_b_pc = os.path.join(project_path, 'pcdatabases/observed/tmp_o_era5_tmp_max_b_pc.csv')
pp_o_era5_pp_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/pp_o_era5_pp_mean_b_pc.csv')
et_o_era5_eto_cum_b_pc = os.path.join(project_path, 'pcdatabases/observed/et_o_era5_eto_cum_b_pc.csv')
et_o_era5_et_cum_b_pc = os.path.join(project_path, 'pcdatabases/observed/et_o_era5_et_cum_b_pc.csv')
snow_o_era5_sca_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/snow_o_era5_sca_b_mean_pc.csv')
snow_o_era5_sna_mean_b_pc = os.path.join(project_path,
                                         'pcdatabases/observed/snow_o_era5_sna_b_mean_pc.csv')  # snow albedo
snow_o_era5_snr_mean_b_pc = os.path.join(project_path,
                                         'pcdatabases/observed/snow_o_era5_snr_b_mean_pc.csv')  # snow density
snow_o_era5_snd_mean_b_pc = os.path.join(project_path,
                                         'pcdatabases/observed/snow_o_era5_snd_b_mean_pc.csv')  # snow depth
sm_o_era5_sm_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/sm_o_era5_sm_mean_b_pc.csv')  # soil moisture
pp_o_era5_plen_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/pp_o_era5_plen_mean_b_pc.csv')  # pp length
# new names
tmp_o_era5_dew_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/tmp_o_era5_dew_mean_b_pc.csv')
wind_o_era5_u10_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/wind_o_era5_u10_mean_b_pc.csv')
wind_o_era5_v10_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/wind_o_era5_v10_mean_b_pc.csv')
atm_o_era5_pres_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/atm_o_era5_pres_mean_b_pc.csv')
atm_o_era5_z_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/atm_o_era5_z_mean_b_pc.csv')
awc_o_era5_rh_mean_b_pc = os.path.join(project_path, 'pcdatabases/observed/awc_o_era5_rh_mean_b_pc.csv')

# forecasted
pp_f_gfs_pp_max_pc_p0d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_pp_max_pc_p0d.csv')
pp_f_gfs_pp_max_pc_p1d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_pp_max_pc_p1d.csv')
pp_f_gfs_pp_max_pc_p2d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_pp_max_pc_p2d.csv')
pp_f_gfs_pp_max_pc_p3d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_pp_max_pc_p3d.csv')
pp_f_gfs_pp_max_pc_p4d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_pp_max_pc_p4d.csv')
pp_f_gfs_pp_mean_pc_p0d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_pp_mean_pc_p0d.csv')
pp_f_gfs_pp_mean_pc_p1d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_pp_mean_pc_p1d.csv')
pp_f_gfs_pp_mean_pc_p2d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_pp_mean_pc_p2d.csv')
pp_f_gfs_pp_mean_pc_p3d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_pp_mean_pc_p3d.csv')
pp_f_gfs_pp_mean_pc_p4d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_pp_mean_pc_p4d.csv')
awc_f_gfs_rh_mean_pc_p0d = os.path.join(project_path, 'pcdatabases/forecasted/awc_f_gfs_rh_mean_pc_p0d.csv')
awc_f_gfs_rh_mean_pc_p1d = os.path.join(project_path, 'pcdatabases/forecasted/awc_f_gfs_rh_mean_pc_p1d.csv')
awc_f_gfs_rh_mean_pc_p2d = os.path.join(project_path, 'pcdatabases/forecasted/awc_f_gfs_rh_mean_pc_p2d.csv')
awc_f_gfs_rh_mean_pc_p3d = os.path.join(project_path, 'pcdatabases/forecasted/awc_f_gfs_rh_mean_pc_p3d.csv')
awc_f_gfs_rh_mean_pc_p4d = os.path.join(project_path, 'pcdatabases/forecasted/awc_f_gfs_rh_mean_pc_p4d.csv')
atm_f_gfs_gh_mean_pc_p0d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_gh_mean_pc_p0d.csv')
atm_f_gfs_gh_mean_pc_p1d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_gh_mean_pc_p1d.csv')
atm_f_gfs_gh_mean_pc_p2d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_gh_mean_pc_p2d.csv')
atm_f_gfs_gh_mean_pc_p3d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_gh_mean_pc_p3d.csv')
atm_f_gfs_gh_mean_pc_p4d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_gh_mean_pc_p4d.csv')
atm_f_gfs_uw_mean_pc_p0d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_uw_mean_pc_p0d.csv')
atm_f_gfs_uw_mean_pc_p1d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_uw_mean_pc_p1d.csv')
atm_f_gfs_uw_mean_pc_p2d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_uw_mean_pc_p2d.csv')
atm_f_gfs_uw_mean_pc_p3d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_uw_mean_pc_p3d.csv')
atm_f_gfs_uw_mean_pc_p4d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_uw_mean_pc_p4d.csv')
atm_f_gfs_vw_mean_pc_p0d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_vw_mean_pc_p0d.csv')
atm_f_gfs_vw_mean_pc_p1d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_vw_mean_pc_p1d.csv')
atm_f_gfs_vw_mean_pc_p2d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_vw_mean_pc_p2d.csv')
atm_f_gfs_vw_mean_pc_p3d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_vw_mean_pc_p3d.csv')
atm_f_gfs_vw_mean_pc_p4d = os.path.join(project_path, 'pcdatabases/forecasted/atm_f_gfs_vw_mean_pc_p4d.csv')
tmp_f_gfs_tmp_mean_pc_p0d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_mean_pc_p0d.csv')
tmp_f_gfs_tmp_mean_pc_p1d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_mean_pc_p1d.csv')
tmp_f_gfs_tmp_mean_pc_p2d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_mean_pc_p2d.csv')
tmp_f_gfs_tmp_mean_pc_p3d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_mean_pc_p3d.csv')
tmp_f_gfs_tmp_mean_pc_p4d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_mean_pc_p4d.csv')
tmp_f_gfs_tmp_min_pc_p0d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_min_pc_p0d.csv')
tmp_f_gfs_tmp_min_pc_p1d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_min_pc_p1d.csv')
tmp_f_gfs_tmp_min_pc_p2d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_min_pc_p2d.csv')
tmp_f_gfs_tmp_min_pc_p3d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_min_pc_p3d.csv')
tmp_f_gfs_tmp_min_pc_p4d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_min_pc_p4d.csv')
tmp_f_gfs_tmp_max_pc_p0d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_max_pc_p0d.csv')
tmp_f_gfs_tmp_max_pc_p1d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_max_pc_p1d.csv')
tmp_f_gfs_tmp_max_pc_p2d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_max_pc_p2d.csv')
tmp_f_gfs_tmp_max_pc_p3d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_max_pc_p3d.csv')
tmp_f_gfs_tmp_max_pc_p4d = os.path.join(project_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_max_pc_p4d.csv')
pp_f_gfs_plen_mean_pc_p0d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_plen_mean_pc_p0d.csv')
pp_f_gfs_plen_mean_pc_p1d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_plen_mean_pc_p1d.csv')
pp_f_gfs_plen_mean_pc_p2d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_plen_mean_pc_p2d.csv')
pp_f_gfs_plen_mean_pc_p3d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_plen_mean_pc_p3d.csv')
pp_f_gfs_plen_mean_pc_p4d = os.path.join(project_path, 'pcdatabases/forecasted/pp_f_gfs_plen_mean_pc_p4d.csv')

# ----
# log files
# ----
# observed
log_snw_o_modis_sca_cum = os.path.join(project_path, 'logs/log_snw_o_modis_sca_cum.txt')
log_veg_o_modis_ndvi_mean = os.path.join(project_path, 'logs/log_veg_o_modis_ndvi_mean.txt')
log_veg_o_modis_evi_mean = os.path.join(project_path, 'logs/log_veg_o_modis_evi_mean.txt')
log_veg_o_int_nbr_mean = os.path.join(project_path, 'logs/log_veg_o_int_nbr_mean.txt')
log_veg_o_agr_ndvi_mean = os.path.join(project_path, 'logs/log_veg_o_modis_agr_mean.txt')
# log_sun_o_modis_al_mean_b_d16_p0d = os.path.join(nas_path, 'logs/log_sun_o_modis_al_mean_b_d16_p0d.txt')
# log_sun_o_modis_al_median_b_d16_p0d = os.path.join(nas_path, 'logs/log_sun_o_modis_al_median_b_d16_p0d.txt')
# log_sun_o_modis_al_p90_b_d16_p0d = os.path.join(nas_path, 'logs/log_sun_o_modis_al_p90_b_d16_p0d.txt')
# log_sun_o_modis_al_p10_b_d16_p0d = os.path.join(nas_path, 'logs/log_sun_o_modis_al_p10_b_d16_p0d.txt')
# log_sun_o_modis_al_p25_b_d16_p0d = os.path.join(nas_path, 'logs/log_sun_o_modis_al_p25_b_d16_p0d.txt')
# log_sun_o_modis_al_p75_b_d16_p0d = os.path.join(nas_path, 'logs/log_sun_o_modis_al_p75_b_d16_p0d.txt')
log_et_o_modis_eto_cum_b_d8_p0d = os.path.join(project_path, 'logs/log_et_o_modis_eto_cum_b_d8_p0d.txt')
log_et_o_modis_eta_cum_b_d8_p0d = os.path.join(project_path, 'logs/log_et_o_modis_eta_cum_b_d8_p0d.txt')
log_veg_o_modis_lai_mean = os.path.join(project_path, 'logs/log_veg_o_modis_lai_mean.txt')
log_veg_o_modis_fpar_mean = os.path.join(project_path, 'logs/log_veg_o_modis_fpar_mean.txt')
log_pp_o_imerg_pp_mean = os.path.join(project_path, 'logs/log_pp_o_imerg_pp_mean.txt')
# GLDAS products:
log_snw_o_gldas_swe_cum = os.path.join(project_path, 'logs/log_snw_o_gldas_swe_cum.txt')
log_tmp_f_gldas_tmp_mean = os.path.join(project_path, 'logs/log_tmp_f_gldas_tmp_mean.txt')
log_et_o_gldas_eta_cum = os.path.join(project_path, 'logs/log_et_o_gldas_eta_cum.txt')
log_sm_o_gldas_sm_mean = os.path.join(project_path, 'logs/log_sm_o_gldas_sm_mean.txt')
log_pp_o_pers_pp_mean = os.path.join(project_path, 'logs/log_pp_o_pers_pp_mean.txt')
log_pp_o_pcdr_pp_mean = os.path.join(project_path, 'logs/log_pp_o_pcdr_pp_mean.txt')
log_pp_o_pdir_pp_mean = os.path.join(project_path, 'logs/log_pp_o_pdir_pp_mean.txt')
# ERA5 products:
log_tmp_o_era5_tmp_mean = os.path.join(project_path, 'logs/log_tmp_o_era5_tmp_mean.txt')
log_tmp_o_era5_tmp_min = os.path.join(project_path, 'logs/log_tmp_o_era5_tmp_mean.txt')
log_tmp_o_era5_tmp_max = os.path.join(project_path, 'logs/log_tmp_o_era5_tmp_mean.txt')
log_pp_o_era5_pp_mean = os.path.join(project_path, 'logs/log_pp_o_era5_pp_mean.txt')
log_et_o_era5_eto_cum = os.path.join(project_path, 'logs/log_et_o_era5_eto_cum.txt')
log_et_o_era5_et_cum = os.path.join(project_path, 'logs/log_et_o_era5_et_cum.txt')
log_snow_o_era5_sca = os.path.join(project_path, 'logs/log_snow_o_era5_sca.txt')
log_snow_o_era5_sna = os.path.join(project_path, 'logs/log_snow_o_era5_sna.txt')
log_snow_o_era5_snr = os.path.join(project_path, 'logs/log_snow_o_era5_snr.txt')
log_snow_o_era5_snd = os.path.join(project_path, 'logs/log_snow_o_era5_snd.txt')
log_sm_o_era5_sm_mean = os.path.join(project_path, 'logs/log_sm_o_era5_sm_mean.txt')
log_tmp_o_era5_dew_mean = os.path.join(project_path, 'logs/log_tmp_o_era5_dew_mean.txt')
log_wind_o_era5_u10_mean = os.path.join(project_path, 'logs/log_wind_o_era5_u10_mean.txt')
log_wind_o_era5_v10_mean = os.path.join(project_path, 'logs/log_wind_o_era5_v10_mean.txt')
log_atm_o_era5_pres_mean = os.path.join(project_path, 'logs/log_atm_o_era5_pres_mean.txt')
log_atm_o_era5_z_mean = os.path.join(project_path, 'logs/log_atm_o_era5_z_mean.csv')
log_awc_o_era5_rh_mean = os.path.join(project_path, 'logs/log_awc_o_era5_rh_mean.txt')
log_pp_o_era5_plen_mean = os.path.join(project_path, 'logs/log_pp_o_era5_plen_mean.txt')  # pp length

log_file_maintainer = os.path.join(project_path, 'logs/file_maintainer.txt')

# forecasted
log_pp_f_gfs_pp_max_log = os.path.join(project_path, 'logs/pp_f_gfs_pp_max_log.txt')
log_pp_f_gfs_pp_mean_log = os.path.join(project_path, 'logs/pp_f_gfs_pp_mean_log.txt')
log_awc_f_gfs_rh_mean_log = os.path.join(project_path, 'logs/awc_f_gfs_rh_mean_log.txt')
log_atm_f_gfs_gh_mean_log = os.path.join(project_path, 'logs/atm_f_gfs_gh_mean_log.txt')
log_atm_f_gfs_uw_mean_log = os.path.join(project_path, 'logs/atm_f_gfs_uw_mean_log.txt')
log_atm_f_gfs_vw_mean_log = os.path.join(project_path, 'logs/atm_f_gfs_vw_mean_log.txt')
log_tmp_f_gfs_tmp_mean_log = os.path.join(project_path, 'logs/tmp_f_gfs_tmp_mean_log.txt')
log_tmp_f_gfs_tmp_min_log = os.path.join(project_path, 'logs/tmp_f_gfs_tmp_min_log.txt')
log_tmp_f_gfs_tmp_max_log = os.path.join(project_path, 'logs/tmp_f_gfs_tmp_max_log.txt')
log_pp_f_gfs_plen_mean_log = os.path.join(project_path, 'logs/pp_f_gfs_plen_mean_log.txt')
