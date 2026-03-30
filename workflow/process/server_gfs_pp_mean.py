import hidrocl
import hidrocl.paths as hcl


hidrocl.variables.create = True

path = '/Users/aldotapia/Documents/GitHub/HidroCL-OOP/tests/ddbb2/'

pp_f_gfs_pp_mean_b_none_d1_p0d = path + 'pp_p0d.csv'
pp_f_gfs_pp_mean_pc_p0d = path + 'pp_p0d_pc.csv'
pp_f_gfs_pp_mean_b_none_d1_p1d = path + 'pp_p1d.csv'
pp_f_gfs_pp_mean_pc_p1d = path + 'pp_p1d_pc.csv'
pp_f_gfs_pp_mean_b_none_d1_p2d = path + 'pp_p2d.csv'
pp_f_gfs_pp_mean_pc_p2d = path + 'pp_p2d_pc.csv'
pp_f_gfs_pp_mean_b_none_d1_p3d = path + 'pp_p3d.csv'
pp_f_gfs_pp_mean_pc_p3d = path + 'pp_p3d_pc.csv'
pp_f_gfs_pp_mean_b_none_d1_p4d = path + 'pp_p4d.csv'
pp_f_gfs_pp_mean_pc_p4d = path + 'pp_p4d_pc.csv'

log_pp_f_gfs_pp_mean_log = path + 'pp_gfs_pp_mean_log.csv'
gfs = '/Users/aldotapia/Documents/GitHub/HidroCL-OOP/tests/newgfs'
hidrocl_wgs84 = '/Users/aldotapia/Downloads/drive-download-20260105T215845Z-3-001/HidroCL_boundaries.shp'



gfs_d0 = hidrocl.HidroCLVariable('test gfs día 0',
                                 pp_f_gfs_pp_mean_b_none_d1_p0d,
                                 pp_f_gfs_pp_mean_pc_p0d)
gfs_d1 = hidrocl.HidroCLVariable('test gfs día 1',
                                 pp_f_gfs_pp_mean_b_none_d1_p1d,
                                 pp_f_gfs_pp_mean_pc_p1d)
gfs_d2 = hidrocl.HidroCLVariable('test gfs día 2',
                                 pp_f_gfs_pp_mean_b_none_d1_p2d,
                                 pp_f_gfs_pp_mean_pc_p2d)
gfs_d3 = hidrocl.HidroCLVariable('test gfs día 3',
                                 pp_f_gfs_pp_mean_b_none_d1_p3d,
                                 pp_f_gfs_pp_mean_pc_p3d)
gfs_d4 = hidrocl.HidroCLVariable('test gfs día 4',
                                 pp_f_gfs_pp_mean_b_none_d1_p4d,
                                 pp_f_gfs_pp_mean_pc_p4d)

import geopandas as gpd
v = gpd.read_file(hidrocl_wgs84)
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
                           db_log=log_pp_f_gfs_pp_mean_log,
                           variable='prate',
                           aggregation='sum',
                           product_path=gfs,
                           vectorpath=hidrocl_wgs84)

gfs.run_extraction()
gfs.run_maintainer()
