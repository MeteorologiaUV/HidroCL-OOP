import hidrocl
import hidrocl.paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

pp = hidrocl.HidroCLVariable("pp",
                             "/Users/aldotapia/hidrocl_test/rain/imerg.csv",
                             "/Users/aldotapia/hidrocl_test/rain/imerg_pc.csv")

v = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = v.gauge_id.tolist()

pp.catchment_names = catchment_names

pp.checkdatabase()
pp.checkpcdatabase()

imerg = hidrocl.ImergGIS(pp,
                         product_path="/Users/aldotapia/hidrocl_test/rain/2023",
                         vector_path=hcl.hidrocl_wgs84,
                         pp_log="/Users/aldotapia/hidrocl_test/rain/imerg_log.txt")

imerg.run_extraction()
