# coding=utf-8

from pathlib import Path
from tempfile import TemporaryDirectory
from ..variables import HidroCLVariable
from . import tools as t
from . import maintainer as m
from . import extractions as e


"""
Extraction of MODIS MOD13Q1 product:
"""


class Mod13q1:
    """
    A class to process MOD13Q1 to hidrocl variables

    Attributes:
        ndvi (HidroCLVariable): HidroCLVariable object with the NDVI data \n
        evi (HidroCLVariable): HidroCLVariable object with the EVI data \n
        nbr (HidroCLVariable): HidroCLVariable object with the NBR data \n
        ndvi_log (str): Path to the log file for the NDVI extraction \n
        evi_log (str): Path to the log file for the EVI extraction \n
        nbr_log (str): Path to the log file for the NBR extraction \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): List of common elements between the NDVI, EVI and NBR databases \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 9 scenes for modis) \n
        complete_scenes (list): List of complete scenes (9 scenes for modis) \n
        incomplete_scenes (list): List of incomplete scenes (less than 9 scenes for modis) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, ndvi, evi, nbr, product_path, vector_path,
                 ndvi_log, evi_log, nbr_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl.products import Mod13q1
            >>> ndvi = HidroCLVariable('ndvi', 'ndvi.db', 'ndvi_pc.db')
            >>> evi = HidroCLVariable('evi', 'evi.db', 'evi_pc.db')
            >>> nbr = HidroCLVariable('nbr', 'nbr.db', 'nbr_pc.db')
            >>> product_path = '/home/user/mod13q1'
            >>> vector_path = '/home/user/vector.shp'
            >>> ndvi_log = '/home/user/ndvi.log'
            >>> evi_log = '/home/user/evi.log'
            >>> nbr_log = '/home/user/nbr.log'
            >>> mod13q1 = Mod13q1(ndvi, evi, nbr, product_path, vector_path,
            ...                   ndvi_log, evi_log, nbr_log)
            >>> mod13q1
            "Class to extract MODIS MOD13Q1 Version 6.1"

        Args:
            ndvi (HidroCLVariable): Object with the NDVI data
            evi (HidroCLVariable): Object with the EVI data
            nbr (HidroCLVariable): Object with the NBR data
            product_path (str): Path to the product folder
            vector_path (str): Path to the vector folder
            ndvi_log (str): Path to the log file for the NDVI extraction
            evi_log (str): Path to the log file for the EVI extraction
            nbr_log (str): Path to the log file for the NBR extraction

        Raises:
              TypeError: If the input is not a HidroCLVariable object
        """
        if t.check_instance(ndvi, evi, nbr):
            self.ndvi = ndvi
            self.evi = evi
            self.nbr = nbr
            self.ndvi_log = ndvi_log
            self.evi_log = evi_log
            self.nbr_log = nbr_log
            self.productname = "MODIS MOD13Q1 Version 6.1"
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
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
                                                            self.common_elements, what='modis')
        else:
            raise TypeError('ndvi, evi and nbr must be HidroCLVariable objects')

    def __repr__(self):
        """
        Return a string representation of the object

        Returns:
             str: String representation of the object
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        Returns:
            str: String representation of the object
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

        Args:
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
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

    def run_maintainer(self, log_file, limit=None):
        """
        Run file maintainer. It will remove any file with problems

        Args:
            log_file (str): log file path
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
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

        if limit is not None:
            scenes_to_process = self.scenes_to_process[:limit]
        else:
            scenes_to_process = self.scenes_to_process

        for scene in scenes_to_process:
            m.file_maintainer(scene=scene,
                              scenes_path=scenes_path,
                              name='modis',
                              log_file=log_file)


"""
Extraction of MODIS MOD10A2 product:
"""


class Mod10a2:
    """
    A class to process MOD10A2 to hidrocl variables

    Attributes:
        nsnow (HidroCLVariable): HidroCLVariable object with north face snow data \n
        ssnow (HidroCLVariable): HidroCLVariable object with south face snow data \n
        snow_log (str): Path to the log file for the snow extraction \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        northvectorpath (str): Path to the vector folder with the north Shapefile with areas to be processed \n
        southvectorpath (str): Path to the vector folder with the south Shapefile with areas to be processed \n
        common_elements (list): List of common elements between the nsnow and ssnow databases \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 9 scenes for modis) \n
        complete_scenes (list): List of complete scenes (9 scenes for modis) \n
        incomplete_scenes (list): List of incomplete scenes (less than 9 scenes for modis) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, nsnow, ssnow, product_path,
                 north_vector_path, south_vector_path, snow_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Mod10a2
            >>> nsnow = HidroCLVariable('nsnow', 'modis', 'mod10a2', 'north')
            >>> ssnow = HidroCLVariable('ssnow', 'modis', 'mod10a2', 'south')
            >>> product_path = '/home/user/mod10a2'
            >>> north_vector_path = '/home/user/north_vector.shp'
            >>> south_vector_path = '/home/user/south_vector.shp'
            >>> snow_log = '/home/user/snow.log'
            >>> mod10a2 = Mod10a2(nsnow, ssnow, product_path,
            ...                   north_vector_path, south_vector_path, snow_log)
            >>> mod10a2
            "Class to extract MODIS MOD10A2 Version 6.1"


        Args:
            nsnow (HidroCLVariable): HidroCLVariable object with north face snow data \n
            ssnow (HidroCLVariable): HidroCLVariable object with south face snow data \n
            product_path (str): Path to the product folder where the product files are located \n
            north_vector_path (str): Path to the vector folder with the north Shapefile with areas to be processed \n
            south_vector_path (str): Path to the vector folder with the south Shapefile with areas to be processed \n
            snow_log (str): Path to the log file for the snow extraction \n

        Raises:
              TypeError: If nsnow or ssnow is not a HidroCLVariable object \n
        """
        if t.check_instance(nsnow, ssnow):
            self.nsnow = nsnow
            self.ssnow = ssnow
            self.snow_log = snow_log
            self.productname = "MODIS MOD10A2 Version 6.1"
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
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
                                                            self.common_elements, what='modis')
        else:
            raise TypeError('nsnow and ssnow must be HidroCLVariable objects')

    def __repr__(self):
        """
        Return a string representation of the object

        Returns:
             str: String representation of the object
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        Returns:
            str: String representation of the object
        """
        return f'''
Product: {self.productname}

North face snow records: {len(self.nsnow.indatabase)}.
North face snow path: {self.nsnow.database}

South face snow records: {len(self.ssnow.indatabase)}.
South face snow database path: {self.ssnow.database}
                '''

    def run_extraction(self, limit=None):
        """Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        Args:
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

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

    def run_maintainer(self, log_file, limit=None):
        """
        Run file maintainer. It will remove any file with problems

        Args:
            log_file (str): log file path
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.nsnow.checkdatabase()
            self.ssnow.checkdatabase()

        self.common_elements = t.compare_indatabase(self.nsnow.indatabase,
                                                    self.ssnow.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        if limit is not None:
            scenes_to_process = self.scenes_to_process[:limit]
        else:
            scenes_to_process = self.scenes_to_process

        for scene in scenes_to_process:
            m.file_maintainer(scene=scene,
                              scenes_path=scenes_path,
                              name='modis',
                              log_file=log_file)


"""
Extraction of MODIS MOD16A2 product:
"""


class Mod16a2:

    """
    A class to process MOD16A2 to hidrocl variables

    Attributes:
        pet (HidroCLVariable): HidroCLVariable object with the potential evapotranspiration \n
        pet_log (str): Path to the log file for the pet extraction \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): Elements in pet database \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 9 scenes for modis) \n
        complete_scenes (list): List of complete scenes (9 scenes for modis) \n
        incomplete_scenes (list): List of incomplete scenes (less than 9 scenes for modis) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, pet, product_path, vector_path, pet_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Mod16a2
            >>> pet = HidroCLVariable('pet', 'pet.db', 'pet_pc.db')
            >>> product_path = '/home/user/modis/mod16a2'
            >>> vector_path = '/home/user/vector.shp'
            >>> pet_log = '/home/user/log/pet.log'
            >>> mod16a2 = Mod16a2(pet, product_path, vector_path, pet_log)
            >>> mod16a2
            "Class to extract MODIS MOD16A2 Version 6.1"

        Args:
            pet (HidroCLVariable): Object with the potential evapotranspiration data
            product_path (str): Path to the product folder
            vector_path (str): Path to the vector folder
            pet_log (str): Path to the log file for the pet extraction

        Raises:
            TypeError: If pet is not a HidroCLVariable object
        """
        if t.check_instance(pet):
            self.pet = pet
            self.pet_log = pet_log
            self.productname = "MODIS MOD16A2 Version 6.1"
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
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
                                                            self.common_elements, what='modis')
        else:
            raise TypeError('pet must be HidroCLVariable object')

    def __repr__(self):
        """
        Return a string representation of the object

        Returns:
             str: String representation of the object
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        Returns:
            str: String representation of the object
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

        Args:
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
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

    def run_maintainer(self, log_file, limit=None):
        """
        Run file maintainer. It will remove any file with problems

        Args:
            log_file (str): log file path
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.pet.checkdatabase()

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pet.indatabase)

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        if limit is not None:
            scenes_to_process = self.scenes_to_process[:limit]
        else:
            scenes_to_process = self.scenes_to_process

        for scene in scenes_to_process:
            m.file_maintainer(scene=scene,
                              scenes_path=scenes_path,
                              name='modis',
                              log_file=log_file)


"""
Extraction of MODIS MCD15A2H product:
"""


class Mcd15a2h:
    """
    A class to process MCD15A2H to hidrocl variables

    Attributes:
        lai (HidroCLVariable): HidroCLVariable object with the LAI data \n
        fpar (HidroCLVariable): HidroCLVariable object with the FPAR data \n
        lai_log (str): Path to the log file for the LAI extraction \n
        fpar_log (str): Path to the log file for the FPAR extraction \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): List of common elements between the FPAR and LAI databases \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 9 scenes for modis) \n
        complete_scenes (list): List of complete scenes (9 scenes for modis) \n
        incomplete_scenes (list): List of incomplete scenes (less than 9 scenes for modis) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, lai, fpar, product_path, vector_path,
                 lai_log, fpar_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Mcd15a2h
            >>> lai = HidroCLVariable('lai', 'lai.db', 'lai_pc.db')
            >>> fpar = HidroCLVariable('fpar', 'fpar.db', 'fpar_pc.db')
            >>> product_path = '/home/user/mod15a2h'
            >>> vector_path = '/home/user/vector'
            >>> lai_log = '/home/user/lai.log'
            >>> fpar_log = '/home/user/fpar.log'
            >>> mcd15a2h = Mcd15a2h(lai, fpar, product_path, vector_path,
            ...                     lai_log, fpar_log)
            >>> mcd15a2h
            "Class to extract MODIS MCD15A2H Version 6.0"

        Args:
            lai (HidroCLVariable): HidroCLVariable object with the LAI data
            fpar (HidroCLVariable): HidroCLVariable object with the FPAR data
            product_path (str): Path to the product folder
            vector_path (str): Path to the vector folder
            lai_log (str): Path to the log file for the LAI extraction
            fpar_log (str): Path to the log file for the FPAR extraction

        Raises:
            TypeError: If lai or fpar is not HidroCLVariable object
        """
        if t.check_instance(lai, fpar):
            self.lai = lai
            self.fpar = fpar
            self.lai_log = lai_log
            self.fpar_log = fpar_log
            self.productname = "MODIS MCD15A2H Version 6.0"
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
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
                                                            self.common_elements, what='modis')
        else:
            raise TypeError('lai and fpar must be HidroCLVariable objects')

    def __repr__(self):
        """
        Return a string representation of the object

        Returns:
             str: String representation of the object
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        Returns:
            str: String representation of the object
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

        Args:
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
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

    def run_maintainer(self, log_file, limit=None):
        """
        Run file maintainer. It will remove any file with problems

        Args:
            log_file (str): log file path
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.lai.checkdatabase()
            self.fpar.checkdatabase()

        self.common_elements = t.compare_indatabase(self.lai.indatabase,
                                                    self.fpar.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        if limit is not None:
            scenes_to_process = self.scenes_to_process[:limit]
        else:
            scenes_to_process = self.scenes_to_process

        for scene in scenes_to_process:
            m.file_maintainer(scene=scene,
                              scenes_path=scenes_path,
                              name='modis',
                              log_file=log_file)


"""
Extraction of GPM IMERG Late Precipitation L3 Half Hourly 0.1 degree product:
"""


class Gpm_3imrghhl:
    """
    A class to process GPM_3IMRGHHL to hidrocl variables

    Attributes:
        pp (HidroCLVariable): HidroCLVariable object with IMERG precipitation data \n
        pp_log (str): Path to the log file for IMERG precipitation data \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): common_elements (list): Elements in precipitation database \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 48 scenes for imerg) \n
        complete_scenes (list): List of complete scenes (48 scenes for imerg) \n
        incomplete_scenes (list): List of incomplete scenes (less than 48 scenes for imerg) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, pp, product_path, vector_path, pp_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Gpm_3imrghhl
            >>> pp = HidroCLVariable('pp', 'pp.db', 'pp_pc.db')
            >>> gpm = Gpm_3imrghhl(pp, product_path, vector_path, pp_log)
            >>> gpm
            "Class to extract GPM IMERG Late Precipitation L3 Half Hourly 0.1 degree Version 0.6"

        Args:
            pp (HidroCLVariable): HidroCLVariable object with IMERG precipitation data \n
            product_path (str): Path to the product folder where the product files are located \n
            vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
            pp_log (str): Path to the log file for IMERG precipitation data \n

        Raises:
            TypeError: If pp is not a HidroCLVariable object
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
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
                                                            self.common_elements, what='imerg')
        else:
            raise TypeError('pp must be HidroCLVariable objects')

    def __repr__(self):
        """
        Return a string representation of the object

        Returns:
             str: String representation of the object
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        Returns:
            str: String representation of the object
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

        Args:
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.pp.checkdatabase()

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase, "imerg")

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

    def run_maintainer(self, log_file, limit=None):
        """
        Run file maintainer. It will remove any file with problems

        Args:
            log_file (str): log file path
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.pp.checkdatabase()

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase, "imerg")

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        if limit is not None:
            scenes_to_process = self.scenes_to_process[:limit]
        else:
            scenes_to_process = self.scenes_to_process

        for scene in scenes_to_process:
            m.file_maintainer(scene=scene,
                              scenes_path=scenes_path,
                              name='imerg',
                              log_file=log_file)


"""
Extraction of GPM IMERG GIS Late Run Precipitation Half Hourly 0.1 degree product:
"""


class ImergGIS:
    """
    A class to process GPM_3IMRGHHL GIS  to hidrocl variables.

    The extracted variable is precipitatation [mm] with a scale factor of 10.

    Attributes:
        pp (HidroCLVariable): HidroCLVariable object with IMERG precipitation data \n
        pp_log (str): Path to the log file for IMERG precipitation data \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): common_elements (list): Elements in precipitation database \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 48 scenes for imerg) \n
        complete_scenes (list): List of complete scenes (48 scenes for imerg) \n
        incomplete_scenes (list): List of incomplete scenes (less than 48 scenes for imerg) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, pp, product_path, vector_path, pp_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import ImergGIS
            >>> pp = HidroCLVariable('pp', 'pp.db', 'pp_pc.db')
            >>> gpm = ImergGIS(pp, product_path, vector_path, pp_log)
            >>> gpm
            "Class to extract GPM IMERG GIS Late Run Precipitation Half Hourly 0.1 degree Version 6"

        Args:
            pp (HidroCLVariable): HidroCLVariable object with IMERG precipitation data \n
            product_path (str): Path to the product folder where the product files are located \n
            vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
            pp_log (str): Path to the log file for IMERG precipitation data \n

        Raises:
            TypeError: If pp is not a HidroCLVariable object
        """
        if t.check_instance(pp):
            self.pp = pp
            self.pp_log = pp_log
            self.productname = "GPM IMERG GIS Late Run Precipitation Half Hourly 0.1 degree Version 6"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = self.pp.indatabase
            self.product_files = t.read_product_files(self.productpath, "imgis")
            self.product_ids = t.get_product_ids(self.product_files, "imgis")
            self.all_scenes = t.check_product_files(self.product_ids)
            self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
            (self.overpopulated_scenes,
             self.complete_scenes,
             self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "imgis")
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
                                                            self.common_elements, what='imgis')
        else:
            raise TypeError('pp must be HidroCLVariable objects')

    def __repr__(self):
        """
        Return a string representation of the object

        Returns:
             str: String representation of the object
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        Returns:
            str: String representation of the object
        """
        return f'''
Product: {self.productname}

IMERG GIS precipitation records: {len(self.pp.indatabase)}.
IMERG GIS precipitation database path: {self.pp.database}
        '''

    def run_extraction(self, limit=None):
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        Args:
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.pp.checkdatabase()

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase, "imgis")

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
                                  temp_dir, 'imgis',
                                  self.pp.catchment_names, self.pp_log,
                                  database=self.pp.database,
                                  pcdatabase=self.pp.pcdatabase,
                                  vector_path=self.vectorpath)

    def run_maintainer(self, log_file, limit=None):
        """
        Run file maintainer. It will remove any file with problems

        Args:
            log_file (str): log file path
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.pp.checkdatabase()

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase, "imgis")

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        if limit is not None:
            scenes_to_process = self.scenes_to_process[:limit]
        else:
            scenes_to_process = self.scenes_to_process

        for scene in scenes_to_process:
            m.file_maintainer(scene=scene,
                              scenes_path=scenes_path,
                              name='imgis',
                              log_file=log_file)


"""
Extraction of GLDAS_NOAH025_3H product:
"""


class Gldas_noah:
    """
    A class to process GLDAS_NOAH025_3H to hidrocl variables

    Attributes:
        snow (HidroCLVariable): HidroCLVariable with the GLDAS snow data \n
        temp (HidroCLVariable): HidroCLVariable with the GLDAS temperature data \n
        et (HidroCLVariable): HidroCLVariable with the GLDAS evapotranspiration data \n
        soilm (HidroCLVariable): HidroCLVariable with the GLDAS soil moisture data \n
        snow_log (str): Path to the log file for the snow extraction \n
        temp_log (str): Path to the log file for the temperature extraction \n
        et_log (str): Path to the log file for the evapotranspiration extraction \n
        soilm_log (str): Path to the log file for the soil moisture extraction \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): List of common elements between the snow, temp, et and soilm databases \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 8 scenes for gldas) \n
        complete_scenes (list): List of complete scenes (8 scenes for gldas) \n
        incomplete_scenes (list): List of incomplete scenes (less than 8 scenes for gldas) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, snow, temp, et, soilm, product_path,
                 vector_path, snow_log, temp_log, et_log, soilm_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Gldas_noah
            >>> snow = HidroCLVariable('snow', 'snow.db', 'snow_pc.db')
            >>> temp = HidroCLVariable('temp', 'temp.db', 'temp_pc.db')
            >>> et = HidroCLVariable('et', 'et.db', 'et.db')
            >>> soilm = HidroCLVariable('soilm', 'soilm.db', 'soilm_pc.db')
            >>> product_path = '/home/user/data/GLDAS_NOAH025_3H'
            >>> vector_path = '/home/user/data/vector.shp'
            >>> snow_log = '/home/user/data/logs/snow.log'
            >>> temp_log = '/home/user/data/logs/temp.log'
            >>> et_log = '/home/user/data/logs/et.log'
            >>> soilm_log = '/home/user/data/logs/soilm.log'
            >>> gldas = Gldas_noah(snow, temp, et, soilm, product_path,
            ...                    vector_path, snow_log, temp_log, et_log, soilm_log)
            >>> gldas
            "Class to extract GLDAS Noah Land Surface Model L4 3 hourly 0.25 degree Version 2.1"

        Args:
            snow (HidroCLVariable): HidroCLVariable with the GLDAS snow data \n
            temp (HidroCLVariable): HidroCLVariable with the GLDAS temperature data \n
            et (HidroCLVariable): HidroCLVariable with the GLDAS evapotranspiration data \n
            soilm (HidroCLVariable): HidroCLVariable with the GLDAS soil moisture data \n
            product_path (str): Path to the product folder where the product files are located \n
            vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
            snow_log (str): Path to the log file for the snow extraction \n
            temp_log (str): Path to the log file for the temperature extraction \n
            et_log (str): Path to the log file for the evapotranspiration extraction \n
            soilm_log (str): Path to the log file for the soil moisture extraction \n

        Raises:
            TypeError: If snow, temp, et or soilm is not a HidroCLVariable
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
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
                                                            self.common_elements, what='gldas')
        else:
            raise TypeError('snow, temp, et and soilm must be HidroCLVariable objects')

    def __repr__(self):
        """
        Return a string representation of the object

        Returns:
             str: String representation of the object
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        Returns:
            str: String representation of the object
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
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        Args:
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.snow.checkdatabase()
            self.temp.checkdatabase()
            self.et.checkdatabase()
            self.soilm.checkdatabase()

        self.common_elements = t.compare_indatabase(self.snow.indatabase,
                                                    self.temp.indatabase,
                                                    self.et.indatabase,
                                                    self.soilm.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, "gldas")

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                if scene not in self.snow.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'snow_gldas',
                                  self.snow.catchment_names, self.snow_log,
                                  database=self.snow.database,
                                  pcdatabase=self.snow.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="SWE_inst")

                if scene not in self.temp.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'temp_gldas',
                                  self.temp.catchment_names, self.temp_log,
                                  database=self.temp.database,
                                  pcdatabase=self.temp.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="Tair_f_inst")

                if scene not in self.et.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'et_gldas',
                                  self.et.catchment_names, self.et_log,
                                  database=self.et.database,
                                  pcdatabase=self.et.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="ECanop_tavg")

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

    def run_maintainer(self, log_file, limit=None):
        """
        Run file maintainer. It will remove any file with problems

        Args:
            log_file (str): log file path
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.snow.checkdatabase()
            self.temp.checkdatabase()
            self.et.checkdatabase()
            self.soilm.checkdatabase()

        self.common_elements = t.compare_indatabase(self.snow.indatabase,
                                                    self.temp.indatabase,
                                                    self.et.indatabase,
                                                    self.soilm.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, "gldas")

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        if limit is not None:
            scenes_to_process = self.scenes_to_process[:limit]
        else:
            scenes_to_process = self.scenes_to_process

        for scene in scenes_to_process:
            m.file_maintainer(scene=scene,
                              scenes_path=scenes_path,
                              name='gldas',
                              log_file=log_file)


"""
Extraction of PERSIANN-CCS 0.04º degree product:
"""


class Persiann_ccs:
    """
    A class to process PERSIANN-CCS to hidrocl variables

    Attributes:
        pp (HidroCLVariable): HidroCLVariable object with PERSIANN-CCS precipitation data \n
        pp_log (str): Path to the log file for PERSIANN-CCS precipitation data \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): common_elements (list): Elements in precipitation database \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 1 scenes for modis) \n
        complete_scenes (list): List of complete scenes (1 scenes for modis) \n
        incomplete_scenes (list): List of incomplete scenes (less than 1 scenes for modis) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, pp, product_path, vector_path, pp_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Persiann_ccs
            >>> pp = HidroCLVariable('pp', 'pp.db', 'pp_pc.db')
            >>> product_path = '/home/user/data/PERSIANN-CCS'
            >>> vector_path = '/home/user/data/vector.shp'
            >>> pp_log = '/home/user/data/logs/pp_log.txt'
            >>> persiann_ccs = Persiann_ccs(pp, product_path, vector_path, pp_log)
            >>> persiann_ccs
            "Class to extract PERSIANN-CCS 0.04º"

        Args:
            pp (HidroCLVariable): HidroCLVariable object with PERSIANN-CCS precipitation data \n
            product_path (str): Path to the product folder where the product files are located \n
            vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
            pp_log (str): Path to the log file for PERSIANN-CCS precipitation data \n

        Raises:
            TypeError: If pp is not a HidroCLVariable object
        """
        if t.check_instance(pp):
            self.pp = pp
            self.pp_log = pp_log
            self.productname = "PERSIANN-CCS 0.04º"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = self.pp.indatabase
            self.product_files = t.read_product_files(self.productpath, "persiann_ccs")
            self.product_ids = t.get_product_ids(self.product_files, "persiann_ccs")
            self.all_scenes = t.check_product_files(self.product_ids)
            self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
            (self.overpopulated_scenes,
             self.complete_scenes,
             self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "persiann_ccs")
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
                                                            self.common_elements, what='persiann_ccs')
        else:
            raise TypeError('pp must be HidroCLVariable object')

    def __repr__(self):
        """
        Return a string representation of the object

        Returns:
             str: String representation of the object
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        Returns:
            str: String representation of the object
        """
        return f'''
Product: {self.productname}

PERSIANN-CCS precipitation records: {len(self.pp.indatabase)}.
PERSIANN-CCS precipitation database path: {self.pp.database}
        '''

    def run_extraction(self, limit=None):
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        Args:
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.pp.checkdatabase()

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase, "persiann_ccs")

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
                                  temp_dir, "persiann_ccs",
                                  self.pp.catchment_names, self.pp_log,
                                  database=self.pp.database,
                                  pcdatabase=self.pp.pcdatabase,
                                  vector_path=self.vectorpath)

    def run_maintainer(self, log_file, limit=None):
        """
        Run file maintainer. It will remove any file with problems

        Args:
            log_file (str): log file path
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.pp.checkdatabase()

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase, "persiann_ccs")

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        if limit is not None:
            scenes_to_process = self.scenes_to_process[:limit]
        else:
            scenes_to_process = self.scenes_to_process

        for scene in scenes_to_process:
            m.file_maintainer(scene=scene,
                              scenes_path=scenes_path,
                              name='persiann',
                              log_file=log_file)


"""
Extraction of PERSIANN-CCS-CDR 0.04º degree product:
"""


class Persiann_ccs_cdr:
    """
    A class to process PERSIANN-CCS-CDR to hidrocl variables

    Attributes:
        pp (HidroCLVariable): HidroCLVariable object with PERSIANN-CCS-CDR precipitation data \n
        pp_log (str): Path to the log file for PERSIANN-CCS-CDR precipitation data \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): common_elements (list): Elements in precipitation database \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 1 scenes for modis) \n
        complete_scenes (list): List of complete scenes (1 scenes for modis) \n
        incomplete_scenes (list): List of incomplete scenes (less than 1 scenes for modis) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, pp, product_path, vector_path, pp_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Persiann_ccs_cdr
            >>> pp = HidroCLVariable('pp', 'pp.db', 'pp_pc.db')
            >>> product_path = '/home/user/data/PERSIANN-CCS-CDR'
            >>> vector_path = '/home/user/data/vector.shp'
            >>> pp_log = '/home/user/data/logs/pp_log.txt'
            >>> persiann_ccs_cdr = Persiann_ccs_cdr(pp, product_path, vector_path, pp_log)
            >>> persiann_ccs_cdr
            "Class to extract PERSIANN-CCS-CDR 0.04º"

        Args:
            pp (HidroCLVariable): HidroCLVariable object with PERSIANN-CCS-CDR precipitation data \n
            product_path (str): Path to the product folder where the product files are located \n
            vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
            pp_log (str): Path to the log file for PERSIANN-CCS-CDR precipitation data \n

        Raises:
            TypeError: If pp is not a HidroCLVariable object
        """
        if t.check_instance(pp):
            self.pp = pp
            self.pp_log = pp_log
            self.productname = "PERSIANN-CCS-CDR 0.04º"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = self.pp.indatabase
            self.product_files = t.read_product_files(self.productpath, "persiann_ccs_cdr")
            self.product_ids = t.get_product_ids(self.product_files, "persiann_ccs_cdr")
            self.all_scenes = t.check_product_files(self.product_ids)
            self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
            (self.overpopulated_scenes,
             self.complete_scenes,
             self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "persiann_ccs_cdr")
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
                                                            self.common_elements, what='persiann_ccs_cdr')
        else:
            raise TypeError('pp must be HidroCLVariable object')

    def __repr__(self):
        """
        Return a string representation of the object

        Returns:
             str: String representation of the object
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        Returns:
            str: String representation of the object
        """
        return f'''
Product: {self.productname}

PERSIANN-CCS-CDR precipitation records: {len(self.pp.indatabase)}.
PERSIANN-CCS-CDR precipitation database path: {self.pp.database}
        '''

    def run_extraction(self, limit=None):
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        Args:
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.pp.checkdatabase()

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase, 'persiann_ccs_cdr')

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
                                  temp_dir, "persiann_ccs_cdr",
                                  self.pp.catchment_names, self.pp_log,
                                  database=self.pp.database,
                                  pcdatabase=self.pp.pcdatabase,
                                  vector_path=self.vectorpath)

    def run_maintainer(self, log_file, limit=None):
        """
        Run file maintainer. It will remove any file with problems

        Args:
            log_file (str): log file path
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.pp.checkdatabase()

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase, 'persiann_ccs_cdr')

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        if limit is not None:
            scenes_to_process = self.scenes_to_process[:limit]
        else:
            scenes_to_process = self.scenes_to_process

        for scene in scenes_to_process:
            m.file_maintainer(scene=scene,
                              scenes_path=scenes_path,
                              name='persiann',
                              log_file=log_file)


"""
Extraction of PDIR-NOW 0.04º degree product:
"""

class Pdirnow:
    """
    A class to process PDIR-Now to hidrocl variables

    Attributes:
        pp (HidroCLVariable): HidroCLVariable object with PDIR-Now precipitation data \n
        pp_log (str): Path to the log file for PDIR-Now precipitation data \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): common_elements (list): Elements in precipitation database \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 1 scenes for modis) \n
        complete_scenes (list): List of complete scenes (1 scenes for modis) \n
        incomplete_scenes (list): List of incomplete scenes (less than 1 scenes for modis) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, pp, product_path, vector_path, pp_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Pdirnow
            >>> pp = HidroCLVariable('pp', 'pp.db', 'pp_pc.db')
            >>> product_path = '/home/user/data/PDIR-Now'
            >>> vector_path = '/home/user/data/vector.shp'
            >>> pp_log = '/home/user/data/logs/pp_log.txt'
            >>> pdirnow = Pdirnow(pp, product_path, vector_path, pp_log)
            >>> pdirnow
            "Class to extract PDIR-Now 0.04º"

        Args:
            pp (HidroCLVariable): HidroCLVariable object with PDIR-Now precipitation data \n
            product_path (str): Path to the product folder where the product files are located \n
            vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
            pp_log (str): Path to the log file for PDIR-Now precipitation data \n

        Raises:
            TypeError: If pp is not a HidroCLVariable object
        """
        if t.check_instance(pp):
            self.pp = pp
            self.pp_log = pp_log
            self.productname = "PDIR-Now 0.04º"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = self.pp.indatabase
            self.product_files = t.read_product_files(self.productpath, 'pdirnow')
            self.product_ids = t.get_product_ids(self.product_files, 'pdirnow')
            self.all_scenes = t.check_product_files(self.product_ids)
            self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
            (self.overpopulated_scenes,
             self.complete_scenes,
             self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, 'pdirnow')
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
                                                            self.common_elements, what='pdirnow')
        else:
            raise TypeError('pp must be HidroCLVariable object')

    def __repr__(self):
        """
        Return a string representation of the object

        Returns:
             str: String representation of the object
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        Returns:
            str: String representation of the object
        """
        return f'''
Product: {self.productname}

PDIR-Now precipitation records: {len(self.pp.indatabase)}.
PDIR-Now precipitation database path: {self.pp.database}
        '''

    def run_extraction(self, limit=None):
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        Args:
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.pp.checkdatabase()

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase, 'pdirnow')

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
                                  temp_dir, "pdirnow",
                                  self.pp.catchment_names, self.pp_log,
                                  database=self.pp.database,
                                  pcdatabase=self.pp.pcdatabase,
                                  vector_path=self.vectorpath)

    def run_maintainer(self, log_file, limit=None):
        """
        Run file maintainer. It will remove any file with problems

        Args:
            log_file (str): log file path
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.pp.checkdatabase()

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase, 'pdirnow')

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        if limit is not None:
            scenes_to_process = self.scenes_to_process[:limit]
        else:
            scenes_to_process = self.scenes_to_process

        for scene in scenes_to_process:
            m.file_maintainer(scene=scene,
                              scenes_path=scenes_path,
                              name='persiann',
                              log_file=log_file)


"""
Extraction of ERA5-Land hourly data product:
"""


class Era5_land:
    """
    A class to process ERA5-Land hourly to hidrocl variables. Where:

    temperature: t2m -> temp (10 * ºC) mean \n
    potential evapotranspiration: pev -> pet (10000 * m) sum \n
    snow albedo: asn -> snwa (10 * frac) mean \n
    snow cover: snowc -> snw (10 * frac) mean \n
    snow density: rsn -> snwdn (10 * kg/m3) mean \n
    snow depth: sd -> snwdt (10 * m) mean \n
    evapotranspiration: e -> et (10000 * m) sum \n
    total precipitation: tp -> pp (10000 * m) sum \n
    volumetric soil water: swvl1+swvl2+swvl3+swvl4 -> soilm (1000 * m3/m3) mean \n

    temp, pp, et, pet, snow, snowa, snowdn, snowdt, soilm \n

    Attributes:
        temp (HidroCLVariable): HidroCLVariable object with ERA5 temperature data \n
        pp (HidroCLVariable): HidroCLVariable object with ERA5 precipitation data \n
        et (HidroCLVariable): HidroCLVariable object with ERA5 evapotranspiration data \n
        pet (HidroCLVariable): HidroCLVariable object with ERA5 potential evapotranspiration data \n
        snw (HidroCLVariable): HidroCLVariable object with ERA5 snow cover data \n
        snwa (HidroCLVariable): HidroCLVariable object with ERA5 snow albedo data \n
        snwdn (HidroCLVariable): HidroCLVariable object with ERA5 snow density data \n
        snwdt (HidroCLVariable): HidroCLVariable object with ERA5 snow depth data \n
        soilm (HidroCLVariable): HidroCLVariable object with ERA5 volumetric soil water data \n
        temp_log (str): Log file path for temperature data \n
        pp_log (str): Log file path for precipitation data \n
        et_log (str): Log file path for evapotranspiration data \n
        pet_log (str): Log file path for potential evapotranspiration data \n
        snw_log (str): Log file path for snow cover data \n
        snwa_log (str): Log file path for snow albedo data \n
        snwdn_log (str): Log file path for snow density data \n
        snwdt_log (str): Log file path for snow depth data \n
        soilm_log (str): Log file path for volumetric soil water data \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): List of common elements between the snow, temp, et and soilm databases \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 1 scenes for era5) \n
        complete_scenes (list): List of complete scenes (1 scenes for era5) \n
        incomplete_scenes (list): List of incomplete scenes (less than 1 scenes for era5) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, temp, pp, et, pet, snw, snwa, snwdn, snwdt,
                 soilm, product_path, vector_path, temp_log,
                 pp_log, et_log, pet_log, snw_log, snwa_log, snwdn_log,
                 snwdt_log, soilm_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Era5_land
            >>> temp = HidroCLVariable('temp',temp.db, temppc.db)
            >>> pp = HidroCLVariable('pp', pp.db, pppc.db)
            >>> et = HidroCLVariable('et', et.db, etpc.db)
            >>> pet = HidroCLVariable('pet', pet.db, petpc.db)
            >>> snw = HidroCLVariable('snw', snw.db, snwpc.db)
            >>> snwa = HidroCLVariable('snwa', snwa.db, snwapc.db)
            >>> snwdn = HidroCLVariable('snwdn', snwdn.db, snwdnpc.db)
            >>> snwdt = HidroCLVariable('snwdt', snwdt.db, snwdtpc.db)
            >>> soilm = HidroCLVariable('soilm', soilm.db, soilmdb.db)
            >>> product_path = '/home/user/era5-land'
            >>> vector_path = '/home/user/shapefiles'
            >>> temp_log = '/home/user/temp.log'
            >>> pp_log = '/home/user/pp.log'
            >>> et_log = '/home/user/et.log'
            >>> pet_log = '/home/user/pet.log'
            >>> snw_log = '/home/user/snw.log'
            >>> snwa_log = '/home/user/snwa.log'
            >>> snwdn_log = '/home/user/snwdn.log'
            >>> snwdt_log = '/home/user/snwdt.log'
            >>> soilm_log = '/home/user/soilm.log'
            >>> era5 = Era5_land(temp, pp, et, pet, snw, snwa, snwdn, snwdt,
                    soilm, product_path, vector_path, temp_log,
                    pp_log, et_log, pet_log, snw_log, snwa_log, snwdn_log,
                    snwdt_log, soilm_log)
            >>> era5
            "Class to extract ERA5-Land Hourly 0.1 degree"
            >>> era5.run_extraction()


        Args:
            temp (HidroCLVariable): HidroCLVariable object with ERA5 temperature data \n
            pp (HidroCLVariable): HidroCLVariable object with ERA5 precipitation data \n
            et (HidroCLVariable): HidroCLVariable object with ERA5 evapotranspiration data \n
            pet (HidroCLVariable): HidroCLVariable object with ERA5 potential evapotranspiration data \n
            snw (HidroCLVariable): HidroCLVariable object with ERA5 snow cover data \n
            snwa (HidroCLVariable): HidroCLVariable object with ERA5 snow albedo data \n
            snwdn (HidroCLVariable): HidroCLVariable object with ERA5 snow density data \n
            snwdt (HidroCLVariable): HidroCLVariable object with ERA5 snow depth data \n
            soilm (HidroCLVariable): HidroCLVariable object with ERA5 volumetric soil water data \n
            product_path (str): Path to the product folder where the product files are located \n
            vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
            temp_log (str): Log file path for temperature data \n
            pp_log (str): Log file path for precipitation data \n
            et_log (str): Log file path for evapotranspiration data \n
            pet_log (str): Log file path for potential evapotranspiration data \n
            snw_log (str): Log file path for snow cover data \n
            snwa_log (str): Log file path for snow albedo data \n
            snwdn_log (str): Log file path for snow density data \n
            snwdt_log (str): Log file path for snow depth data \n
            soilm_log (str): Log file path for volumetric soil water data \n

        Raises:
            TypeError: If temp, pp, et, pet, snow, snowa, snowdn, snowdt or soilm is not HidroCLVariable objects \n
        """
        if t.check_instance(temp, pp, et, pet, snw, snwa, snwdn, snwdt, soilm):
            self.temp = temp
            self.pp = pp
            self.et = et
            self.pet = pet
            self.snw = snw
            self.snwa = snwa
            self.snwdn = snwdn
            self.snwdt = snwdt
            self.soilm = soilm
            self.temp_log = temp_log
            self.pp_log = pp_log
            self.et_log = et_log
            self.pet_log = pet_log
            self.snw_log = snw_log
            self.snwa_log = snwa_log
            self.snwdn_log = snwdn_log
            self.snwdt_log = snwdt_log
            self.soilm_log = soilm_log
            self.productname = "ERA5-Land Hourly 0.1 degree"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = t.compare_indatabase(self.temp.indatabase,
                                                        self.pp.indatabase,
                                                        self.et.indatabase,
                                                        self.pet.indatabase,
                                                        self.snw.indatabase,
                                                        self.snwa.indatabase,
                                                        self.snwdn.indatabase,
                                                        self.snwdt.indatabase,
                                                        self.soilm.indatabase)
            self.product_files = t.read_product_files(self.productpath, "era5")
            self.product_ids = t.get_product_ids(self.product_files, "era5")
            self.all_scenes = t.check_product_files(self.product_ids)
            self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
            (self.overpopulated_scenes,
             self.complete_scenes,
             self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "era5")
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
                                                            self.common_elements, what="era5")
        else:
            raise TypeError('temp, pp, et, pet, snw, snwa, snwdn, snwdt and soilm must be HidroCLVariable objects')

    def __repr__(self):
        """
        Return a string representation of the object

        Returns:
             str: String representation of the object
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        Returns:
            str: String representation of the object
        """
        return f'''
Product: {self.productname}

Temperature records: {len(self.temp.indatabase)}.
Temperature path: {self.temp.database}

Precipitation records: {len(self.pp.indatabase)}.
Precipitation path: {self.pp.database}

Evapotranspiration records: {len(self.et.indatabase)}.
Evapotranspiration path: {self.et.database}

Potential evapotranspiration records: {len(self.pet.indatabase)}.
Potential evapotranspiration path: {self.pet.database}

Snow cover records: {len(self.snw.indatabase)}.
Snow cover path: {self.snw.database}

Snow albedo records: {len(self.snwa.indatabase)}.
Snow albedo path: {self.snwa.database}

Snow density records: {len(self.snwdn.indatabase)}.
Snow density path: {self.snwdn.database}

Snow depth records: {len(self.snwdt.indatabase)}.
Snow depth path: {self.snwdt.database}

Volumetric soil water records: {len(self.soilm.indatabase)}.
Volumetric soil water path: {self.soilm.database}
                '''

    def run_extraction(self, limit=None):
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        Args:
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.temp.checkdatabase()
            self.pp.checkdatabase()
            self.et.checkdatabase()
            self.pet.checkdatabase()
            self.snw.checkdatabase()
            self.snwa.checkdatabase()
            self.snwdn.checkdatabase()
            self.snwdt.checkdatabase()
            self.soilm.checkdatabase()

        self.common_elements = t.compare_indatabase(self.temp.indatabase,
                                                    self.pp.indatabase,
                                                    self.et.indatabase,
                                                    self.pet.indatabase,
                                                    self.snw.indatabase,
                                                    self.snwa.indatabase,
                                                    self.snwdn.indatabase,
                                                    self.snwdt.indatabase,
                                                    self.soilm.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, "era5")

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                if scene not in self.temp.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'temp_era5',
                                  self.temp.catchment_names, self.temp_log,
                                  database=self.temp.database,
                                  pcdatabase=self.temp.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="t2m")

                if scene not in self.pp.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'pp_era5',
                                  self.pp.catchment_names, self.pp_log,
                                  database=self.pp.database,
                                  pcdatabase=self.pp.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="tp")

                if scene not in self.et.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'et_era5',
                                  self.et.catchment_names, self.et_log,
                                  database=self.et.database,
                                  pcdatabase=self.et.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="e")

                if scene not in self.pet.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'pet_era5',
                                  self.pet.catchment_names, self.pet_log,
                                  database=self.pet.database,
                                  pcdatabase=self.pet.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="pev")

                if scene not in self.snw.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'snw_era5',
                                  self.snw.catchment_names, self.snw_log,
                                  database=self.snw.database,
                                  pcdatabase=self.snw.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="snowc")

                if scene not in self.snwa.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'snwa_era5',
                                  self.snwa.catchment_names, self.snwa_log,
                                  database=self.snwa.database,
                                  pcdatabase=self.snwa.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="asn")

                if scene not in self.snwdn.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'snwdn_era5',
                                  self.snwdn.catchment_names, self.snwdn_log,
                                  database=self.snwdn.database,
                                  pcdatabase=self.snwdn.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="rsn")

                if scene not in self.snwdt.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'snwdt_era5',
                                  self.snwdt.catchment_names, self.snwdt_log,
                                  database=self.snwdt.database,
                                  pcdatabase=self.snwdt.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="sd")

                if scene not in self.soilm.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'soilm_era5',
                                  self.soilm.catchment_names, self.soilm_log,
                                  database=self.soilm.database,
                                  pcdatabase=self.soilm.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer=["swvl1", "swvl2", "swvl3", "swvl4"])

    def run_maintainer(self, log_file, limit=None):
        """
        Run file maintainer. It will remove any file with problems

        Args:
            log_file (str): log file path
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.temp.checkdatabase()
            self.pp.checkdatabase()
            self.et.checkdatabase()
            self.pet.checkdatabase()
            self.snw.checkdatabase()
            self.snwa.checkdatabase()
            self.snwdn.checkdatabase()
            self.snwdt.checkdatabase()
            self.soilm.checkdatabase()

        self.common_elements = t.compare_indatabase(self.temp.indatabase,
                                                    self.pp.indatabase,
                                                    self.et.indatabase,
                                                    self.pet.indatabase,
                                                    self.snw.indatabase,
                                                    self.snwa.indatabase,
                                                    self.snwdn.indatabase,
                                                    self.snwdt.indatabase,
                                                    self.soilm.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, "era5")

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        if limit is not None:
            scenes_to_process = self.scenes_to_process[:limit]
        else:
            scenes_to_process = self.scenes_to_process

        for scene in scenes_to_process:
            m.file_maintainer(scene=scene,
                              scenes_path=scenes_path,
                              name='era5',
                              log_file=log_file)


"""
Extraction of GFS data product:
"""


class Gfs:
    """
    A class to process GFS to hidrocl variables. The used variables are:
    - gh: Geopotential height
    - prate: Precipitation rate
    - r2: 2m relative humidity
    - t2m: 2m temperature
    - u10: 10m U wind component
    - v10: 10m V wind component

    Attributes:
        db0 (HidroCLVariable): HidroCLVariable object with GFS variable (see avobe) of day 0 \n
        db1 (HidroCLVariable): HidroCLVariable object with GFS variable (see avobe) of day 1 \n
        db2 (HidroCLVariable): HidroCLVariable object with GFS variable (see avobe) of day 2 \n
        db3 (HidroCLVariable): HidroCLVariable object with GFS variable (see avobe) of day 3 \n
        db4 (HidroCLVariable): HidroCLVariable object with GFS variable (see avobe) of day 4 \n
        db_log (str): Log file path for temperature data \n
        valid_time (int): Valid time for extracting the product \n
        variable (str): Variable name \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 1 scenes for era5) \n
        complete_scenes (list): List of complete scenes (1 scenes for era5) \n
        incomplete_scenes (list): List of incomplete scenes (less than 1 scenes for era5) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, db0, db1, db2, db3, db4,
                 db_log, variable, aggregation,
                 product_path, vectorpath):
        """
        Examples:

        Args:
            db (HidroCLVariable): HidroCLVariable object with GFS variable (see avobe) \n
            db_log (str): Log file path for extracted data \n
            valid_time (int): Valid time for extracting the product \n
            variable (str): Variable name \n
            product_path (str): Path to the product folder where the product files are located \n
            vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n

        Raises:
            TypeError: If db is not HidroCLVariable objects \n
        """
        if t.check_instance(db0, db1, db2, db3, db4):
            self.db0 = db0
            self.db1 = db1
            self.db2 = db2
            self.db3 = db3
            self.db4 = db4
            self.db_log = db_log
            self.variable = variable
            self.aggregation = aggregation
            self.productname = "GFS 0.5º"
            self.productpath = product_path
            self.vectorpath = vectorpath
            self.common_elements = t.compare_indatabase(self.db0.indatabase, self.db1.indatabase,
                                                        self.db2.indatabase, self.db3.indatabase, self.db4.indatabase)
            self.product_files = t.read_product_files(self.productpath, "gfs", variable=self.variable)
            self.product_ids = t.get_product_ids(self.product_files, "gfs")

            self.all_scenes = t.check_product_files(self.product_ids)

            self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
            (self.overpopulated_scenes,
             self.complete_scenes,
             self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "gfs")
            self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
                                                            self.common_elements, what="gfs")
        else:
            raise TypeError('db0, db1, db2, db3, db4 must be HidroCLVariable objects')

    def __repr__(self):
        """
        Return a string representation of the object

        Returns:
             str: String representation of the object
        """
        return f'Class to extract {self.productname}'

    def __str__(self):
        """
        Return a string representation of the object

        Returns:
            str: String representation of the object
        """
        return f'''
Product: {self.productname}

Database records day0: {len(self.db0.indatabase)}.
Database path day 0: {self.db0.database}

Database records day1: {len(self.db1.indatabase)}.
Database path day 1: {self.db1.database}

Database records day2: {len(self.db2.indatabase)}.
Database path day 2: {self.db2.database}

Database records day3: {len(self.db3.indatabase)}.
Database path day 3: {self.db3.database}

Database records day4: {len(self.db4.indatabase)}.
Database path day 4: {self.db4.database}
                '''

    def run_extraction(self, limit=None):
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        Args:
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.db0.checkdatabase()
            self.db1.checkdatabase()
            self.db2.checkdatabase()
            self.db3.checkdatabase()
            self.db4.checkdatabase()

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, what="gfs")

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                days = []
                if scene not in self.db0.indatabase:
                    days.append(0)
                if scene not in self.db1.indatabase:
                    days.append(1)
                if scene not in self.db2.indatabase:
                    days.append(2)
                if scene not in self.db3.indatabase:
                    days.append(3)
                if scene not in self.db4.indatabase:
                    days.append(4)

                e.zonal_stats(scene, scenes_path,
                              temp_dir, 'gfs',
                              self.db0.catchment_names, self.db_log,
                              database=None,
                              databases=[self.db0.database,
                                         self.db1.database,
                                         self.db2.database,
                                         self.db3.database,
                                         self.db4.database],
                              pcdatabase=None,
                              pcdatabases=[self.db0.pcdatabase,
                                           self.db1.pcdatabase,
                                           self.db2.pcdatabase,
                                           self.db3.pcdatabase,
                                           self.db4.pcdatabase],
                              vector_path=self.vectorpath,
                              layer=self.variable,
                              aggregation=self.aggregation,
                              days=days)


    def run_maintainer(self, log_file, limit=None):
        """
        Run file maintainer. It will remove any file with problems

        Args:
            log_file (str): log file path
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.temp.checkdatabase()
            self.pp.checkdatabase()
            self.et.checkdatabase()
            self.pet.checkdatabase()
            self.snw.checkdatabase()
            self.snwa.checkdatabase()
            self.snwdn.checkdatabase()
            self.snwdt.checkdatabase()
            self.soilm.checkdatabase()

        self.common_elements = t.compare_indatabase(self.temp.indatabase,
                                                    self.pp.indatabase,
                                                    self.et.indatabase,
                                                    self.pet.indatabase,
                                                    self.snw.indatabase,
                                                    self.snwa.indatabase,
                                                    self.snwdn.indatabase,
                                                    self.snwdt.indatabase,
                                                    self.soilm.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, "era5")

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        if limit is not None:
            scenes_to_process = self.scenes_to_process[:limit]
        else:
            scenes_to_process = self.scenes_to_process

        for scene in scenes_to_process:
            m.file_maintainer(scene=scene,
                              scenes_path=scenes_path,
                              name='era5',
                              log_file=log_file)
