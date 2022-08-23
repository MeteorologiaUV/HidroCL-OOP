# coding=utf-8

from pathlib import Path
from tempfile import TemporaryDirectory
from ..variables import HidroCLVariable
from . import tools as t
from . import extractions as e


class Test:
    def __init__(self, ndvi):
        if isinstance(ndvi, HidroCLVariable):
            self.ndvi = ndvi
            print('All good')
        else:
            raise TypeError('ndvi must be HidroCLVariable object')


class Mod13q1:
    """class to process MOD13Q1 to hidrocl variables

    Parameters:
    ndvi (HidroCLVariable): ndvi variable
    evi (HidroCLVariable): evi variable
    nbr (HidroCLVariable): nbr variable
    product_path (str): path to the product"""

    def __init__(self, ndvi, evi, nbr, product_path, vector_path,
                 ndvi_log, evi_log, nbr_log):
        if t.check_instance(ndvi, evi, nbr):
            self.ndvi = ndvi
            self.evi = evi
            self.nbr = nbr
            self.ndvi_log = ndvi_log
            self.evi_log = evi_log
            self.nbr_log = nbr_log
            self.productname = "MODIS MOD13Q1 Version 0.61"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = t.compare_indatabase(self.ndvi.indatabase,
                                                        self.evi.indatabase,
                                                        self.nbr.indatabase)
            self.product_files = t.read_product_files(self.productpath, "modis")
            self.product_ids = t.get_product_ids(self.product_files, "modis")
            self.all_scenes = t.check_product_files(self.product_ids)
            self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
            (self.overpopulated_scenes,
             self.complete_scenes,
             self.incomplete_scenes) = t.classify_ocurrences(self.scenes_occurrences, "modis")
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)
        else:
            raise TypeError('ndvi, evi and nbr must be HidroCLVariable objects')

    def __repr__(self):
        return f'Class to extract {self.productname}'

    def __str__(self):
        return f'''
Product: {self.productname}

NDVI records: {len(self.ndvi.indatabase)}.
NDVI database path: {self.ndvi.database}

EVI records: {len(self.evi.indatabase)}.
EVI database path: {self.evi.database}

NBR records: {len(self.nbr.indatabase)}.
NBR database path: {self.nbr.database}
        '''

    def run_extraction(self, limit=None):
        """run extraction"""

        with t.HiddenPrints():
            self.ndvi.checkdatabase()
            self.evi.checkdatabase()
            self.nbr.checkdatabase()

        self.common_elements = t.compare_indatabase(self.ndvi.indatabase,
                                                    self.evi.indatabase,
                                                    self.nbr.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                if scene not in self.ndvi.indatabase:
                    e.weighted_mean_modis(scene, scenes_path,
                                          temp_dir, 'ndvi', self.vectorpath,
                                          self.ndvi.database, self.ndvi.pcdatabase,
                                          self.ndvi.catchment_names, self.ndvi_log,
                                          layer="250m 16 days NDVI",)

                if scene not in self.evi.indatabase:
                    e.weighted_mean_modis(scene, scenes_path,
                                          temp_dir, 'evi', self.vectorpath,
                                          self.evi.database, self.evi.pcdatabase,
                                          self.evi.catchment_names, self.evi_log,
                                          layer="250m 16 days EVI",)

                if scene not in self.evi.indatabase:
                    e.weighted_mean_modis(scene, scenes_path,
                                          temp_dir, 'nbr', self.vectorpath,
                                          self.nbr.database, self.nbr.pcdatabase,
                                          self.nbr.catchment_names, self.nbr_log,
                                          layer1="250m 16 days NIR reflectance",
                                          layer2="250m 16 days MIR reflectance")
