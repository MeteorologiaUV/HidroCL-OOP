import hidrocl
import hidrocl.paths as hcl

era5pre = hidrocl.preprocess.Era5_pre_rh(product_path=hcl.era5_hourly_path,
                                         output_path=hcl.era5_relative_humidity_path)

era5pre.run_extraction()
