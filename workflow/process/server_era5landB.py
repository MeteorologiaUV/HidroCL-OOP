import hidrocl
import hidrocl.paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

hidrocl.variables.create = True

path = '/Users/aldotapia/hidrocl_test/era5land/dbs'

eto = hidrocl.HidroCLVariable("eto",
                              f'{path}/et_o_era5_eta_mean.csv',
                              f'{path}/et_o_era5_eta_pc.csv',
                              )

et = hidrocl.HidroCLVariable("et",
                                f'{path}/et_o_era5_eto_mean.csv',
                                f'{path}/et_o_era5_eto_pc.csv')

sca = hidrocl.HidroCLVariable("sca",
                                f'{path}/snw_o_era5_sca_mean.csv',
                                f'{path}/snw_o_era5_sca_pc.csv')

sna = hidrocl.HidroCLVariable("sna",
                                f'{path}/snw_o_era5_sna_mean.csv',
                                f'{path}/snw_o_era5_sna_pc.csv')
# density
snr = hidrocl.HidroCLVariable("snr",
                                f'{path}/snw_o_era5_snr_mean.csv',
                                f'{path}/snw_o_era5_snr_pc.csv')
# depth
snd = hidrocl.HidroCLVariable("snd",
                                f'{path}/snw_o_era5_snd_mean.csv',
                                f'{path}/snw_o_era5_snd_pc.csv')

sm = hidrocl.HidroCLVariable("sm",
                                f'{path}/swc_o_era5_sm_mean.csv',
                                f'{path}/swc_o_era5_sm_pc.csv')

v = gpd.read_file('/Users/aldotapia/Documents/Fondef/2000_2022/HidroCL_boundaries/HidroCL_boundaries.shp')
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
                         et_log=f'{path}/log_et_o_era5_eta_mean.txt',
                         pet_log=f'{path}/log_et_o_era5_eto_mean.txt',
                         snw_log=   f'{path}/log_snw_o_era5_sca_mean.txt',
                         snwa_log=  f'{path}/log_snw_o_era5_sna_mean.txt',
                         snwdn_log= f'{path}/log_snw_o_era5_snr_mean.txt',
                         snwdt_log= f'{path}/log_snw_o_era5_snd_mean.txt',
                         soilm_log= f'{path}/log_swc_o_era5_sm_mean.txt',
                         product_path='/Users/aldotapia/hidrocl_test/era5land',
                         vector_path='/Users/aldotapia/Documents/Fondef/2000_2022/HidroCL_boundaries/HidroCL_boundaries.shp')

era5.run_extraction()
