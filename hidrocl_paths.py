import os
# import geopandas as gpd
from sys import platform


if platform == "linux" or platform == "linux2":
    nas_path = '/mnt/nas'
    github_path = '/home/aldo/github-hidrocl/HidroCL-DBCreation/'
elif platform == "darwin":
    nas_path = '/private/nfs2'
    github_path = '/Users/aldotapia/Documents/GitHub/HidroCL-OOP/'
# elif platform == "win32":
    # Windows...



# ----
# path to folders
# ----
# observed
mcd12q1_path = os.path.join(nas_path, 'observed/MCD12Q1/')  # lulc
mcd15a2h_path = os.path.join(nas_path, 'observed/MCD15A2H/')  # lai/fpar
mcd43a3_path = os.path.join(nas_path, 'observed/MCD43A3/')  # albedo
mod10a2_path = os.path.join(nas_path, 'observed/MOD10A2/')  # snow
mod13q1_path = os.path.join(nas_path, 'observed/MOD13Q1/')  # vegetation
mod16a2_path = os.path.join(nas_path, 'observed/MOD16A2/')  # et
# imerghhl_path = os.path.join(nas_path, 'observed/GPM_3IMERGHHL/')  # pp + other
imerggis_path = os.path.join(nas_path, 'observed/IMERG_GIS')  # pp
persiann = os.path.join(nas_path, 'observed/PERSIANN/')  # pp
gldas_noah025_3h_path = os.path.join(nas_path, 'observed/GLDAS_NOAH025_3H/')  # land data
era5_land_hourly_path = os.path.join(nas_path, 'observed/ERA5_LAND_HOURLY/')  # era5 land data
satellite_soil_moisture = os.path.join(nas_path, 'observed/SATELLITE_SOIL_MOISTURE/')  # satellite soil moisture
pdirnow = os.path.join(nas_path, 'observed/PDIRNOW/')  # pdirnow

# forecasted
gfs = os.path.join(nas_path, 'forecasted')  # only forecasted variable

# path to files
hidrocl_sinusoidal = os.path.join(nas_path,
                                  'base/boundaries/HidroCL_boundaries_sinu.shp')  # polys with sinusoidal projection
hidrocl_utm = os.path.join(nas_path, 'base/boundaries/HidroCL_boundaries_utm.shp')
hidrocl_wgs84 = os.path.join(nas_path, 'base/boundaries/HidroCL_boundaries.shp')
hidrocl_north = os.path.join(nas_path, 'static/DEM/HidroCL_north.shp')
hidrocl_south = os.path.join(nas_path, 'static/DEM/HidroCL_south.shp')

# ----
# databases
# ----
# static
# not for this module

# observed
snw_o_modis_sca_cum_n_d8_p0d = os.path.join(nas_path, 'databases/observed/snw_o_modis_sca_cum_n_d8_p0d.csv')
snw_o_modis_sca_cum_s_d8_p0d = os.path.join(nas_path, 'databases/observed/snw_o_modis_sca_cum_s_d8_p0d.csv')
veg_o_modis_ndvi_mean_b_d16_p0d = os.path.join(nas_path, 'databases/observed/veg_o_modis_ndvi_mean_b_d16_p0d.csv')
veg_o_modis_evi_mean_b_d16_p0d = os.path.join(nas_path, 'databases/observed/veg_o_modis_evi_mean_b_d16_p0d.csv')
veg_o_int_nbr_mean_b_d16_p0d = os.path.join(nas_path, 'databases/observed/veg_o_int_nbr_mean_b_d16_p0d.csv')
# sun_o_modis_al_mean_b_d16_p0d = os.path.join(nas_path, 'databases/observed/sun_o_modis_al_mean_b_d16_p0d.csv')
# sun_o_modis_al_p10_b_d16_p0d = os.path.join(nas_path, 'databases/observed/sun_o_modis_al_p10_b_d16_p0d.csv')
# sun_o_modis_al_p25_b_d16_p0d = os.path.join(nas_path, 'databases/observed/sun_o_modis_al_p25_b_d16_p0d.csv')
# sun_o_modis_al_median_b_d16_p0d = os.path.join(nas_path, 'databases/observed/sun_o_modis_al_median_b_d16_p0d.csv')
# sun_o_modis_al_p75_b_d16_p0d = os.path.join(nas_path, 'databases/observed/sun_o_modis_al_p75_b_d16_p0d.csv')
# sun_o_modis_al_p90_b_d16_p0d = os.path.join(nas_path, 'databases/observed/sun_o_modis_al_p90_b_d16_p0d.csv')
et_o_modis_eto_cum_b_d8_p0d = os.path.join(nas_path, 'databases/observed/et_o_modis_eto_cum_b_d8_p0d.csv')
et_o_modis_eta_cum_b_d8_p0d = os.path.join(nas_path, 'databases/observed/et_o_modis_eta_cum_b_d8_p0d.csv')
veg_o_modis_lai_mean_b_d8_p0d = os.path.join(nas_path, 'databases/observed/veg_o_modis_lai_mean_b_d8_p0d.csv')
veg_o_modis_fpar_mean_b_d8_p0d = os.path.join(nas_path, 'databases/observed/veg_o_modis_fpar_mean_b_d8_p0d.csv')
pp_o_imerg_pp_mean_b_d_p0d = os.path.join(nas_path, 'databases/observed/pp_o_imerg_pp_mean_b_d_p0d.csv')
# GLDAS products:
snw_o_gldas_swe_cum_b_d8_p0d = os.path.join(nas_path, 'databases/observed/snw_o_gldas_swe_cum_b_d8_p0d.csv')
tmp_f_gldas_tmp_mean_b_d_p0d = os.path.join(nas_path, 'databases/observed/tmp_f_gldas_tmp_mean_b_d_p0d.csv')
et_o_gldas_eta_cum_b_d0_p0d = os.path.join(nas_path, 'databases/observed/et_o_gldas_eta_cum_b_d0_p0d.csv')
sm_o_gldas_sm_mean_b_d_p0d = os.path.join(nas_path, 'databases/observed/sm_o_gldas_sm_mean_b_d_p0d.csv')
pp_o_pers_pp_mean_b_d_p0d = os.path.join(nas_path, 'databases/observed/pp_o_pers_pp_mean_b_d_p0d.csv')
pp_o_pcdr_pp_mean_b_d_p0d = os.path.join(nas_path, 'databases/observed/pp_o_pcdr_pp_mean_b_d_p0d.csv')
# ERA5 products:
tmp_o_era5_tmp_mean_b_d14_p0d = os.path.join(nas_path, 'databases/observed/tmp_o_era5_tmp_mean_b_d14_p0d.csv')
pp_o_era5_pp_mean_b_d_p0d = os.path.join(nas_path, 'databases/observed/pp_o_era5_pp_mean_b_d_p0d.csv')
et_o_era5_eto_cum_b_d_p0d = os.path.join(nas_path, 'databases/observed/et_o_era5_eto_cum_b_d_p0d.csv')
et_o_era5_et_cum_b_d_p0d = os.path.join(nas_path, 'databases/observed/et_o_era5_et_cum_b_d_p0d.csv')
snow_o_era5_sca_mean_b_d_p0d = os.path.join(nas_path, 'databases/observed/snow_o_era5_sca_mean_b_d_p0d.csv')
snow_o_era5_sna_mean_b_d_p0d = os.path.join(nas_path, 'databases/observed/snow_o_era5_sna_mean_b_d_p0d.csv') # snow albedo
snow_o_era5_snr_mean_b_d_p0d = os.path.join(nas_path, 'databases/observed/snow_o_era5_snr_mean_b_d_p0d.csv') # snow density
snow_o_era5_snd_mean_b_d_p0d = os.path.join(nas_path, 'databases/observed/snow_o_era5_snd_mean_b_d_p0d.csv') # snow depth
sm_o_era5_sm_mean_b_d_p0d = os.path.join(nas_path, 'databases/observed/sm_o_era5_sm_mean_b_d_p0d.csv') # soil moisture
pp_o_pdir_pp_mean_b_none_d1_p0d = os.path.join(nas_path, 'databases/observed/pp_o_pdir_pp_mean_b_none_d1_p0d.csv') # new persiann

# forecasted
pp_f_gfs_pp_mean_b_none_d1_p0d = os.path.join(nas_path, 'databases/forecasted/pp_f_gfs_pp_mean_b_none_d1_p0d.csv')
pp_f_gfs_pp_mean_b_none_d1_p1d = os.path.join(nas_path, 'databases/forecasted/pp_f_gfs_pp_mean_b_none_d1_p1d.csv')
pp_f_gfs_pp_mean_b_none_d1_p2d = os.path.join(nas_path, 'databases/forecasted/pp_f_gfs_pp_mean_b_none_d1_p2d.csv')
pp_f_gfs_pp_mean_b_none_d1_p3d = os.path.join(nas_path, 'databases/forecasted/pp_f_gfs_pp_mean_b_none_d1_p3d.csv')
pp_f_gfs_pp_mean_b_none_d1_p4d = os.path.join(nas_path, 'databases/forecasted/pp_f_gfs_pp_mean_b_none_d1_p4d.csv')
pp_f_gfs_pp_max_b_none_d1_p0d = os.path.join(nas_path, 'databases/forecasted/pp_f_gfs_pp_max_b_none_d1_p0d.csv')
pp_f_gfs_pp_max_b_none_d1_p1d = os.path.join(nas_path, 'databases/forecasted/pp_f_gfs_pp_max_b_none_d1_p1d.csv')
pp_f_gfs_pp_max_b_none_d1_p2d = os.path.join(nas_path, 'databases/forecasted/pp_f_gfs_pp_max_b_none_d1_p2d.csv')
pp_f_gfs_pp_max_b_none_d1_p3d = os.path.join(nas_path, 'databases/forecasted/pp_f_gfs_pp_max_b_none_d1_p3d.csv')
pp_f_gfs_pp_max_b_none_d1_p4d = os.path.join(nas_path, 'databases/forecasted/pp_f_gfs_pp_max_b_none_d1_p4d.csv')
awc_f_gfs_rh_mean_b_none_d1_p0d = os.path.join(nas_path, 'databases/forecasted/awc_f_gfs_rh_mean_b_none_d1_p0d.csv')
awc_f_gfs_rh_mean_b_none_d1_p1d = os.path.join(nas_path, 'databases/forecasted/awc_f_gfs_rh_mean_b_none_d1_p1d.csv')
awc_f_gfs_rh_mean_b_none_d1_p2d = os.path.join(nas_path, 'databases/forecasted/awc_f_gfs_rh_mean_b_none_d1_p2d.csv')
awc_f_gfs_rh_mean_b_none_d1_p3d = os.path.join(nas_path, 'databases/forecasted/awc_f_gfs_rh_mean_b_none_d1_p3d.csv')
awc_f_gfs_rh_mean_b_none_d1_p4d = os.path.join(nas_path, 'databases/forecasted/awc_f_gfs_rh_mean_b_none_d1_p4d.csv')
tmp_f_gfs_tmp_mean_b_none_d1_p0d = os.path.join(nas_path, 'databases/forecasted/tmp_f_gfs_tmp_mean_b_none_d1_p0d.csv')
tmp_f_gfs_tmp_mean_b_none_d1_p1d = os.path.join(nas_path, 'databases/forecasted/tmp_f_gfs_tmp_mean_b_none_d1_p1d.csv')
tmp_f_gfs_tmp_mean_b_none_d1_p2d = os.path.join(nas_path, 'databases/forecasted/tmp_f_gfs_tmp_mean_b_none_d1_p2d.csv')
tmp_f_gfs_tmp_mean_b_none_d1_p3d = os.path.join(nas_path, 'databases/forecasted/tmp_f_gfs_tmp_mean_b_none_d1_p3d.csv')
tmp_f_gfs_tmp_mean_b_none_d1_p4d = os.path.join(nas_path, 'databases/forecasted/tmp_f_gfs_tmp_mean_b_none_d1_p4d.csv')
atm_f_gfs_gh_mean_b_none_d1_p0d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_gh_mean_b_none_d1_p0d.csv')
atm_f_gfs_gh_mean_b_none_d1_p1d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_gh_mean_b_none_d1_p1d.csv')
atm_f_gfs_gh_mean_b_none_d1_p2d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_gh_mean_b_none_d1_p2d.csv')
atm_f_gfs_gh_mean_b_none_d1_p3d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_gh_mean_b_none_d1_p3d.csv')
atm_f_gfs_gh_mean_b_none_d1_p4d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_gh_mean_b_none_d1_p4d.csv')
atm_f_gfs_uw_mean_b_none_d1_p0d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_uw_mean_b_none_d1_p0d.csv')
atm_f_gfs_uw_mean_b_none_d1_p1d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_uw_mean_b_none_d1_p1d.csv')
atm_f_gfs_uw_mean_b_none_d1_p2d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_uw_mean_b_none_d1_p2d.csv')
atm_f_gfs_uw_mean_b_none_d1_p3d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_uw_mean_b_none_d1_p3d.csv')
atm_f_gfs_uw_mean_b_none_d1_p4d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_uw_mean_b_none_d1_p4d.csv')
atm_f_gfs_vw_mean_b_none_d1_p0d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_vw_mean_b_none_d1_p0d.csv')
atm_f_gfs_vw_mean_b_none_d1_p1d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_vw_mean_b_none_d1_p1d.csv')
atm_f_gfs_vw_mean_b_none_d1_p2d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_vw_mean_b_none_d1_p2d.csv')
atm_f_gfs_vw_mean_b_none_d1_p3d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_vw_mean_b_none_d1_p3d.csv')
atm_f_gfs_vw_mean_b_none_d1_p4d = os.path.join(nas_path, 'databases/forecasted/atm_f_gfs_vw_mean_b_none_d1_p4d.csv')


# ----
# pixel count databases
# ----
# static

# observed
veg_o_modis_ndvi_mean_pc = os.path.join(nas_path, 'pcdatabases/observed/veg_o_modis_ndvi_mean_pc.csv')
veg_o_modis_evi_mean_pc = os.path.join(nas_path, 'pcdatabases/observed/veg_o_modis_evi_mean_pc.csv')
veg_o_int_nbr_mean_pc = os.path.join(nas_path, 'pcdatabases/observed/veg_o_int_nbr_mean_pc.csv')
snw_o_modis_sca_cum_n_pc = os.path.join(nas_path, 'pcdatabases/observed/snw_o_modis_sca_cum_n_pc.csv')
snw_o_modis_sca_cum_s_pc = os.path.join(nas_path, 'pcdatabases/observed/snw_o_modis_sca_cum_s_pc.csv')
et_o_modis_eto_cum_b_pc = os.path.join(nas_path, 'pcdatabases/observed/et_o_modis_eto_cum_b_pc.csv')
et_o_modis_eta_cum_b_pc = os.path.join(nas_path, 'pcdatabases/observed/et_o_modis_eta_cum_b_pc.csv')
veg_o_modis_lai_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/veg_o_modis_lai_mean_b_pc.csv')
veg_o_modis_fpar_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/veg_o_modis_fpar_mean_b_pc.csv')
pp_o_imerg_pp_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/pp_o_imerg_pp_mean_b_pc.csv')
# GLDAS products:
snw_o_gldas_swe_cum_b_pc = os.path.join(nas_path, 'pcdatabases/observed/snw_o_gldas_swe_cum_b_pc.csv')
tmp_f_gldas_tmp_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/tmp_f_gldas_tmp_mean_b_pc.csv')
et_o_gldas_eta_cum_b_pc = os.path.join(nas_path, 'pcdatabases/observed/et_o_gldas_eta_cum_b_pc.csv')
sm_o_gldas_sm_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/sm_o_gldas_sm_mean_b_pc.csv')
pp_o_pers_pp_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/pp_o_pers_pp_mean_b_pc.csv')
pp_o_pcdr_pp_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/pp_o_pcdr_pp_mean_b_pc.csv')
pp_o_pdir_pp_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/pp_o_pdir_pp_mean_b_pc.csv')
# ERA5 products:
tmp_o_era5_tmp_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/tmp_o_era5_tmp_mean_b_pc.csv')
pp_o_era5_pp_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/pp_o_era5_pp_mean_b_pc.csv')
et_o_era5_eto_cum_b_pc = os.path.join(nas_path, 'pcdatabases/observed/et_o_era5_eto_cum_b_pc.csv')
et_o_era5_et_cum_b_pc = os.path.join(nas_path, 'pcdatabases/observed/et_o_era5_et_cum_b_pc.csv')
snow_o_era5_sca_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/snow_o_era5_sca_b_mean_pc.csv')
snow_o_era5_sna_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/snow_o_era5_sna_b_mean_pc.csv') # snow albedo
snow_o_era5_snr_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/snow_o_era5_snr_b_mean_pc.csv') # snow density
snow_o_era5_snd_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/snow_o_era5_snd_b_mean_pc.csv') # snow depth
sm_o_era5_sm_mean_b_pc = os.path.join(nas_path, 'pcdatabases/observed/sm_o_era5_sm_mean_b_pc.csv') # soil moisture

# forecasted
pp_f_gfs_pp_max_pc_p0d = os.path.join(nas_path, 'pcdatabases/forecasted/pp_f_gfs_pp_max_pc_p0d.csv')
pp_f_gfs_pp_max_pc_p1d = os.path.join(nas_path, 'pcdatabases/forecasted/pp_f_gfs_pp_max_pc_p1d.csv')
pp_f_gfs_pp_max_pc_p2d = os.path.join(nas_path, 'pcdatabases/forecasted/pp_f_gfs_pp_max_pc_p2d.csv')
pp_f_gfs_pp_max_pc_p3d = os.path.join(nas_path, 'pcdatabases/forecasted/pp_f_gfs_pp_max_pc_p3d.csv')
pp_f_gfs_pp_max_pc_p4d = os.path.join(nas_path, 'pcdatabases/forecasted/pp_f_gfs_pp_max_pc_p4d.csv')
pp_f_gfs_pp_mean_pc_p0d = os.path.join(nas_path, 'pcdatabases/forecasted/pp_f_gfs_pp_mean_pc_p0d.csv')
pp_f_gfs_pp_mean_pc_p1d = os.path.join(nas_path, 'pcdatabases/forecasted/pp_f_gfs_pp_mean_pc_p1d.csv')
pp_f_gfs_pp_mean_pc_p2d = os.path.join(nas_path, 'pcdatabases/forecasted/pp_f_gfs_pp_mean_pc_p2d.csv')
pp_f_gfs_pp_mean_pc_p3d = os.path.join(nas_path, 'pcdatabases/forecasted/pp_f_gfs_pp_mean_pc_p3d.csv')
pp_f_gfs_pp_mean_pc_p4d = os.path.join(nas_path, 'pcdatabases/forecasted/pp_f_gfs_pp_mean_pc_p4d.csv')
awc_f_gfs_rh_mean_pc_p0d = os.path.join(nas_path, 'pcdatabases/forecasted/awc_f_gfs_rh_mean_pc_p0d.csv')
awc_f_gfs_rh_mean_pc_p1d = os.path.join(nas_path, 'pcdatabases/forecasted/awc_f_gfs_rh_mean_pc_p1d.csv')
awc_f_gfs_rh_mean_pc_p2d = os.path.join(nas_path, 'pcdatabases/forecasted/awc_f_gfs_rh_mean_pc_p2d.csv')
awc_f_gfs_rh_mean_pc_p3d = os.path.join(nas_path, 'pcdatabases/forecasted/awc_f_gfs_rh_mean_pc_p3d.csv')
awc_f_gfs_rh_mean_pc_p4d = os.path.join(nas_path, 'pcdatabases/forecasted/awc_f_gfs_rh_mean_pc_p4d.csv')
atm_f_gfs_gh_mean_pc_p0d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_gh_mean_pc_p0d.csv')
atm_f_gfs_gh_mean_pc_p1d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_gh_mean_pc_p1d.csv')
atm_f_gfs_gh_mean_pc_p2d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_gh_mean_pc_p2d.csv')
atm_f_gfs_gh_mean_pc_p3d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_gh_mean_pc_p3d.csv')
atm_f_gfs_gh_mean_pc_p4d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_gh_mean_pc_p4d.csv')
atm_f_gfs_uw_mean_pc_p0d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_uw_mean_pc_p0d.csv')
atm_f_gfs_uw_mean_pc_p1d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_uw_mean_pc_p1d.csv')
atm_f_gfs_uw_mean_pc_p2d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_uw_mean_pc_p2d.csv')
atm_f_gfs_uw_mean_pc_p3d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_uw_mean_pc_p3d.csv')
atm_f_gfs_uw_mean_pc_p4d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_uw_mean_pc_p4d.csv')
atm_f_gfs_vw_mean_pc_p0d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_vw_mean_pc_p0d.csv')
atm_f_gfs_vw_mean_pc_p1d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_vw_mean_pc_p1d.csv')
atm_f_gfs_vw_mean_pc_p2d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_vw_mean_pc_p2d.csv')
atm_f_gfs_vw_mean_pc_p3d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_vw_mean_pc_p3d.csv')
atm_f_gfs_vw_mean_pc_p4d = os.path.join(nas_path, 'pcdatabases/forecasted/atm_f_gfs_vw_mean_pc_p4d.csv')
tmp_f_gfs_tmp_mean_pc_p0d = os.path.join(nas_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_mean_pc_p0d.csv')
tmp_f_gfs_tmp_mean_pc_p1d = os.path.join(nas_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_mean_pc_p1d.csv')
tmp_f_gfs_tmp_mean_pc_p2d = os.path.join(nas_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_mean_pc_p2d.csv')
tmp_f_gfs_tmp_mean_pc_p3d = os.path.join(nas_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_mean_pc_p3d.csv')
tmp_f_gfs_tmp_mean_pc_p4d = os.path.join(nas_path, 'pcdatabases/forecasted/tmp_f_gfs_tmp_mean_pc_p4d.csv')

# ----
# log files
# ----
# observed
log_snw_o_modis_sca_cum = os.path.join(nas_path, 'logs/log_snw_o_modis_sca_cum.txt')
log_veg_o_modis_ndvi_mean = os.path.join(nas_path, 'logs/log_veg_o_modis_ndvi_mean.txt')
log_veg_o_modis_evi_mean = os.path.join(nas_path, 'logs/log_veg_o_modis_evi_mean.txt')
log_veg_o_int_nbr_mean = os.path.join(nas_path, 'logs/log_veg_o_int_nbr_mean.txt')
# log_sun_o_modis_al_mean_b_d16_p0d = os.path.join(nas_path, 'logs/log_sun_o_modis_al_mean_b_d16_p0d.txt')
# log_sun_o_modis_al_median_b_d16_p0d = os.path.join(nas_path, 'logs/log_sun_o_modis_al_median_b_d16_p0d.txt')
# log_sun_o_modis_al_p90_b_d16_p0d = os.path.join(nas_path, 'logs/log_sun_o_modis_al_p90_b_d16_p0d.txt')
# log_sun_o_modis_al_p10_b_d16_p0d = os.path.join(nas_path, 'logs/log_sun_o_modis_al_p10_b_d16_p0d.txt')
# log_sun_o_modis_al_p25_b_d16_p0d = os.path.join(nas_path, 'logs/log_sun_o_modis_al_p25_b_d16_p0d.txt')
# log_sun_o_modis_al_p75_b_d16_p0d = os.path.join(nas_path, 'logs/log_sun_o_modis_al_p75_b_d16_p0d.txt')
log_et_o_modis_eto_cum_b_d8_p0d = os.path.join(nas_path, 'logs/log_et_o_modis_eto_cum_b_d8_p0d.txt')
log_et_o_modis_eta_cum_b_d8_p0d = os.path.join(nas_path, 'logs/log_et_o_modis_eta_cum_b_d8_p0d.txt')
log_veg_o_modis_lai_mean = os.path.join(nas_path, 'logs/log_veg_o_modis_lai_mean.txt')
log_veg_o_modis_fpar_mean = os.path.join(nas_path, 'logs/log_veg_o_modis_fpar_mean.txt')
log_pp_o_imerg_pp_mean = os.path.join(nas_path, 'logs/log_pp_o_imerg_pp_mean.txt')
# GLDAS products:
log_snw_o_gldas_swe_cum = os.path.join(nas_path, 'logs/log_snw_o_gldas_swe_cum.txt')
log_tmp_f_gldas_tmp_mean = os.path.join(nas_path, 'logs/log_tmp_f_gldas_tmp_mean.txt')
log_et_o_gldas_eta_cum = os.path.join(nas_path, 'logs/log_et_o_gldas_eta_cum.txt')
log_sm_o_gldas_sm_mean = os.path.join(nas_path, 'logs/log_sm_o_gldas_sm_mean.txt')
log_pp_o_pers_pp_mean = os.path.join(nas_path, 'logs/log_pp_o_pers_pp_mean.txt')
log_pp_o_pcdr_pp_mean = os.path.join(nas_path, 'logs/log_pp_o_pcdr_pp_mean.txt')
log_pp_o_pdir_pp_mean = os.path.join(nas_path, 'logs/log_pp_o_pdir_pp_mean.txt')
# ERA5 products:
log_tmp_o_era5_tmp_mean = os.path.join(nas_path, 'logs/log_tmp_o_era5_tmp_mean.txt')
log_pp_o_era5_pp_mean = os.path.join(nas_path, 'logs/log_pp_o_era5_pp_mean.txt')
log_et_o_era5_eto_cum = os.path.join(nas_path, 'logs/log_et_o_era5_eto_cum.txt')
log_et_o_era5_et_cum = os.path.join(nas_path, 'logs/log_et_o_era5_et_cum.txt')
log_snow_o_era5_sca = os.path.join(nas_path, 'logs/log_snow_o_era5_sca.txt')
log_snow_o_era5_sna = os.path.join(nas_path, 'logs/log_snow_o_era5_sna.txt')
log_snow_o_era5_snr = os.path.join(nas_path, 'logs/log_snow_o_era5_snr.txt')
log_snow_o_era5_snd = os.path.join(nas_path, 'logs/log_snow_o_era5_snd.txt')
log_sm_o_era5_sm_mean = os.path.join(nas_path, 'logs/log_sm_o_era5_sm_mean.txt')

log_file_maintainer = os.path.join(nas_path, 'logs/file_maintainer.txt')

# forecasted
log_pp_f_gfs_pp_max_log = os.path.join(nas_path, 'logs/pp_f_gfs_pp_max_log.txt')
log_pp_f_gfs_pp_mean_log = os.path.join(nas_path, 'logs/pp_f_gfs_pp_mean_log.txt')
log_awc_f_gfs_rh_mean_log = os.path.join(nas_path, 'logs/awc_f_gfs_rh_mean_log.txt')
log_atm_f_gfs_gh_mean_log = os.path.join(nas_path, 'logs/atm_f_gfs_gh_mean_log.txt')
log_atm_f_gfs_uw_mean_log = os.path.join(nas_path, 'logs/atm_f_gfs_uw_mean_log.txt')
log_atm_f_gfs_vw_mean_log = os.path.join(nas_path, 'logs/atm_f_gfs_vw_mean_log.txt')
log_tmp_f_gfs_tmp_mean_log = os.path.join(nas_path, 'logs/tmp_f_gfs_tmp_mean_log.txt')

"""
polys = gpd.read_file(hidrocl_sinusoidal)  # for getting gauge_id values
catchment_names = polys.gauge_id.tolist()
del polys
"""