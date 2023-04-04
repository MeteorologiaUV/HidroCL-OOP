import os
import glob
import shutil
import hidrocl.paths as hcl

path = hcl.era5_land_hourly_path
os.chdir(path)
for file in glob.glob("*.nc"):
    """get future subfolder from name"""
    folder = file.split("_")[1][:4]
    """copy or create the folder if fails"""
    os.makedirs(os.path.join(path, folder), exist_ok=True)
    shutil.copyfile(file, os.path.join(path, folder, file))
    """remove file from old folder"""
    os.remove(file)
    print(f'Done with {file}')
