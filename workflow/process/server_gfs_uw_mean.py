import hidrocl
import hidrocl.paths as hcl
import geopandas as gpd

gfs_d0 = hidrocl.HidroCLVariable('test gfs día 0',
                                 hcl.atm_f_gfs_uw_mean_b_none_d1_p0d,
                                 hcl.atm_f_gfs_uw_mean_pc_p0d)
gfs_d1 = hidrocl.HidroCLVariable('test gfs día 1',
                                 hcl.atm_f_gfs_uw_mean_b_none_d1_p1d,
                                 hcl.atm_f_gfs_uw_mean_pc_p1d)
gfs_d2 = hidrocl.HidroCLVariable('test gfs día 2',
                                 hcl.atm_f_gfs_uw_mean_b_none_d1_p2d,
                                 hcl.atm_f_gfs_uw_mean_pc_p2d)
gfs_d3 = hidrocl.HidroCLVariable('test gfs día 3',
                                 hcl.atm_f_gfs_uw_mean_b_none_d1_p3d,
                                 hcl.atm_f_gfs_uw_mean_pc_p3d)
gfs_d4 = hidrocl.HidroCLVariable('test gfs día 4',
                                 hcl.atm_f_gfs_uw_mean_b_none_d1_p4d,
                                 hcl.atm_f_gfs_uw_mean_pc_p4d)

v = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = v.gauge_id.tolist()

gfs_d0.catchment_names = catchment_names
gfs_d1.catchment_names = catchment_names
gfs_d2.catchment_names = catchment_names
gfs_d3.catchment_names = catchment_names
gfs_d4.catchment_names = catchment_names

gfs_d0.checkdatabase()
gfs_d0.checkpcdatabase()
gfs_d1.checkdatabase()
gfs_d1.checkpcdatabase()
gfs_d2.checkdatabase()
gfs_d2.checkpcdatabase()
gfs_d3.checkdatabase()
gfs_d3.checkpcdatabase()
gfs_d4.checkdatabase()
gfs_d4.checkpcdatabase()

gfs = hidrocl.products.Gfs(db0=gfs_d0,
                           db1=gfs_d1,
                           db2=gfs_d2,
                           db3=gfs_d3,
                           db4=gfs_d4,
                           db_log=hcl.log_atm_f_gfs_uw_mean_log,
                           variable='u10',
                           aggregation='mean',
                           product_path=hcl.gfs,
                           vectorpath=hcl.hidrocl_wgs84)

gfs.run_extraction()
