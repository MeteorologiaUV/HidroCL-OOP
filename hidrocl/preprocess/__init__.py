# coding=utf-8

import os
import sys
import xarray
from pathlib import Path

class HiddenPrints:
    """
    Context manager to suppress stdout and stderr.
    """
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr


def read_era5_files(productpath):
    """
    Read remote sensing/modeling product files

    Args:
        productpath (str): Path to the product folder where the product files are located

    Returns:
        list: List of product files in the product folder
    """

    return [str(value.relative_to(productpath)) for value in Path(productpath).rglob('*.nc')]


def compute_rh(file, output_file):
    """
    Compute relative humidity from ERA5 2m temperature and 2m dew point temperature

    Args:
        file (xarray.Dataset):
        output_file (str):

    Returns:

    """

    with HiddenPrints():

        da = xarray.open_dataset(file, mask_and_scale=True)

        if isinstance(da, xarray.Dataset):
            pass
        else:
            raise TypeError(f"file is not a xarray.Dataset object: {file}")

        if ('t2m' in list(da.data_vars)) and ('d2m' in list(da.data_vars)):
            t2m = da['t2m'] - 273.15
            d2m = da['d2m'] - 273.15
            e = 6.11 * 10 ** (7.5 * d2m / (237.3 + d2m))
            es = 6.11 * 10 ** (7.5 * t2m / (237.3 + t2m))
            rh = (e / es * 100)
            rh = rh.rename('rh')
            rh.mean(dim='time').to_netcdf(output_file)
        else:
            raise ValueError(f"t2m or d2m not in file {file}")

class Era5_pre_rh:
    """
    A class to process ERA5 hourly data to compute relative humidity

    Attributes:
        product_path (str): Path to the product folder where the product files are located \n
        output_path (str): Path to the output folder where the output files will be located \n
        product_files (list): List of product files in the product folder \n
        processed_files (list): List of processed files \n
    """

    def __init__(self, product_path, output_path):
        """
        Examples:
            >>> from hidrocl import Era5_pre_rh
            >>>


        Args:
            product_path (str): Path to the product folder where the product files are located
            output_path (str): Path to the output folder where the output files will be located

        Raises:
            # TypeError: If z is not HidroCLVariable object \n
        """
        self.product_path = product_path
        self.output_path = output_path
        self.product_files = read_era5_files(self.product_path)
        self.processed_files = read_era5_files(self.output_path)
        self.to_process = [value for value in self.product_files if value not in self.processed_files]

        if not self.product_files:
            raise ValueError("No files found in product path")

        if not self.to_process:
            print("All files have been processed")
        else:
            # sort files to_process
            self.to_process.sort()
            print(f"{len(self.to_process)} files to process")

    def run_extraction(self):
        """
        Run the extraction of the product.

        Returns:
            str: Print
        """

        for file in self.to_process:
            output_file = os.path.join(self.output_path, file)
            output_path = os.path.dirname(output_file)
            # create subfolder if it does not exist
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            compute_rh(os.path.join(self.product_path, file), output_file)
            print(f"Processed file: {file.split('/')[-1]}")
