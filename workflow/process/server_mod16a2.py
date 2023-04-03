import hidrocl
import hidrocl_paths as hcl
import geopandas as gpd
print(hidrocl.__version__)

pet = hidrocl.HidroCLVariable("pet",
                               hcl.et_o_modis_eto_cum_b_d8_p0d,
                               hcl.et_o_modis_eto_cum_b_pc)

et = hidrocl.HidroCLVariable("et",
                               hcl.et_o_modis_eta_cum_b_d8_p0d,
                               hcl.et_o_modis_eta_cum_b_pc)

v = gpd.read_file(hcl.hidrocl_wgs84)
catchment_names = v.gauge_id.tolist()

pet.catchment_names = catchment_names
pet.checkdatabase()
pet.checkpcdatabase()
et.catchment_names = catchment_names
et.checkdatabase()
et.checkpcdatabase()


mod16 = hidrocl.Mod16a2(pet,
                        et,
                        product_path=hcl.mod16a2_path,
                        vector_path=hcl.hidrocl_sinusoidal,
                        pet_log=hcl.log_et_o_modis_eto_cum_b_d8_p0d,
                        et_log=hcl.log_et_o_modis_eta_cum_b_d8_p0d)

mod16.run_extraction()