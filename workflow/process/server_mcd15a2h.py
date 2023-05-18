import hidrocl
import hidrocl.paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

lai = hidrocl.HidroCLVariable("lai",
                              hcl.veg_o_modis_lai_mean,
                              hcl.veg_o_modis_lai_pc)

fpar = hidrocl.HidroCLVariable("fpar",
                               hcl.veg_o_modis_fpar_mean,
                               hcl.veg_o_modis_fpar_pc)

v = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = v.gauge_id.tolist()

lai.catchment_names = catchment_names
lai.checkdatabase()
lai.checkpcdatabase()
fpar.catchment_names = catchment_names
fpar.checkdatabase()
fpar.checkpcdatabase()

mcd15 = hidrocl.Mcd15a2h(lai, fpar,
                         product_path=hcl.mcd15a2h_path,
                         vector_path=hcl.hidrocl_sinusoidal,
                         lai_log=hcl.log_veg_o_modis_lai_mean,
                         fpar_log=hcl.log_veg_o_modis_fpar_mean)

mcd15.run_extraction()
