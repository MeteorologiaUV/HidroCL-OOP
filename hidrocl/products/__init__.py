# coding=utf-8

from pathlib import Path
from tempfile import TemporaryDirectory
from ..variables import HidroCLVariable
from . import tools as t
from . import extractions as e


""""
Extraction of MODIS MOD13Q1 product:
"""


class Mod13q1:
    """
    A class to process MOD13Q1 to hidrocl variables

    Attributes
    ----------
    ndvi : HidroCLVariable
        HidroCLVariable object with the NDVI data
    evi : HidroCLVariable
        HidroCLVariable object with the EVI data
    nbr : HidroCLVariable
        HidroCLVariable object with the NBR data
    ndvi_log : str
        Path to the log file for the NDVI extraction
    evi_log : str
        Path to the log file for the EVI extraction
    nbr_log : str
        Path to the log file for the NBR extraction
    productname : str
        Name of the remote sensing product to be processed
    productpath : str
        Path to the product folder where the product files are located
    vectorpath : str
        Path to the vector folder with Shapefile with areas to be processed
    common_elements : list
        List of common elements between the NDVI, EVI and NBR databases
    product_files : list
        List of product files in the product folder
    product_ids : list
        List of product ids. Each product id is str with common tag by date
    all_scenes : list
        List of all scenes (no matter the product id here)
    scenes_occurrences : list
        List of scenes occurrences for each product id
    overpopulated_scenes : list
        List of overpopulated scenes (more than 9 scenes for modis)
    complete_scenes : list
        List of complete scenes (9 scenes for modis)
    incomplete_scenes : list
        List of incomplete scenes (less than 9 scenes for modis)
    scenes_to_process : list
        List of scenes to process (complete scenes no processed)
    """

    def __init__(self, ndvi, evi, nbr, product_path, vector_path,
                 ndvi_log, evi_log, nbr_log):
        """
        Parameters
        ----------
        :param ndvi: HidroCLVariable
            Object with the NDVI data
        :param evi: HidroCLVariable
            Object with the EVI data
        :param nbr: HidroCLVariable
            Object with the NBR data
        :param product_path: str
            Path to the product folder
        :param vector_path: str
            Path to the vector folder
        :param ndvi_log: str
            Path to the log file for the NDVI extraction
        :param evi_log: str
            Path to the log file for the EVI extraction
        :param nbr_log: str
            Path to the log file for the NBR extraction
        """
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
             self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "modis")
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)
        else:
            raise TypeError('ndvi, evi and nbr must be HidroCLVariable objects')

    def __repr__(self):
        """
        Return a string representation of the object

        :return: str
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        :return: str
        """
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
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        :param limit: int (length of the scenes_to_process)
        :return: Print
        """

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
                                          temp_dir, 'ndvi',
                                          self.ndvi.catchment_names, self.ndvi_log,
                                          database=self.ndvi.database,
                                          pcdatabase=self.ndvi.pcdatabase,
                                          vector_path=self.vectorpath,
                                          layer="250m 16 days NDVI",)

                if scene not in self.evi.indatabase:
                    e.weighted_mean_modis(scene, scenes_path,
                                          temp_dir, 'evi',
                                          self.evi.catchment_names, self.evi_log,
                                          database=self.evi.database,
                                          pcdatabase=self.evi.pcdatabase,
                                          vector_path=self.vectorpath,
                                          layer="250m 16 days EVI",)

                if scene not in self.evi.indatabase:
                    e.weighted_mean_modis(scene, scenes_path,
                                          temp_dir, 'nbr',
                                          self.nbr.catchment_names, self.nbr_log,
                                          database=self.nbr.database,
                                          pcdatabase=self.nbr.pcdatabase,
                                          vector_path=self.vectorpath,
                                          layer1="250m 16 days NIR reflectance",
                                          layer2="250m 16 days MIR reflectance")


""""
Extraction of MODIS MOD10A2 product:
"""


class Mod10a2:
    """
    A class to process MOD10A2 to hidrocl variables

    Attributes
    ----------
    nsnow : HidroCLVariable
        HidroCLVariable with the snow data
    ssnow : HidroCLVariable
        HidroCLVariable with the snow data
    snow_log : str
        Path to the log file for the snow extraction
    productname : str
        Name of the remote sensing product to be processed
    productpath : str
        Path to the product folder where the product files are located
    northvectorpath : str
        Path to the vector folder with the north Shapefile with areas to be processed
    southvectorpath : str
        Path to the vector folder with the south Shapefile with areas to be processed
    common_elements : list
        List of common elements between the NDVI, EVI and NBR databases
    product_files : list
        List of product files in the product folder
    product_ids : list
        List of product ids. Each product id is str with common tag by date
    all_scenes : list
        List of all scenes (no matter the product id here)
    scenes_occurrences : list
        List of scenes occurrences for each product id
    overpopulated_scenes : list
        List of overpopulated scenes (more than 9 scenes for modis)
    complete_scenes : list
        List of complete scenes (9 scenes for modis)
    incomplete_scenes : list
        List of incomplete scenes (less than 9 scenes for modis)
    scenes_to_process : list
        List of scenes to process (complete scenes no processed)
    """

    def __init__(self, nsnow, ssnow, product_path,
                 north_vector_path, south_vector_path, snow_log):
        """
        Parameters
        ----------
        :param nsnow : HidroCLVariable
            Object with the north face snow data
        :param ssnow: HidroCLVariable
            Object with the south face snow data
        :param product_path: str
            Path to the product folder
        :param north_vector_path: str
            Path to the north vector folder
        :param south_vector_path: str
            Path to the south vector folder
        :param snow_log: str
            Path to the snow log file
        """
        if t.check_instance(nsnow, ssnow):
            self.nsnow = nsnow
            self.ssnow = ssnow
            self.snow_log = snow_log
            self.productname = "MODIS MOD10A2 Version 0.61"
            self.productpath = product_path
            self.northvectorpath = north_vector_path
            self.southvectorpath = south_vector_path
            self.common_elements = t.compare_indatabase(self.nsnow.indatabase,
                                                        self.ssnow.indatabase)
            self.product_files = t.read_product_files(self.productpath, "modis")
            self.product_ids = t.get_product_ids(self.product_files, "modis")
            self.all_scenes = t.check_product_files(self.product_ids)
            self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
            (self.overpopulated_scenes,
             self.complete_scenes,
             self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "modis")
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)
        else:
            raise TypeError('nsnow and ssnow must be HidroCLVariable objects')

    def __repr__(self):
        """
        Return a string representation of the object

        :return: str
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        :return: str
        """
        return f'''
Product: {self.productname}

North face snow records: {len(self.nsnow.indatabase)}.
North face snow path: {self.nsnow.database}

South face snow records: {len(self.ssnow.indatabase)}.
South face snow database path: {self.ssnow.database}
                '''

    def run_extraction(self, limit=None):
        """run extraction"""

        with t.HiddenPrints():
            self.nsnow.checkdatabase()
            self.ssnow.checkdatabase()

        self.common_elements = t.compare_indatabase(self.nsnow.indatabase,
                                                    self.ssnow.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                if scene not in self.nsnow.indatabase:  # so what about the south one?
                    e.weighted_mean_modis(scene, scenes_path,
                                          temp_dir, 'snow',
                                          self.nsnow.catchment_names, self.snow_log,
                                          north_database=self.nsnow.database,
                                          north_pcdatabase=self.nsnow.pcdatabase,
                                          south_database=self.ssnow.database,
                                          south_pcdatabase=self.ssnow.pcdatabase,
                                          north_vector_path=self.northvectorpath,
                                          south_vector_path=self.southvectorpath,
                                          layer="Maximum_Snow_Extent")


class Mod16a2:

    """
    A class to process MOD13Q1 to hidrocl variables

    Attributes
    ----------
    pet : HidroCLVariable
        HidroCLVariable object with the potential evapotranspoira
    pet_log : str
        Path to the log file for the pet extraction
    productname : str
        Name of the remote sensing product to be processed
    productpath : str
        Path to the product folder where the product files are located
    vectorpath : str
        Path to the vector folder with Shapefile with areas to be processed
    product_files : list
        List of product files in the product folder
    product_ids : list
        List of product ids. Each product id is str with common tag by date
    all_scenes : list
        List of all scenes (no matter the product id here)
    scenes_occurrences : list
        List of scenes occurrences for each product id
    overpopulated_scenes : list
        List of overpopulated scenes (more than 9 scenes for modis)
    complete_scenes : list
        List of complete scenes (9 scenes for modis)
    incomplete_scenes : list
        List of incomplete scenes (less than 9 scenes for modis)
    scenes_to_process : list
        List of scenes to process (complete scenes no processed)
    """

    def __init__(self, pet, product_path, vector_path, pet_log):
        """
        Parameters
        ----------
        :param pet: HidroCLVariable
            Object with the potential evapotranspiration data
        :param product_path: str
            Path to the product folder
        :param vector_path: str
            Path to the vector folder
        :param pet_log: str
            Path to the log file for the PET extraction
        """
        if t.check_instance(pet):
            self.pet = pet
            self.pet_log = pet_log
            self.productname = "MODIS MOD16A2 Version 0.61"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.product_files = t.read_product_files(self.productpath, "modis")
            self.product_ids = t.get_product_ids(self.product_files, "modis")
            self.all_scenes = t.check_product_files(self.product_ids)
            self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
            (self.overpopulated_scenes,
             self.complete_scenes,
             self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "modis")
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pet.indatabase)
        else:
            raise TypeError('pet must be HidroCLVariable objects')

    def __repr__(self):
        """
        Return a string representation of the object

        :return: str
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        :return: str
        """
        return f'''
Product: {self.productname}

PET records: {len(self.pet.indatabase)}.
PET database path: {self.pet.database}
        '''

    def run_extraction(self, limit=None):
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        :param limit: int (length of the scenes_to_process)
        :return: Print
        """

        with t.HiddenPrints():
            self.pet.checkdatabase()

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pet.indatabase)

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                if scene not in self.pet.indatabase:
                    e.weighted_mean_modis(scene, scenes_path,
                                          temp_dir, 'pet',
                                          self.pet.catchment_names, self.pet_log,
                                          database=self.pet.database,
                                          pcdatabase=self.pet.pcdatabase,
                                          vector_path=self.vectorpath,
                                          layer="PET_500m", )
