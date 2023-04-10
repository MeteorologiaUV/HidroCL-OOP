import hidrocl
import hidrocl.paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

pp = hidrocl.HidroCLVariable("pp",
                             hcl.pp_o_era5_pp_mean_b_d_p0d,
                             hcl.pp_o_era5_pp_mean_b_pc)

dew = hidrocl.HidroCLVariable("dew",
                              hcl.tmp_o_era5_dew_mean_b_none_d1_p0d,
                              hcl.tmp_o_era5_dew_mean_b_pc)

pres = hidrocl.HidroCLVariable("pres",
                               hcl.atm_o_era5_pres_mean_b_none_d1_p0d,
                               hcl.atm_o_era5_pres_mean_b_pc)

u = hidrocl.HidroCLVariable("u",
                            hcl.wind_o_era5_u10_mean_b_none_d1_p0d,
                            hcl.wind_o_era5_u10_mean_b_pc)

v = hidrocl.HidroCLVariable("v",
                            hcl.wind_o_era5_v10_mean_b_none_d1_p0d,
                            hcl.wind_o_era5_v10_mean_b_pc)


vc = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = vc.gauge_id.tolist()

pp.catchment_names = catchment_names
dew.catchment_names = catchment_names
pres.catchment_names = catchment_names
u.catchment_names = catchment_names
v.catchment_names = catchment_names

pp.checkdatabase()
pp.checkpcdatabase()
dew.checkdatabase()
dew.checkpcdatabase()
pres.checkdatabase()
pres.checkpcdatabase()
u.checkdatabase()
u.checkpcdatabase()
v.checkdatabase()
v.checkpcdatabase()

era5 = hidrocl.Era5(pp=pp, dew=dew, pres=pres, u=u, v=v,
                    pp_log=hcl.log_pp_o_era5_pp_mean,
                    dew_log=hcl.log_tmp_o_era5_dew_mean,
                    pres_log=hcl.log_atm_o_era5_pres_mean,
                    u_log=hcl.log_wind_o_era5_u10_mean,
                    v_log=hcl.log_wind_o_era5_v10_mean,
                    product_path=hcl.era5_hourly_path,
                    vector_path=hcl.hidrocl_wgs84)

era5.run_extraction()
