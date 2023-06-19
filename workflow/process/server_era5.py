import hidrocl
import hidrocl.paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

pp = hidrocl.HidroCLVariable("pp",
                             hcl.pp_o_era5_pp_mean,
                             hcl.pp_o_era5_pp_pc)

ppmax = hidrocl.HidroCLVariable("ppmax",
                                hcl.pp_o_era5_maxpp_mean,
                                hcl.pp_o_era5_maxpp_pc)

temp = hidrocl.HidroCLVariable("temp",
                               hcl.tmp_o_era5_tmp_mean,
                               hcl.tmp_o_era5_tmp_pc)

tempmin = hidrocl.HidroCLVariable("tempmin",
                                  hcl.tmp_o_era5_tmin_mean,
                                  hcl.tmp_o_era5_tmin_pc)

tempmax = hidrocl.HidroCLVariable("tempmax",
                                  hcl.tmp_o_era5_tmax_mean,
                                  hcl.tmp_o_era5_tmax_pc)

dew = hidrocl.HidroCLVariable("dew",
                              hcl.tmp_o_era5_dew_mean,
                              hcl.tmp_o_era5_dew_pc)

pres = hidrocl.HidroCLVariable("pres",
                               hcl.atm_o_era5_pres_mean,
                               hcl.atm_o_era5_pres_pc)

u = hidrocl.HidroCLVariable("u",
                            hcl.atm_o_era5_uw_mean,
                            hcl.atm_o_era5_uw_pc)

v = hidrocl.HidroCLVariable("v",
                            hcl.atm_o_era5_vw_mean,
                            hcl.atm_o_era5_vw_pc)


vc = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = vc.gauge_id.tolist()

pp.catchment_names = catchment_names
ppmax.catchment_names = catchment_names
dew.catchment_names = catchment_names
pres.catchment_names = catchment_names
u.catchment_names = catchment_names
v.catchment_names = catchment_names

pp.checkdatabase()
pp.checkpcdatabase()
ppmax.checkdatabase()
ppmax.checkpcdatabase()
temp.checkdatabase()
temp.checkpcdatabase()
tempmin.checkdatabase()
tempmin.checkpcdatabase()
tempmax.checkdatabase()
tempmax.checkpcdatabase()
dew.checkdatabase()
dew.checkpcdatabase()
pres.checkdatabase()
pres.checkpcdatabase()
u.checkdatabase()
u.checkpcdatabase()
v.checkdatabase()
v.checkpcdatabase()


era5 = hidrocl.Era5(pp=pp,
                    ppmax=ppmax,
                    temp=temp, tempmin=tempmin, tempmax=tempmax,
                    dew=dew, pres=pres, u=u, v=v,
                    pp_log=hcl.log_pp_o_era5_pp_mean,
                    ppmax_log=hcl.log_pp_o_era5_maxpp_mean,
                    temp_log=hcl.log_tmp_o_era5_tmp_mean,
                    tempmin_log=hcl.log_tmp_o_era5_tmin_mean,
                    tempmax_log=hcl.log_tmp_o_era5_tmax_mean,
                    dew_log=hcl.log_tmp_o_era5_dew_mean,
                    pres_log=hcl.log_atm_o_era5_pres_mean,
                    u_log=hcl.log_wind_o_era5_u10_mean,
                    v_log=hcl.log_wind_o_era5_v10_mean,
                    product_path=hcl.era5_hourly_path,
                    vector_path=hcl.hidrocl_wgs84)
era5.run_extraction()
