import hidrocl
import hidrocl.paths as hcl

hidrocl.download.earthdata_download('snow', hcl.mod13q1_path, '2022-01-01','2024-01-01')