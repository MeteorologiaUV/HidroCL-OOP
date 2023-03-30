import os
import glob
import shutil

path = "/mnt/nas/observed/IMERG_GIS"
os.chdir(path)
for file in glob.glob("*.tif"):
    """get future subfolder from name"""
    folder = file.split(".")[4][:4]
    """copy file to new folder using shutil.copyfile"""
    shutil.copyfile(file, os.path.join(path, folder, file))
    """remove file from old folder"""
    os.remove(file)
    print(f'Done with {file}')
