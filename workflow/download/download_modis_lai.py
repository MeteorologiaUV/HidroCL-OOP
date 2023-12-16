import hidrocl
import hidrocl.paths as hcl

hidrocl.download.earthdata_download('lai', hcl.mcd15a2h_path, '2022-07-30','2024-01-01')