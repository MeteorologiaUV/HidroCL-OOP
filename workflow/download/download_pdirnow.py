import hidrocl
from hidrocl import paths as hcl

hidrocl.download.download_pdirnow('2023-01-01', '2023-12-31', hcl.pdirnow, check_ppath=True)