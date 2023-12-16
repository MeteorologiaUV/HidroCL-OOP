import hidrocl
import hidrocl.paths as hcl

hidrocl.download.earthdata_download('lulc', hcl.mcd12q1_path, '2020-12-01','2024-01-01')