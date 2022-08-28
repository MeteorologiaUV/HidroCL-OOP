# coding=utf-8

from pathlib import Path
from tempfile import TemporaryDirectory
from ..variables import HidroCLVariable
from . import tools as t
from . import extractions as e


"""
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
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'ndvi',
                                  self.ndvi.catchment_names, self.ndvi_log,
                                  database=self.ndvi.database,
                                  pcdatabase=self.ndvi.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="250m 16 days NDVI", )

                if scene not in self.evi.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'evi',
                                  self.evi.catchment_names, self.evi_log,
                                  database=self.evi.database,
                                  pcdatabase=self.evi.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="250m 16 days EVI", )

                if scene not in self.evi.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'nbr',
                                  self.nbr.catchment_names, self.nbr_log,
                                  database=self.nbr.database,
                                  pcdatabase=self.nbr.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer=["250m 16 days NIR reflectance",
                                         "250m 16 days MIR reflectance"])


"""
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
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'snow',
                                  self.nsnow.catchment_names, self.snow_log,
                                  north_database=self.nsnow.database,
                                  north_pcdatabase=self.nsnow.pcdatabase,
                                  south_database=self.ssnow.database,
                                  south_pcdatabase=self.ssnow.pcdatabase,
                                  north_vector_path=self.northvectorpath,
                                  south_vector_path=self.southvectorpath,
                                  layer="Maximum_Snow_Extent")


"""
Extraction of MODIS MOD16A2 product:
"""


class Mod16a2:

    """
    A class to process MOD16A2 to hidrocl variables

    Attributes
    ----------
    pet : HidroCLVariable
        HidroCLVariable object with the potential evapotranspiration
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
            self.common_elements = self.pet.indatabase
            self.product_files = t.read_product_files(self.productpath, "modis")
            self.product_ids = t.get_product_ids(self.product_files, "modis")
            self.all_scenes = t.check_product_files(self.product_ids)
            self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
            (self.overpopulated_scenes,
             self.complete_scenes,
             self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "modis")
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)
        else:
            raise TypeError('pet must be HidroCLVariable object')

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
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'pet',
                                  self.pet.catchment_names, self.pet_log,
                                  database=self.pet.database,
                                  pcdatabase=self.pet.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="PET_500m", )


"""
Extraction of MODIS MCD15A2H product:
"""


class Mcd15a2h:
    """
    A class to process MCD15A2H to hidrocl variables

    Attributes
    ----------
    lai : HidroCLVariable
        HidroCLVariable object with the LAI data
    fpar : HidroCLVariable
        HidroCLVariable object with the FPAR data
    lai_log : str
        Path to the log file for the LAI extraction
    fpar_log : str
        Path to the log file for the FPAR extraction
    productname : str
        Name of the remote sensing product to be processed
    productpath : str
        Path to the product folder where the product files are located
    vectorpath : str
        Path to the vector folder with Shapefile with areas to be processed
    common_elements : list
        List of common elements between the FPAR and LAI databases
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

    def __init__(self, lai, fpar, product_path, vector_path,
                 lai_log, fpar_log):
        """
        Parameters
        ----------
        :param lai: HidroCLVariable
            Object with the LAI data
        :param fpar: HidroCLVariable
            Object with the FPAR data
        :param product_path: str
            Path to the product folder
        :param vector_path: str
            Path to the vector folder
        :param lai_log: str
            Path to the log file for the LAI extraction
        :param fpar_log: str
            Path to the log file for the FPAR extraction
        """
        if t.check_instance(lai, fpar):
            self.lai = lai
            self.fpar = fpar
            self.lai_log = lai_log
            self.fpar_log = fpar_log
            self.productname = "MODIS MCD15A2H Version 0.6"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = t.compare_indatabase(self.lai.indatabase,
                                                        self.fpar.indatabase)
            self.product_files = t.read_product_files(self.productpath, "modis")
            self.product_ids = t.get_product_ids(self.product_files, "modis")
            self.all_scenes = t.check_product_files(self.product_ids)
            self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
            (self.overpopulated_scenes,
             self.complete_scenes,
             self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "modis")
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)
        else:
            raise TypeError('lai and fpar must be HidroCLVariable objects')

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

LAI records: {len(self.lai.indatabase)}.
LAI database path: {self.lai.database}

FPAR records: {len(self.fpar.indatabase)}.
FPAR database path: {self.fpar.database}
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
            self.lai.checkdatabase()
            self.fpar.checkdatabase()

        self.common_elements = t.compare_indatabase(self.lai.indatabase,
                                                    self.fpar.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                if scene not in self.lai.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lai',
                                  self.lai.catchment_names, self.lai_log,
                                  database=self.lai.database,
                                  pcdatabase=self.lai.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="Lai_500m", )

                if scene not in self.fpar.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'fpar',
                                  self.fpar.catchment_names, self.fpar_log,
                                  database=self.fpar.database,
                                  pcdatabase=self.fpar.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="Fpar_500m")


"""
Extraction of GPM IMERG Late Precipitation L3 Half Hourly 0.1 degree product:
"""


class Gpm_3imrghhl:
    """
    A class to process GPM_3IMRGHHL to hidrocl variables

    Attributes
    ----------
    pp : HidroCLVariable
        HidroCLVariable object with IMERG precipitation data
    pp_log : str
        Path to the log file for IMERG precipitation data
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
        List of overpopulated scenes (more than 48 scenes for modis)
    complete_scenes : list
        List of complete scenes (48 scenes for modis)
    incomplete_scenes : list
        List of incomplete scenes (less than 48 scenes for modis)
    scenes_to_process : list
        List of scenes to process (complete scenes no processed)
    """

    def __init__(self, pp, product_path, vector_path, pp_log):
        """
        Parameters
        ----------
        :param pp: HidroCLVariable
            Object with IMERG precipitation data
        :param product_path: str
            Path to the product folder
        :param vector_path: str
            Path to the vector folder
        :param pp_log: str
            Path to the log file for IMERG precipitation extraction
        :param pp_log: str
            Path to the log file for the IMERG precipitation extraction
        """
        if t.check_instance(pp):
            self.pp = pp
            self.pp_log = pp_log
            self.productname = "GPM IMERG Late Precipitation L3 Half Hourly 0.1 degree Version 0.6"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = self.pp.indatabase
            self.product_files = t.read_product_files(self.productpath, "imerg")
            self.product_ids = t.get_product_ids(self.product_files, "imerg")
            self.all_scenes = t.check_product_files(self.product_ids)
            self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
            (self.overpopulated_scenes,
             self.complete_scenes,
             self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "imerg")
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)
        else:
            raise TypeError('pp must be HidroCLVariable objects')

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

IMERG precipitation records: {len(self.pp.indatabase)}.
IMERG precipitation database path: {self.pp.database}
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
            self.pp.checkdatabase()

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase)

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                if scene not in self.pp.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'imerg',
                                  self.pp.catchment_names, self.pp_log,
                                  database=self.pp.database,
                                  pcdatabase=self.pp.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="Grid_precipitationCal")


"""
Extraction of GLDAS_NOAH025_3H product:
"""


class Gldas_noah:
    """
    A class to process GLDAS_NOAH025_3H to hidrocl variables

    Attributes
    ----------
    snow : HidroCLVariable
        HidroCLVariable with the GLDAS snow data
    temp : HidroCLVariable
        HidroCLVariable with the GLDAS temperature data
    et : HidroCLVariable
        HidroCLVariable with the GLDAS evapotranspiration data
    soilm : HidroCLVariable
        HidroCLVariable with the GLDAS soil moisture data
    snow_log : str
        Path to the log file for the snow extraction
    temp_log : str
        Path to the log file for the temperature extraction
    et_log : str
        Path to the log file for the evapotranspiration extraction
    soilm_log : str
        Path to the log file for the soil moisture extraction
    productname : str
        Name of the remote sensing product to be processed
    productpath : str
        Path to the product folder where the product files are located
    vectorpath : str
        Path to the vector folder with Shapefile with areas to be processed
    common_elements : list
        List of common elements between the snow, temp, et and soilm databases
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

    def __init__(self, snow, temp, et, soilm, product_path,
                 vector_path, snow_log, temp_log, et_log, soilm_log):
        """
        Parameters
        ----------
        :param snow : HidroCLVariable
            Object with GLDAS snow data
        :param temp : HidroCLVariable
            Object with GLDAS temperature data
        :param et : HidroCLVariable
            Object with GLDAS evapotranspiration data
        :param soilm : HidroCLVariable
            Object with GLDAS soil moisture data
        :param product_path: str
            Path to the product folder
        :param vector_path: str
            Path to the vector folder
        :param snow_log: str
            Path to the snow log file
        :param temp_log: str
            Path to the temperature log file
        :param et_log: str
            Path to the evapotranspiration log file
        :param soilm_log: str
            Path to the soil moisture log file
        """
        if t.check_instance(snow, temp, et, soilm):
            self.snow = snow
            self.temp = temp
            self.et = et
            self.soilm = soilm
            self.snow_log = snow_log
            self.temp_log = temp_log
            self.et_log = et_log
            self.soilm_log = soilm_log
            self.productname = "GLDAS Noah Land Surface Model L4 3 hourly 0.25 degree Version 2.1"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = t.compare_indatabase(self.snow.indatabase,
                                                        self.temp.indatabase,
                                                        self.et.indatabase,
                                                        self.soilm.indatabase)
            self.product_files = t.read_product_files(self.productpath, "gldas")
            self.product_ids = t.get_product_ids(self.product_files, "gldas")
            self.all_scenes = t.check_product_files(self.product_ids)
            self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
            (self.overpopulated_scenes,
             self.complete_scenes,
             self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "gldas")
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)
        else:
            raise TypeError('snow, temp, et and soilm must be HidroCLVariable objects')

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

Snow records: {len(self.snow.indatabase)}.
Snow path: {self.snow.database}

Temperature records: {len(self.temp.indatabase)}.
Temperature path: {self.temp.database}

Evapotranspiration records: {len(self.et.indatabase)}.
Evapotranspiration path: {self.et.database}

Soil moisture records: {len(self.soilm.indatabase)}.
Soil moisture path: {self.soilm.database}
                '''

    def run_extraction(self, limit=None):
        """run extraction"""

        with t.HiddenPrints():
            self.snow.checkdatabase()
            self.temp.checkdatabase()
            self.et.checkdatabase()
            self.soilm.checkdatabase()

        self.common_elements = t.compare_indatabase(self.snow.indatabase,
                                                    self.temp.indatabase,
                                                    self.et.indatabase,
                                                    self.soilm.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                if scene not in self.snow.indatabase:
                    if scene not in self.snow.indatabase:
                        e.zonal_stats(scene, scenes_path,
                                      temp_dir, 'snow_gldas',
                                      self.snow.catchment_names, self.snow_log,
                                      database=self.snow.database,
                                      pcdatabase=self.snow.pcdatabase,
                                      vector_path=self.vectorpath,
                                      layer="SWE_inst")

                if scene not in self.temp.indatabase:
                    if scene not in self.temp.indatabase:
                        e.zonal_stats(scene, scenes_path,
                                      temp_dir, 'temp_gldas',
                                      self.temp.catchment_names, self.temp_log,
                                      database=self.temp.database,
                                      pcdatabase=self.temp.pcdatabase,
                                      vector_path=self.vectorpath,
                                      layer="Tair_f_inst")

                if scene not in self.et.indatabase:
                    if scene not in self.et.indatabase:
                        e.zonal_stats(scene, scenes_path,
                                      temp_dir, 'et_gldas',
                                      self.et.catchment_names, self.et_log,
                                      database=self.et.database,
                                      pcdatabase=self.et.pcdatabase,
                                      vector_path=self.vectorpath,
                                      layer="ECanop_tavg")

                if scene not in self.soilm.indatabase:
                    if scene not in self.soilm.indatabase:
                        e.zonal_stats(scene, scenes_path,
                                      temp_dir, 'soilm_gldas',
                                      self.soilm.catchment_names, self.soilm_log,
                                      database=self.soilm.database,
                                      pcdatabase=self.soilm.pcdatabase,
                                      vector_path=self.vectorpath,
                                      layer=["SoilMoi0_10cm_inst",
                                             "SoilMoi10_40cm_inst",
                                             "SoilMoi40_100cm_inst",
                                             "SoilMoi100_200cm_inst"])