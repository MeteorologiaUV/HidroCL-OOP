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
Extraction Agr. NDVI from MODIS MOD13Q1 product:
"""


class Mod13q1agr:
    """
    A class to process MOD13Q1 to hidrocl variables

    Attributes:
        ndvi (HidroCLVariable): HidroCLVariable object with the NDVI data \n
        ndvi_log (str): Path to the log file for the NDVI extraction \n
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

    def __init__(self, ndvi, product_path, vector_path, ndvi_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl.products import Mod13q1agr
            >>> ndvi = HidroCLVariable('ndvi', 'ndvi.db', 'ndvi_pc.db')
            >>> product_path = '/home/user/mod13q1'
            >>> vector_path = '/home/user/vector.shp'
            >>> ndvi_log = '/home/user/ndvi.log'
            >>> mod13q1agr = Mod13q1agr(ndvi, product_path, vector_path, ndvi_log)
            >>> mod13q1agr
            "Class to extract agricultural NDVI from MODIS MOD13Q1 Version 6.1"

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
        if t.check_instance(ndvi):
            self.ndvi = ndvi
            self.ndvi_log = ndvi_log
            self.productname = "agricultural NDVI from MODIS MOD13Q1 Version 6.1"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = t.compare_indatabase(self.ndvi.indatabase)
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

        self.common_elements = t.compare_indatabase(self.ndvi.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                e.zonal_stats(scene, scenes_path,
                              temp_dir, 'ndvi',
                              self.ndvi.catchment_names, self.ndvi_log,
                              database=self.ndvi.database,
                              pcdatabase=self.ndvi.pcdatabase,
                              vector_path=self.vectorpath,
                              layer="250m 16 days NDVI", )

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

        self.common_elements = t.compare_indatabase(self.ndvi.indatabase)

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
        et (HidroCLVariable): HidroCLVariable object with the actual evapotranspiration \n
        pet_log (str): Path to the log file for the pet extraction \n
        et_log (str): Path to the log file for the et extraction \n
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

    def __init__(self, pet, et, product_path, vector_path, pet_log, et_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Mod16a2
            >>> pet = HidroCLVariable('pet', 'pet.db', 'pet_pc.db')
            >>> et = HidroCLVariable('et', 'et.db', 'et_pc.db')
            >>> product_path = '/home/user/modis/mod16a2'
            >>> vector_path = '/home/user/vector.shp'
            >>> pet_log = '/home/user/log/pet.log'
            >>> et_log = '/home/user/log/et.log'
            >>> mod16a2 = Mod16a2(pet, et, product_path, vector_path, pet_log, et_log)
            >>> mod16a2
            "Class to extract MODIS MOD16A2 Version 6.1"

        Args:
            pet (HidroCLVariable): Object with the potential evapotranspiration data
            et (HidroCLVariable): Object with the actual evapotranspiration data
            product_path (str): Path to the product folder
            vector_path (str): Path to the vector folder
            pet_log (str): Path to the log file for the pet extraction
            et_log (str): Path to the log file for the et extraction

        Raises:
            TypeError: If pet is not a HidroCLVariable object
        """
        if t.check_instance(pet):
            self.pet = pet
            self.et = et
            self.pet_log = pet_log
            self.et_log = et_log
            self.productname = "MODIS MOD16A2 Version 6.1"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = t.compare_indatabase(self.pet.indatabase,
                                                        self.et.indatabase)
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

ET records: {len(self.et.indatabase)}.
ET database path: {self.et.database}
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
            self.et.checkdatabase()

        self.common_elements = t.compare_indatabase(self.pet.indatabase,
                                                    self.et.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)

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

                if scene not in self.pet.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'et',
                                  self.et.catchment_names, self.et_log,
                                  database=self.et.database,
                                  pcdatabase=self.et.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="ET_500m", )

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
Extraction of MODIS MOD12Q1 product:
"""


class Mod12q1:
    """
    A class to process MOD12AQ1 to hidrocl variables

    The MOD12Q1 product has the following land cover classes:
    - barren (brn): value 16
    - cropland (crp): value 12
    - closed shrubland (csh): value 6
    - cropland/natural vegetation mosaic (cvm): value 14
    - deciduous broadleaf forest (dbf): value 4
    - deciduous needleleaf forest (dnf): value 3
    - evergreen broadleaf forest (ebf): value 2
    - evergreen needleleaf forest (enf): value 1
    - grassland (grs): value 10
    - mixed forest (mxf): value 5
    - open shrubland (osh): value 7
    - permanent wetland (pwt): value 11
    - snow and ice (snw): value 15
    - savannas (svn): value 9
    - urban and built-up (urb): value 13
    - water bodies (wat): value 17
    - woody savannas (wsv): value 8


    Attributes:
        brn (HidroCLVariable): HidroCLVariable object with barren data \n
        crp (HidroCLVariable): HidroCLVariable object with cropland data \n
        csh (HidroCLVariable): HidroCLVariable object with closed shrubland data \n
        cvm (HidroCLVariable): HidroCLVariable object with cropland/natural vegetation mosaic data \n
        dbf (HidroCLVariable): HidroCLVariable object with deciduous broadleaf forest data \n
        dnf (HidroCLVariable): HidroCLVariable object with deciduous needleleaf forest data \n
        ebf (HidroCLVariable): HidroCLVariable object with evergreen broadleaf forest data \n
        enf (HidroCLVariable): HidroCLVariable object with evergreen needleleaf forest data \n
        grs (HidroCLVariable): HidroCLVariable object with grassland data \n
        mxf (HidroCLVariable): HidroCLVariable object with mixed forest data \n
        osh (HidroCLVariable): HidroCLVariable object with open shrubland data \n
        pwt (HidroCLVariable): HidroCLVariable object with permanent wetland data \n
        snw (HidroCLVariable): HidroCLVariable object with snow and ice data \n
        svn (HidroCLVariable): HidroCLVariable object with savannas data \n
        urb (HidroCLVariable): HidroCLVariable object with urban and built-up data \n
        wat (HidroCLVariable): HidroCLVariable object with water bodies data \n
        wsv (HidroCLVariable): HidroCLVariable object with woody savannas data \n
        var_log (str): Path to the log file for the variable extraction \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        agg (str): Aggregation method to be used \n
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

    def __init__(self, brn, crp, csh, cvm, dbf, dnf, ebf, enf, grs, mxf,
                 osh, pwt, snw, svn, urb, wat, wsv, product_path, vector_path, var_log, agg):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Mod12q1
            >>> brn = HidroCLVariable('brn', 'modis', 'mod12q1', 'barren')
            >>> crp = HidroCLVariable('crp', 'modis', 'mod12q1', 'cropland')
            >>> csh = HidroCLVariable('csh', 'modis', 'mod12q1', 'closed shrubland')
            >>> cvm = HidroCLVariable('cvm', 'modis', 'mod12q1', 'cropland/natural vegetation mosaic')
            >>> dbf = HidroCLVariable('dbf', 'modis', 'mod12q1', 'deciduous broadleaf forest')
            >>> dnf = HidroCLVariable('dnf', 'modis', 'mod12q1', 'deciduous needleleaf forest')
            >>> ebf = HidroCLVariable('ebf', 'modis', 'mod12q1', 'evergreen broadleaf forest')
            >>> enf = HidroCLVariable('enf', 'modis', 'mod12q1', 'evergreen needleleaf forest')
            >>> grs = HidroCLVariable('grs', 'modis', 'mod12q1', 'grassland')
            >>> mxf = HidroCLVariable('mxf', 'modis', 'mod12q1', 'mixed forest')
            >>> osh = HidroCLVariable('osh', 'modis', 'mod12q1', 'open shrubland')
            >>> pwt = HidroCLVariable('pwt', 'modis', 'mod12q1', 'permanent wetland')
            >>> snw = HidroCLVariable('snw', 'modis', 'mod12q1', 'snow')
            >>> svn = HidroCLVariable('svn', 'modis', 'mod12q1', 'savannas')
            >>> urb = HidroCLVariable('urb', 'modis', 'mod12q1', 'urban and built-up')
            >>> wat = HidroCLVariable('wat', 'modis', 'mod12q1', 'water bodies')
            >>> wsv = HidroCLVariable('wsv', 'modis', 'mod12q1', 'woody savannas')
            >>> product_path = '/home/user/mod12q1'
            >>> vector_path = '/home/user/vector.shp'
            >>> var_log = '/home/user/var.log'
            >>> mod12q1 = Mod12q1(brn, crp, csh, cvm, dbf, dnf, ebf, enf, grs, mxf,
            ...                   osh, pwt, snw, svn, urb, wat, wsv, product_path, vector_path, var_log, 'mean')
            >>> mod12q1
            "Class to extract MODIS MOD12Q1 Version 6.1"

        Args:
            brn (HidroCLVariable): Object with the barren data \n
            crp (HidroCLVariable): Object with the cropland data \n
            csh (HidroCLVariable): Object with the closed shrubland data \n
            cvm (HidroCLVariable): Object with the cropland/natural vegetation mosaic data \n
            dbf (HidroCLVariable): Object with the deciduous broadleaf forest data \n
            dnf (HidroCLVariable): Object with the deciduous needleleaf forest data \n
            ebf (HidroCLVariable): Object with the evergreen broadleaf forest data \n
            enf (HidroCLVariable): Object with the evergreen needleleaf forest data \n
            grs (HidroCLVariable): Object with the grassland data \n
            mxf (HidroCLVariable): Object with the mixed forest data \n
            osh (HidroCLVariable): Object with the open shrubland data \n
            pwt (HidroCLVariable): Object with the permanent wetland data \n
            snw (HidroCLVariable): Object with the snow and ice data \n
            svn (HidroCLVariable): Object with the savannas data \n
            urb (HidroCLVariable): Object with the urban and built-up data \n
            wat (HidroCLVariable): Object with the water bodies data \n
            wsv (HidroCLVariable): Object with the woody savannas data \n
            product_path (str): Path to the product folder \n
            vector_path (str): Path to the vector folder \n
            var_log (str): Path to the log file for the variable extraction \n
            agg (str): Aggregation method to be used \n

        Raises:
            TypeError: If pet is not a HidroCLVariable object
        """
        if t.check_instance(brn, crp, csh, cvm, dbf, dnf, ebf, enf, grs, mxf,
                            osh, pwt, snw, svn, urb, wat, wsv):
            self.brn = brn
            self.crp = crp
            self.csh = csh
            self.cvm = cvm
            self.dbf = dbf
            self.dnf = dnf
            self.ebf = ebf
            self.enf = enf
            self.grs = grs
            self.mxf = mxf
            self.osh = osh
            self.pwt = pwt
            self.snw = snw
            self.svn = svn
            self.urb = urb
            self.wat = wat
            self.wsv = wsv
            if agg not in ['mean', 'sum']:
                raise ValueError('agg must be mean or sum')
            self.agg = agg
            self.var_log = var_log
            self.productname = "Class to extract MODIS MOD12Q1 Version 6.1"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = t.compare_indatabase(self.brn.indatabase,
                                                        self.crp.indatabase,
                                                        self.csh.indatabase,
                                                        self.cvm.indatabase,
                                                        self.dbf.indatabase,
                                                        self.dnf.indatabase,
                                                        self.ebf.indatabase,
                                                        self.enf.indatabase,
                                                        self.grs.indatabase,
                                                        self.mxf.indatabase,
                                                        self.osh.indatabase,
                                                        self.pwt.indatabase,
                                                        self.snw.indatabase,
                                                        self.svn.indatabase,
                                                        self.urb.indatabase,
                                                        self.wat.indatabase,
                                                        self.wsv.indatabase)
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
            raise TypeError('brn, crp, csh, cvm, dbf, dnf, ebf, enf, grs, mxf,' +
                            'osh, pwt, snw, svn, urb, wat and wsv must be HidroCLVariable objects')

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

Barren records: {len(self.brn.indatabase)}.
Barren database path: {self.brn.database}

Cropland records: {len(self.crp.indatabase)}.
Cropland database path: {self.crp.database}

Closed shrubland records: {len(self.csh.indatabase)}.
Closed shrubland database path: {self.csh.database}

Cropland/natural vegetation mosaic records: {len(self.cvm.indatabase)}.
Cropland/natural vegetation mosaic database path: {self.cvm.database}

Deciduous broadleaf forest records: {len(self.dbf.indatabase)}.
Deciduous broadleaf forest database path: {self.dbf.database}

Deciduous needleleaf forest records: {len(self.dnf.indatabase)}.
Deciduous needleleaf forest database path: {self.dnf.database}

Evergreen broadleaf forest records: {len(self.ebf.indatabase)}.
Evergreen broadleaf forest database path: {self.ebf.database}

Evergreen needleleaf forest records: {len(self.enf.indatabase)}.
Evergreen needleleaf forest database path: {self.enf.database}

Grassland records: {len(self.grs.indatabase)}.
Grassland database path: {self.grs.database}

Mixed forest records: {len(self.mxf.indatabase)}.
Mixed forest database path: {self.mxf.database}

Open shrubland records: {len(self.osh.indatabase)}.
Open shrubland database path: {self.osh.database}

Permanent wetland records: {len(self.pwt.indatabase)}.
Permanent wetland database path: {self.pwt.database}

Snow records: {len(self.snw.indatabase)}.
Snow database path: {self.snw.database}

Savannas records: {len(self.svn.indatabase)}.
Savannas database path: {self.svn.database}

Urban and built-up records: {len(self.urb.indatabase)}.
Urban and built-up database path: {self.urb.database}

Water bodies records: {len(self.wat.indatabase)}.
Water bodies database path: {self.wat.database}

Woody savannas records: {len(self.wsv.indatabase)}.
Woody savannas database path: {self.wsv.database}
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
            self.brn.checkdatabase()
            self.crp.checkdatabase()
            self.csh.checkdatabase()
            self.cvm.checkdatabase()
            self.dbf.checkdatabase()
            self.dnf.checkdatabase()
            self.ebf.checkdatabase()
            self.enf.checkdatabase()
            self.grs.checkdatabase()
            self.mxf.checkdatabase()
            self.osh.checkdatabase()
            self.pwt.checkdatabase()
            self.snw.checkdatabase()
            self.svn.checkdatabase()
            self.urb.checkdatabase()
            self.wat.checkdatabase()
            self.wsv.checkdatabase()

        self.common_elements = t.compare_indatabase(self.brn.indatabase,
                                                    self.crp.indatabase,
                                                    self.csh.indatabase,
                                                    self.cvm.indatabase,
                                                    self.dbf.indatabase,
                                                    self.dnf.indatabase,
                                                    self.ebf.indatabase,
                                                    self.enf.indatabase,
                                                    self.grs.indatabase,
                                                    self.mxf.indatabase,
                                                    self.osh.indatabase,
                                                    self.pwt.indatabase,
                                                    self.snw.indatabase,
                                                    self.svn.indatabase,
                                                    self.urb.indatabase,
                                                    self.wat.indatabase,
                                                    self.wsv.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements)

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                if scene not in self.brn.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_brn',
                                  self.brn.catchment_names, self.var_log,
                                  database=self.brn.database,
                                  pcdatabase=self.brn.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=16)
                if scene not in self.crp.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_crp',
                                  self.crp.catchment_names, self.var_log,
                                  database=self.crp.database,
                                  pcdatabase=self.crp.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=12)
                if scene not in self.csh.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_csh',
                                  self.csh.catchment_names, self.var_log,
                                  database=self.csh.database,
                                  pcdatabase=self.csh.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=6)
                if scene not in self.cvm.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_cvm',
                                  self.cvm.catchment_names, self.var_log,
                                  database=self.cvm.database,
                                  pcdatabase=self.cvm.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=14)
                if scene not in self.dbf.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_dbf',
                                  self.dbf.catchment_names, self.var_log,
                                  database=self.dbf.database,
                                  pcdatabase=self.dbf.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=4)
                if scene not in self.dnf.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_dnf',
                                  self.dnf.catchment_names, self.var_log,
                                  database=self.dnf.database,
                                  pcdatabase=self.dnf.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=3)
                if scene not in self.ebf.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_ebf',
                                  self.ebf.catchment_names, self.var_log,
                                  database=self.ebf.database,
                                  pcdatabase=self.ebf.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=2)
                if scene not in self.enf.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_enf',
                                  self.enf.catchment_names, self.var_log,
                                  database=self.enf.database,
                                  pcdatabase=self.enf.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=1)
                if scene not in self.grs.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_grs',
                                  self.grs.catchment_names, self.var_log,
                                  database=self.grs.database,
                                  pcdatabase=self.grs.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=10)
                if scene not in self.mxf.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_mxf',
                                  self.mxf.catchment_names, self.var_log,
                                  database=self.mxf.database,
                                  pcdatabase=self.mxf.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=5)
                if scene not in self.osh.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_osh',
                                  self.osh.catchment_names, self.var_log,
                                  database=self.osh.database,
                                  pcdatabase=self.osh.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=7)
                if scene not in self.pwt.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_pwt',
                                  self.pwt.catchment_names, self.var_log,
                                  database=self.pwt.database,
                                  pcdatabase=self.pwt.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=11)
                if scene not in self.snw.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_snw',
                                  self.snw.catchment_names, self.var_log,
                                  database=self.snw.database,
                                  pcdatabase=self.snw.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=15)
                if scene not in self.svn.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_svn',
                                  self.svn.catchment_names, self.var_log,
                                  database=self.svn.database,
                                  pcdatabase=self.svn.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=9)
                if scene not in self.urb.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_urb',
                                  self.urb.catchment_names, self.var_log,
                                  database=self.urb.database,
                                  pcdatabase=self.urb.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=13)
                if scene not in self.wat.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_wat',
                                  self.wat.catchment_names, self.var_log,
                                  database=self.wat.database,
                                  pcdatabase=self.wat.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=17)
                if scene not in self.wsv.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'lulc_wsv',
                                  self.wsv.catchment_names, self.var_log,
                                  database=self.wsv.database,
                                  pcdatabase=self.wsv.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="LC_Type1",
                                  aggregation=self.agg, value=8)

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
            self.brn.checkdatabase()
            self.crp.checkdatabase()
            self.csh.checkdatabase()
            self.cvm.checkdatabase()
            self.dbf.checkdatabase()
            self.dnf.checkdatabase()
            self.ebf.checkdatabase()
            self.enf.checkdatabase()
            self.grs.checkdatabase()
            self.mxf.checkdatabase()
            self.osh.checkdatabase()
            self.pwt.checkdatabase()
            self.snw.checkdatabase()
            self.svn.checkdatabase()
            self.urb.checkdatabase()
            self.wat.checkdatabase()
            self.wsv.checkdatabase()

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


# """
# Extraction of PERSIANN-CCS 0.04º degree product:
# """
#
#
# class Persiann_ccs:
#     """
#     A class to process PERSIANN-CCS to hidrocl variables
#
#     Attributes:
#         pp (HidroCLVariable): HidroCLVariable object with PERSIANN-CCS precipitation data \n
#         pp_log (str): Path to the log file for PERSIANN-CCS precipitation data \n
#         productname (str): Name of the remote sensing product to be processed \n
#         productpath (str): Path to the product folder where the product files are located \n
#         vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
#         common_elements (list): common_elements (list): Elements in precipitation database \n
#         product_files (list): List of product files in the product folder \n
#         product_ids (list): List of product ids. Each product id is str with common tag by date \n
#         all_scenes (list): List of all scenes (no matter the product id here) \n
#         scenes_occurrences (list): List of scenes occurrences for each product id \n
#         overpopulated_scenes (list): List of overpopulated scenes (more than 1 scenes for modis) \n
#         complete_scenes (list): List of complete scenes (1 scenes for modis) \n
#         incomplete_scenes (list): List of incomplete scenes (less than 1 scenes for modis) \n
#         scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
#     """
#
#     def __init__(self, pp, product_path, vector_path, pp_log):
#         """
#         Examples:
#             >>> from hidrocl import HidroCLVariable
#             >>> from hidrocl import Persiann_ccs
#             >>> pp = HidroCLVariable('pp', 'pp.db', 'pp_pc.db')
#             >>> product_path = '/home/user/data/PERSIANN-CCS'
#             >>> vector_path = '/home/user/data/vector.shp'
#             >>> pp_log = '/home/user/data/logs/pp_log.txt'
#             >>> persiann_ccs = Persiann_ccs(pp, product_path, vector_path, pp_log)
#             >>> persiann_ccs
#             "Class to extract PERSIANN-CCS 0.04º"
#
#         Args:
#             pp (HidroCLVariable): HidroCLVariable object with PERSIANN-CCS precipitation data \n
#             product_path (str): Path to the product folder where the product files are located \n
#             vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
#             pp_log (str): Path to the log file for PERSIANN-CCS precipitation data \n
#
#         Raises:
#             TypeError: If pp is not a HidroCLVariable object
#         """
#         if t.check_instance(pp):
#             self.pp = pp
#             self.pp_log = pp_log
#             self.productname = "PERSIANN-CCS 0.04º"
#             self.productpath = product_path
#             self.vectorpath = vector_path
#             self.common_elements = self.pp.indatabase
#             self.product_files = t.read_product_files(self.productpath, "persiann_ccs")
#             self.product_ids = t.get_product_ids(self.product_files, "persiann_ccs")
#             self.all_scenes = t.check_product_files(self.product_ids)
#             self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
#             (self.overpopulated_scenes,
#              self.complete_scenes,
#              self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "persiann_ccs")
#             self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
#                                                             self.common_elements, what='persiann_ccs')
#         else:
#             raise TypeError('pp must be HidroCLVariable object')
#
#     def __repr__(self):
#         """
#         Return a string representation of the object
#
#         Returns:
#              str: String representation of the object
#         """
#         return f'Class to extract {self.productname}'
#
#     def __str__(self):
#         """
#         Return a string representation of the object
#
#         Returns:
#             str: String representation of the object
#         """
#         return f'''
# Product: {self.productname}
#
# PERSIANN-CCS precipitation records: {len(self.pp.indatabase)}.
# PERSIANN-CCS precipitation database path: {self.pp.database}
#         '''
#
#     def run_extraction(self, limit=None):
#         """
#         Run the extraction of the product.
#         If limit is None, all scenes will be processed.
#         If limit is a number, only the first limit scenes will be processed.
#
#         Args:
#             limit (int): length of the scenes_to_process
#
#         Returns:
#             str: Print
#         """
#
#         with t.HiddenPrints():
#             self.pp.checkdatabase()
#
#         self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase, "persiann_ccs")
#
#         scenes_path = t.get_scenes_path(self.product_files, self.productpath)
#
#         with TemporaryDirectory() as tempdirname:
#             temp_dir = Path(tempdirname)
#
#             if limit is not None:
#                 scenes_to_process = self.scenes_to_process[:limit]
#             else:
#                 scenes_to_process = self.scenes_to_process
#
#             for scene in scenes_to_process:
#                 if scene not in self.pp.indatabase:
#                     e.zonal_stats(scene, scenes_path,
#                                   temp_dir, "persiann_ccs",
#                                   self.pp.catchment_names, self.pp_log,
#                                   database=self.pp.database,
#                                   pcdatabase=self.pp.pcdatabase,
#                                   vector_path=self.vectorpath)
#
#     def run_maintainer(self, log_file, limit=None):
#         """
#         Run file maintainer. It will remove any file with problems
#
#         Args:
#             log_file (str): log file path
#             limit (int): length of the scenes_to_process
#
#         Returns:
#             str: Print
#         """
#
#         with t.HiddenPrints():
#             self.pp.checkdatabase()
#
#         self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase, "persiann_ccs")
#
#         scenes_path = t.get_scenes_path(self.product_files, self.productpath)
#
#         if limit is not None:
#             scenes_to_process = self.scenes_to_process[:limit]
#         else:
#             scenes_to_process = self.scenes_to_process
#
#         for scene in scenes_to_process:
#             m.file_maintainer(scene=scene,
#                               scenes_path=scenes_path,
#                               name='persiann',
#                               log_file=log_file)
#
#
# """
# Extraction of PERSIANN-CCS-CDR 0.04º degree product:
# """
#
#
# class Persiann_ccs_cdr:
#     """
#     A class to process PERSIANN-CCS-CDR to hidrocl variables
#
#     Attributes:
#         pp (HidroCLVariable): HidroCLVariable object with PERSIANN-CCS-CDR precipitation data \n
#         pp_log (str): Path to the log file for PERSIANN-CCS-CDR precipitation data \n
#         productname (str): Name of the remote sensing product to be processed \n
#         productpath (str): Path to the product folder where the product files are located \n
#         vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
#         common_elements (list): common_elements (list): Elements in precipitation database \n
#         product_files (list): List of product files in the product folder \n
#         product_ids (list): List of product ids. Each product id is str with common tag by date \n
#         all_scenes (list): List of all scenes (no matter the product id here) \n
#         scenes_occurrences (list): List of scenes occurrences for each product id \n
#         overpopulated_scenes (list): List of overpopulated scenes (more than 1 scenes for modis) \n
#         complete_scenes (list): List of complete scenes (1 scenes for modis) \n
#         incomplete_scenes (list): List of incomplete scenes (less than 1 scenes for modis) \n
#         scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
#     """
#
#     def __init__(self, pp, product_path, vector_path, pp_log):
#         """
#         Examples:
#             >>> from hidrocl import HidroCLVariable
#             >>> from hidrocl import Persiann_ccs_cdr
#             >>> pp = HidroCLVariable('pp', 'pp.db', 'pp_pc.db')
#             >>> product_path = '/home/user/data/PERSIANN-CCS-CDR'
#             >>> vector_path = '/home/user/data/vector.shp'
#             >>> pp_log = '/home/user/data/logs/pp_log.txt'
#             >>> persiann_ccs_cdr = Persiann_ccs_cdr(pp, product_path, vector_path, pp_log)
#             >>> persiann_ccs_cdr
#             "Class to extract PERSIANN-CCS-CDR 0.04º"
#
#         Args:
#             pp (HidroCLVariable): HidroCLVariable object with PERSIANN-CCS-CDR precipitation data \n
#             product_path (str): Path to the product folder where the product files are located \n
#             vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
#             pp_log (str): Path to the log file for PERSIANN-CCS-CDR precipitation data \n
#
#         Raises:
#             TypeError: If pp is not a HidroCLVariable object
#         """
#         if t.check_instance(pp):
#             self.pp = pp
#             self.pp_log = pp_log
#             self.productname = "PERSIANN-CCS-CDR 0.04º"
#             self.productpath = product_path
#             self.vectorpath = vector_path
#             self.common_elements = self.pp.indatabase
#             self.product_files = t.read_product_files(self.productpath, "persiann_ccs_cdr")
#             self.product_ids = t.get_product_ids(self.product_files, "persiann_ccs_cdr")
#             self.all_scenes = t.check_product_files(self.product_ids)
#             self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
#             (self.overpopulated_scenes,
#              self.complete_scenes,
#              self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "persiann_ccs_cdr")
#             self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
#                                                             self.common_elements, what='persiann_ccs_cdr')
#         else:
#             raise TypeError('pp must be HidroCLVariable object')
#
#     def __repr__(self):
#         """
#         Return a string representation of the object
#
#         Returns:
#              str: String representation of the object
#         """
#         return f'Class to extract {self.productname}'
#
#     def __str__(self):
#         """
#         Return a string representation of the object
#
#         Returns:
#             str: String representation of the object
#         """
#         return f'''
# Product: {self.productname}
#
# PERSIANN-CCS-CDR precipitation records: {len(self.pp.indatabase)}.
# PERSIANN-CCS-CDR precipitation database path: {self.pp.database}
#         '''
#
#     def run_extraction(self, limit=None):
#         """
#         Run the extraction of the product.
#         If limit is None, all scenes will be processed.
#         If limit is a number, only the first limit scenes will be processed.
#
#         Args:
#             limit (int): length of the scenes_to_process
#
#         Returns:
#             str: Print
#         """
#
#         with t.HiddenPrints():
#             self.pp.checkdatabase()
#
#         self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase, 'persiann_ccs_cdr')
#
#         scenes_path = t.get_scenes_path(self.product_files, self.productpath)
#
#         with TemporaryDirectory() as tempdirname:
#             temp_dir = Path(tempdirname)
#
#             if limit is not None:
#                 scenes_to_process = self.scenes_to_process[:limit]
#             else:
#                 scenes_to_process = self.scenes_to_process
#
#             for scene in scenes_to_process:
#                 if scene not in self.pp.indatabase:
#                     e.zonal_stats(scene, scenes_path,
#                                   temp_dir, "persiann_ccs_cdr",
#                                   self.pp.catchment_names, self.pp_log,
#                                   database=self.pp.database,
#                                   pcdatabase=self.pp.pcdatabase,
#                                   vector_path=self.vectorpath)
#
#     def run_maintainer(self, log_file, limit=None):
#         """
#         Run file maintainer. It will remove any file with problems
#
#         Args:
#             log_file (str): log file path
#             limit (int): length of the scenes_to_process
#
#         Returns:
#             str: Print
#         """
#
#         with t.HiddenPrints():
#             self.pp.checkdatabase()
#
#         self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.pp.indatabase, 'persiann_ccs_cdr')
#
#         scenes_path = t.get_scenes_path(self.product_files, self.productpath)
#
#         if limit is not None:
#             scenes_to_process = self.scenes_to_process[:limit]
#         else:
#             scenes_to_process = self.scenes_to_process
#
#         for scene in scenes_to_process:
#             m.file_maintainer(scene=scene,
#                               scenes_path=scenes_path,
#                               name='persiann',
#                               log_file=log_file)


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
        overpopulated_scenes (list): List of overpopulated scenes (more than 1 scene for modis) \n
        complete_scenes (list): List of complete scenes (1 scene for modis) \n
        incomplete_scenes (list): List of incomplete scenes (less than 1 scene for modis) \n
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

    potential evapotranspiration: pev -> pet (10000 * m) sum \n
    snow albedo: asn -> snwa (10 * frac) mean \n
    snow cover: snowc -> snw (10 * frac) mean \n
    snow density: rsn -> snwdn (10 * kg/m3) mean \n
    snow depth: sd -> snwdt (10 * m) mean \n
    evapotranspiration: e -> et (10000 * m) sum \n
    # out now: total precipitation: tp -> pp (10000 * m) sum \n
    volumetric soil water: swvl1+swvl2+swvl3+swvl4 -> soilm (1000 * m3/m3) mean \n

    et, pet, snow, snowa, snowdn, snowdt, soilm \n

    Attributes:
        et (HidroCLVariable): HidroCLVariable object with ERA5 evapotranspiration data \n
        pet (HidroCLVariable): HidroCLVariable object with ERA5 potential evapotranspiration data \n
        snw (HidroCLVariable): HidroCLVariable object with ERA5 snow cover data \n
        snwa (HidroCLVariable): HidroCLVariable object with ERA5 snow albedo data \n
        snwdn (HidroCLVariable): HidroCLVariable object with ERA5 snow density data \n
        snwdt (HidroCLVariable): HidroCLVariable object with ERA5 snow depth data \n
        soilm (HidroCLVariable): HidroCLVariable object with ERA5 volumetric soil water data \n
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

    def __init__(self, et, pet, snw, snwa, snwdn, snwdt,
                 soilm, product_path, vector_path,
                 et_log, pet_log, snw_log, snwa_log, snwdn_log,
                 snwdt_log, soilm_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Era5_land
            >>> et = HidroCLVariable('et', et.db, etpc.db)
            >>> pet = HidroCLVariable('pet', pet.db, petpc.db)
            >>> snw = HidroCLVariable('snw', snw.db, snwpc.db)
            >>> snwa = HidroCLVariable('snwa', snwa.db, snwapc.db)
            >>> snwdn = HidroCLVariable('snwdn', snwdn.db, snwdnpc.db)
            >>> snwdt = HidroCLVariable('snwdt', snwdt.db, snwdtpc.db)
            >>> soilm = HidroCLVariable('soilm', soilm.db, soilmdb.db)
            >>> product_path = '/home/user/era5-land'
            >>> vector_path = '/home/user/shapefiles'
            >>> et_log = '/home/user/et.log'
            >>> pet_log = '/home/user/pet.log'
            >>> snw_log = '/home/user/snw.log'
            >>> snwa_log = '/home/user/snwa.log'
            >>> snwdn_log = '/home/user/snwdn.log'
            >>> snwdt_log = '/home/user/snwdt.log'
            >>> soilm_log = '/home/user/soilm.log'
            >>> era5 = Era5_land(et, pet, snw, snwa, snwdn, snwdt,
                                 soilm, product_path, vector_path,
                                 et_log, pet_log, snw_log, snwa_log,
                                 snwdn_log, snwdt_log, soilm_log)
            >>> era5
            "Class to extract ERA5-Land Hourly 0.1 degree"
            >>> era5.run_extraction()


        Args:
            et (HidroCLVariable): HidroCLVariable object with ERA5 evapotranspiration data \n
            pet (HidroCLVariable): HidroCLVariable object with ERA5 potential evapotranspiration data \n
            snw (HidroCLVariable): HidroCLVariable object with ERA5 snow cover data \n
            snwa (HidroCLVariable): HidroCLVariable object with ERA5 snow albedo data \n
            snwdn (HidroCLVariable): HidroCLVariable object with ERA5 snow density data \n
            snwdt (HidroCLVariable): HidroCLVariable object with ERA5 snow depth data \n
            soilm (HidroCLVariable): HidroCLVariable object with ERA5 volumetric soil water data \n
            product_path (str): Path to the product folder where the product files are located \n
            vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
            et_log (str): Log file path for evapotranspiration data \n
            pet_log (str): Log file path for potential evapotranspiration data \n
            snw_log (str): Log file path for snow cover data \n
            snwa_log (str): Log file path for snow albedo data \n
            snwdn_log (str): Log file path for snow density data \n
            snwdt_log (str): Log file path for snow depth data \n
            soilm_log (str): Log file path for volumetric soil water data \n

        Raises:
            TypeError: If pp, et, pet, snow, snowa, snowdn, snowdt or soilm is not HidroCLVariable objects \n
        """
        if t.check_instance(et, pet, snw, snwa, snwdn, snwdt, soilm):
            self.et = et
            self.pet = pet
            self.snw = snw
            self.snwa = snwa
            self.snwdn = snwdn
            self.snwdt = snwdt
            self.soilm = soilm
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
            self.common_elements = t.compare_indatabase(self.et.indatabase,
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
            raise TypeError('et, pet, snw, snwa, snwdn, snwdt ' +
                            'and soilm must be HidroCLVariable objects')

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

    def run_extraction(self, scene=None, limit=None):
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        Args:
            scene (str): scene name
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.et.checkdatabase()
            self.pet.checkdatabase()
            self.snw.checkdatabase()
            self.snwa.checkdatabase()
            self.snwdn.checkdatabase()
            self.snwdt.checkdatabase()
            self.soilm.checkdatabase()

        self.common_elements = t.compare_indatabase(self.et.indatabase,
                                                    self.pet.indatabase,
                                                    self.snw.indatabase,
                                                    self.snwa.indatabase,
                                                    self.snwdn.indatabase,
                                                    self.snwdt.indatabase,
                                                    self.soilm.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, "era5")

        if scene is not None:
            if scene in self.scenes_to_process:
                self.scenes_to_process = [scene]
            else:
                print(f'{scene} not in the scenes to process. Please, check the scene name.')
                return

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                if scene not in self.et.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'et_era5',
                                  self.et.catchment_names, self.et_log,
                                  database=self.et.database,
                                  pcdatabase=self.et.pcdatabase,
                                  vector_path=self.vectorpath,
                                  aggregation='sum',
                                  layer="e")

                if scene not in self.pet.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'pet_era5',
                                  self.pet.catchment_names, self.pet_log,
                                  database=self.pet.database,
                                  pcdatabase=self.pet.pcdatabase,
                                  vector_path=self.vectorpath,
                                  aggregation='sum',
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
            self.et.checkdatabase()
            self.pet.checkdatabase()
            self.snw.checkdatabase()
            self.snwa.checkdatabase()
            self.snwdn.checkdatabase()
            self.snwdt.checkdatabase()
            self.soilm.checkdatabase()

        self.common_elements = t.compare_indatabase(self.et.indatabase,
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
Extraction of ERA5 hourly data product:
"""


class Era5:
    """
    A class to process ERA5 hourly to hidrocl variables. Where:

    total precipitation: tp -> pp (10000 * m) sum \n
    air temperature: t2m -> temp (10 * ºC) mean \n
    dewpoint temperature: d2m -> dew (10 * ºC) mean \n
    surface pressure: sp -> pres (10 * Pa) mean \n
    u wind component: u10 -> u (10 * m/s) mean \n
    v wind component: v10 -> v (10 * m/s) mean \n

    pp, dew, pres, u, v: HidroCLVariable object with ERA5 data \n

    Attributes:
        pp (HidroCLVariable): HidroCLVariable object with ERA5 precipitation data \n
        temp (HidroCLVariable): HidroCLVariable object with ERA5 air temperature data \n
        tempmin (HidroCLVariable): HidroCLVariable object with ERA5 minimum air temperature data \n
        tempmax (HidroCLVariable): HidroCLVariable object with ERA5 maximum air temperature data \n
        dew (HidroCLVariable): HidroCLVariable object with ERA5 dewpoint temperature data \n
        pres (HidroCLVariable): HidroCLVariable object with ERA5 surface pressure data \n
        u (HidroCLVariable): HidroCLVariable object with ERA5 u wind component data \n
        v (HidroCLVariable): HidroCLVariable object with ERA5 v wind component data \n
        pp_log (str): Log file path for precipitation data \n
        temp_log (str): Log file path for air temperature data \n
        tempmin_log (str): Log file path for minimum air temperature data \n
        tempmax_log (str): Log file path for maximum air temperature data \n
        dew_log (str): Log file path for dewpoint temperature data \n
        pres_log (str): Log file path for surface pressure data \n
        u_log (str): Log file path for u wind component data \n
        v_log (str): Log file path for v wind component data \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): List of common elements between the pp, dew, pres, u and v databases \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 1 scenes for era5) \n
        complete_scenes (list): List of complete scenes (1 scenes for era5) \n
        incomplete_scenes (list): List of incomplete scenes (less than 1 scenes for era5) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, pp, temp, tempmin, tempmax,
                 dew, pres, u, v, product_path, vector_path,
                 pp_log, temp_log, tempmin_log, tempmax_log,
                 dew_log, pres_log, u_log, v_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Era5
            >>> pp = HidroCLVariable('pp', pp.db, pppc.db)
            >>> temp = HidroCLVariable('temp', temp.db, temppc.db)
            >>> tempmin = HidroCLVariable('tempmin', tempmin.db, tempminpc.db)
            >>> tempmax = HidroCLVariable('tempmax', tempmax.db, tempmaxpc.db)
            >>> dew = HidroCLVariable('dew', dew.db, dewpc.db)
            >>> pres = HidroCLVariable('pres', pres.db, prespc.db)
            >>> u = HidroCLVariable('u', u.db, upc.db)
            >>> v = HidroCLVariable('v', v.db, vpc.db)
            >>> product_path = '/home/user/era5'
            >>> vector_path = '/home/user/shapefiles'
            >>> pp_log = '/home/user/pp.log'
            >>> dew_log = '/home/user/dew.log'
            >>> pres_log = '/home/user/pres.log'
            >>> u_log = '/home/user/u.log'
            >>> v_log = '/home/user/v.log'
            >>> era5 = Era5(pp, temp, tempmin, tempmax,
                            dew, pres, u, v,
                            product_path, vector_path,
                            pp_log, temp_log,
                            tempmin_log, tempmax_log,
                            pp_log, dew_log, pres_log, u_log, v_log)
            >>> era5
            "Class to extract ERA5 Hourly 0.25 degree"
            >>> era5.run_extraction()


        Args:
            pp (HidroCLVariable): HidroCLVariable object with ERA5 precipitation data \n
            temp (HidroCLVariable): HidroCLVariable object with ERA5 air temperature data \n
            tempmin (HidroCLVariable): HidroCLVariable object with ERA5 minimum air temperature data \n
            tempmax (HidroCLVariable): HidroCLVariable object with ERA5 maximum air temperature data \n
            dew (HidroCLVariable): HidroCLVariable object with ERA5 dewpoint temperature data \n
            pres (HidroCLVariable): HidroCLVariable object with ERA5 surface pressure data \n
            u (HidroCLVariable): HidroCLVariable object with ERA5 u wind component data \n
            v (HidroCLVariable): HidroCLVariable object with ERA5 v wind component data \n
            product_path (str): Path to the product folder where the product files are located \n
            vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
            pp_log (str): Log file path for precipitation data \n
            temp_log (str): Log file path for air temperature data \n
            tempmin_log (str): Log file path for minimum air temperature data \n
            tempmax_log (str): Log file path for maximum air temperature data \n
            dew_log (str): Log file path for dewpoint temperature data \n
            pres_log (str): Log file path for surface pressure data \n
            u_log (str): Log file path for u wind component data \n
            v_log (str): Log file path for v wind component data \n

        Raises:
            TypeError: If pp, temp, tempmin, tempmax, dew, pres, u or v are not HidroCLVariable objects \n
        """
        if t.check_instance(pp, temp, tempmin, tempmax, dew, pres, u, v):
            self.pp = pp
            self.temp = temp
            self.tempmin = tempmin
            self.tempmax = tempmax
            self.dew = dew
            self.pres = pres
            self.u = u
            self.v = v
            self.pp_log = pp_log
            self.temp_log = temp_log
            self.tempmin_log = tempmin_log
            self.tempmax_log = tempmax_log
            self.dew_log = dew_log
            self.pres_log = pres_log
            self.u_log = u_log
            self.v_log = v_log
            self.productname = "ERA5 Hourly 0.25 degree on single levels"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = t.compare_indatabase(self.pp.indatabase,
                                                        self.temp.indatabase,
                                                        self.tempmin.indatabase,
                                                        self.tempmax.indatabase,
                                                        self.dew.indatabase,
                                                        self.pres.indatabase,
                                                        self.u.indatabase,
                                                        self.v.indatabase)
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
            raise TypeError('pp, temp, tempmin, tempmax, dew, pres, u and v must be HidroCLVariable objects')

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

Precipitation records: {len(self.pp.indatabase)}.
Precipitation path: {self.pp.database}

Air temperature records: {len(self.temp.indatabase)}.
Air temperature path: {self.temp.database}

Minimum air temperature records: {len(self.tempmin.indatabase)}.
Minimum air temperature path: {self.tempmin.database}

Maximum air temperature records: {len(self.tempmax.indatabase)}.
Maximum air temperature path: {self.tempmax.database}

Dewpoint temperature records: {len(self.dew.indatabase)}.
Dewpoint temperature path: {self.dew.database}

Surface pressure records: {len(self.pres.indatabase)}.
Surface pressure path: {self.pres.database}

U wind component records: {len(self.u.indatabase)}.
U wind component path: {self.u.database}

V wind component records: {len(self.v.indatabase)}.
V wind component path: {self.v.database}
                '''

    def run_extraction(self, scene=None, limit=None):
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        Args:
            scene (str): scene name
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.pp.checkdatabase()
            self.temp.checkdatabase()
            self.tempmin.checkdatabase()
            self.tempmax.checkdatabase()
            self.dew.checkdatabase()
            self.pres.checkdatabase()
            self.u.checkdatabase()
            self.v.checkdatabase()

        self.common_elements = t.compare_indatabase(self.pp.indatabase,
                                                    self.temp.indatabase,
                                                    self.tempmin.indatabase,
                                                    self.tempmax.indatabase,
                                                    self.dew.indatabase,
                                                    self.pres.indatabase,
                                                    self.u.indatabase,
                                                    self.v.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, "era5")

        if scene is not None:
            if scene in self.scenes_to_process:
                self.scenes_to_process = [scene]
            else:
                print(f'{scene} not in the scenes to process. Please, check the scene name.')
                return

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
                                  temp_dir, 'pp_era5',
                                  self.pp.catchment_names, self.pp_log,
                                  database=self.pp.database,
                                  pcdatabase=self.pp.pcdatabase,
                                  vector_path=self.vectorpath,
                                  aggregation='sum',
                                  layer="tp")

                if scene not in self.temp.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'temp_era5',
                                  self.temp.catchment_names, self.temp_log,
                                  database=self.temp.database,
                                  pcdatabase=self.temp.pcdatabase,
                                  vector_path=self.vectorpath,
                                  aggregation='mean',
                                  layer="t2m")

                if scene not in self.tempmin.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'tempmin_era5',
                                  self.tempmin.catchment_names, self.tempmin_log,
                                  database=self.tempmin.database,
                                  pcdatabase=self.tempmin.pcdatabase,
                                  vector_path=self.vectorpath,
                                  aggregation='min',
                                  layer="t2m")

                if scene not in self.tempmax.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'tempmax_era5',
                                  self.tempmax.catchment_names, self.tempmax_log,
                                  database=self.tempmax.database,
                                  pcdatabase=self.tempmax.pcdatabase,
                                  vector_path=self.vectorpath,
                                  aggregation='max',
                                  layer="t2m")

                if scene not in self.dew.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'dew_era5',
                                  self.dew.catchment_names, self.dew_log,
                                  database=self.dew.database,
                                  pcdatabase=self.dew.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="d2m")

                if scene not in self.pres.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'pres_era5',
                                  self.pres.catchment_names, self.pres_log,
                                  database=self.pres.database,
                                  pcdatabase=self.pres.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="sp")

                if scene not in self.u.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'u10_era5',
                                  self.u.catchment_names, self.u_log,
                                  database=self.u.database,
                                  pcdatabase=self.u.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="u10")

                if scene not in self.v.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'v10_era5',
                                  self.v.catchment_names, self.v_log,
                                  database=self.v.database,
                                  pcdatabase=self.v.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="v10")

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
            self.temp.checkdatabase()
            self.tempmin.checkdatabase()
            self.tempmax.checkdatabase()
            self.dew.checkdatabase()
            self.pres.checkdatabase()
            self.u.checkdatabase()
            self.v.checkdatabase()

        self.common_elements = t.compare_indatabase(self.pp.indatabase,
                                                    self.temp.indatabase,
                                                    self.tempmin.indatabase,
                                                    self.tempmax.indatabase,
                                                    self.dew.indatabase,
                                                    self.pres.indatabase,
                                                    self.u.indatabase,
                                                    self.v.indatabase)

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
Extraction of ERA5 max precipitation 3-hour data:
"""


class Era5ppmax:
    """
    A class to process ERA5 hourly to hidrocl variables. Where:

    total precipitation: tp -> pp (10000 * m) sum \n

    ppmax: HidroCLVariable object with ERA5 data \n

    Attributes:
        ppmax (HidroCLVariable): HidroCLVariable object with ERA5 maximum precipitation data \n
        ppmax_log (str): Log file path for maximum precipitation data \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): List of common elements between pp database \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 1 scene for era5) \n
        complete_scenes (list): List of complete scenes (1 scene for era5) \n
        incomplete_scenes (list): List of incomplete scenes (less than 1 scene for era5) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, ppmax, product_path, vector_path, ppmax_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Era5ppmax
            >>> ppmax = HidroCLVariable('ppmax', ppmax.db, ppmaxpc.db)
            >>> product_path = '/home/user/era5'
            >>> vector_path = '/home/user/shapefiles'
            >>> ppmax_log = '/home/user/pp.log'
            >>> era5 = Era5(ppmax, product_path, vector_path,
                            ppmax_log)
            >>> era5
            "Class to extract ERA5 max precipitation 3-Hour 0.25 degree"
            >>> era5.run_extraction()


        Args:
            ppmax (HidroCLVariable): HidroCLVariable object with ERA5 maximum precipitation data \n
            product_path (str): Path to the product folder where the product files are located \n
            vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
            ppmax_log (str): Log file path for maximum precipitation data \n

        Raises:
            TypeError: If ppmax is not HidroCLVariable objects \n
        """
        if t.check_instance(ppmax):
            self.ppmax = ppmax
            self.ppmax_log = ppmax_log
            self.productname = "ERA5 max precipitation 3-Hour 0.25 degree"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = t.compare_indatabase(self.ppmax.indatabase)
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
            raise TypeError('ppmax must be HidroCLVariable object')

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

Maximum precipitation records: {len(self.ppmax.indatabase)}.
Maximum precipitation path: {self.ppmax.database}
                '''

    def run_extraction(self, scene=None, limit=None):
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        Args:
            scene (str): scene name
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.ppmax.checkdatabase()

        self.common_elements = t.compare_indatabase(self.ppmax.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, "era5")

        if scene is not None:
            if scene in self.scenes_to_process:
                self.scenes_to_process = [scene]
            else:
                print(f'{scene} not in the scenes to process. Please, check the scene name.')
                return

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                if scene not in self.ppmax.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'maxpp_eraacc',
                                  self.ppmax.catchment_names, self.ppmax_log,
                                  database=self.ppmax.database,
                                  pcdatabase=self.ppmax.pcdatabase,
                                  vector_path=self.vectorpath,
                                  aggregation='max',
                                  layer="tp")

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
            self.ppmax.checkdatabase()

        self.common_elements = t.compare_indatabase(self.ppmax.indatabase)

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
Extraction of ERA5 precipitation length 3-hour data:
"""


class Era5pplen:
    """
    A class to process ERA5 hourly to hidrocl variables. Where:

    total precipitation: tp -> pp (10000 * m) sum \n

    ppmax: HidroCLVariable object with ERA5 data \n

    Attributes:
        pplen (HidroCLVariable): HidroCLVariable object with ERA5 precipitation length data \n
        pplen_log (str): Log file path for precipitation length data \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): List of common elements between pp database \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 1 scene for era5) \n
        complete_scenes (list): List of complete scenes (1 scene for era5) \n
        incomplete_scenes (list): List of incomplete scenes (less than 1 scene for era5) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, pplen, product_path, vector_path, pplen_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Era5pplen
            >>> pplen = HidroCLVariable('pplen', pplen.db, pplenpc.db)
            >>> product_path = '/home/user/era5'
            >>> vector_path = '/home/user/shapefiles'
            >>> pplen_log = '/home/user/pp.log'
            >>> era5 = Era5(pplen, product_path, vector_path,
                            pplen_log)
            >>> era5
            "Class to extract ERA5 precipitation 3-Hour length 0.25 degree"
            >>> era5.run_extraction()


        Args:
            ppmax (HidroCLVariable): HidroCLVariable object with ERA5 maximum precipitation data \n
            product_path (str): Path to the product folder where the product files are located \n
            vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
            ppmax_log (str): Log file path for maximum precipitation data \n

        Raises:
            TypeError: If pplen is not HidroCLVariable objects \n
        """
        if t.check_instance(pplen):
            self.pplen = pplen
            self.pplen_log = pplen_log
            self.productname = "ERA5 precipitation 3-Hour length 0.25 degree"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = t.compare_indatabase(self.pplen.indatabase)
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
            raise TypeError('pplen must be HidroCLVariable object')

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

Precipitation length records: {len(self.pplen.indatabase)}.
Precipitation length path: {self.pplen.database}
                '''

    def run_extraction(self, scene=None, limit=None):
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        Args:
            scene (str): scene name
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.pplen.checkdatabase()

        self.common_elements = t.compare_indatabase(self.pplen.indatabase)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, "era5")

        if scene is not None:
            if scene in self.scenes_to_process:
                self.scenes_to_process = [scene]
            else:
                print(f'{scene} not in the scenes to process. Please, check the scene name.')
                return

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                if scene not in self.pplen.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'pp_era5',
                                  self.pplen.catchment_names, self.pplen_log,
                                  database=self.pplen.database,
                                  pcdatabase=self.pplen.pcdatabase,
                                  vector_path=self.vectorpath,
                                  aggregation='len',
                                  layer="tp",
                                  prec_threshold=1)

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
            self.pplen.checkdatabase()

        self.common_elements = t.compare_indatabase(self.pplen.indatabase)

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
Extraction of ERA5 Pressure levels hourly data product:
"""


class Era5_pressure:
    """
    A class to process ERA5 pressure levels hourly to hidrocl variables. Where:

    geopotential height 500 hPa: z -> z (10 * m) mean \n

    z: HidroCLVariable object with ERA5 data \n

    Attributes:
        z (HidroCLVariable): HidroCLVariable object with ERA5 geopotential height 500 hPa data \n
        z_log (str): Log file path for geopotential height data \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): List of common elements / this case the same elements \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 1 scene for era5) \n
        complete_scenes (list): List of complete scenes (1 scene for era5) \n
        incomplete_scenes (list): List of incomplete scenes (less than 1 scene for era5) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, z, product_path, vector_path, z_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Era5_pressure
            >>> z = HidroCLVariable('z', z.db, zpc.db)
            >>> product_path = '/home/user/era5-pressure-levels'
            >>> vector_path = '/home/user/shapefiles'
            >>> z_log = '/home/user/z.log'
            >>> era5 = Era5_pressure(z, product_path, vector_path, z_log)
            >>> era5
            "Class to extract ERA5 Pressure Levels Hourly 0.25 degree"
            >>> era5.run_extraction()


        Args:
            z (HidroCLVariable): HidroCLVariable object with ERA5 geopotential height data \n
            product_path (str): Path to the product folder where the product files are located \n
            vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
            z_log (str): Log file path for geopotential height data \n

        Raises:
            TypeError: If z is not HidroCLVariable object \n
        """
        if t.check_instance(z):
            self.z = z
            self.z_log = z_log
            self.productname = "ERA5 Pressure Levels Hourly 0.25 degree"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = self.z.indatabase
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
            raise TypeError('z must be HidroCLVariable object')

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

Geo potential height records: {len(self.z.indatabase)}.
Geo potential height path: {self.z.database}
                '''

    def run_extraction(self, scene=None, limit=None):
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        Args:
            scene (str): scene name
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.z.checkdatabase()

        self.common_elements = self.z.indatabase

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, "era5")

        if scene is not None:
            if scene in self.scenes_to_process:
                self.scenes_to_process = [scene]
            else:
                print(f'{scene} not in the scenes to process. Please, check the scene name.')
                return

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                if scene not in self.z.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'z_era5',
                                  self.z.catchment_names, self.z_log,
                                  database=self.z.database,
                                  pcdatabase=self.z.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="z")

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
            self.z.checkdatabase()

        self.common_elements = self.z.indatabase

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
Extraction of ERA5 Relative humidity hourly data product:
"""


class Era5_rh:
    """
    A class to process ERA5 relative humidity hourly to hidrocl variables. Where:

    relative humidity (%): rh -> rh (10 * %) mean \n

    rh: HidroCLVariable object with ERA5 data \n

    Attributes:
        rh (HidroCLVariable): HidroCLVariable object with ERA5 relative humidity data \n
        rh_log (str): Log file path for relative humidity data \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        common_elements (list): List of common elements / this case the same elements \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 1 scene for era5) \n
        complete_scenes (list): List of complete scenes (1 scene for era5) \n
        incomplete_scenes (list): List of incomplete scenes (less than 1 scene for era5) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, rh, product_path, vector_path, rh_log):
        """
        Examples:
            >>> from hidrocl import HidroCLVariable
            >>> from hidrocl import Era5_rh
            >>> rh = HidroCLVariable('rh', rh.db, rhpc.db)
            >>> product_path = '/home/user/era5-rh'
            >>> vector_path = '/home/user/shapefiles'
            >>> rh_log = '/home/user/rh.log'
            >>> era5 = Era5_rh(rh, product_path, vector_path, rh_log)
            >>> era5
            "Class to extract ERA5 Relative humidity Hourly 0.25 degree"
            >>> era5.run_extraction()


        Args:
            rh (HidroCLVariable): HidroCLVariable object with ERA5 relative humidity data \n
            product_path (str): Path to the product folder where the product files are located \n
            vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
            rh_log (str): Log file path for relative humidity data \n

        Raises:
            TypeError: If rh is not HidroCLVariable object \n
        """
        if t.check_instance(rh):
            self.rh = rh
            self.rh_log = rh_log
            self.productname = "ERA5 Relative humidity Hourly 0.25 degree"
            self.productpath = product_path
            self.vectorpath = vector_path
            self.common_elements = self.rh.indatabase
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
            raise TypeError('rh must be HidroCLVariable object')

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

Relative humidity records: {len(self.rh.indatabase)}.
Relative humidity path: {self.rh.database}
                '''

    def run_extraction(self, scene=None, limit=None):
        """
        Run the extraction of the product.
        If limit is None, all scenes will be processed.
        If limit is a number, only the first limit scenes will be processed.

        Args:
            scene (str): scene name
            limit (int): length of the scenes_to_process

        Returns:
            str: Print
        """

        with t.HiddenPrints():
            self.rh.checkdatabase()

        self.common_elements = self.rh.indatabase

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, "era5")

        if scene is not None:
            if scene in self.scenes_to_process:
                self.scenes_to_process = [scene]
            else:
                print(f'{scene} not in the scenes to process. Please, check the scene name.')
                return

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        with TemporaryDirectory() as tempdirname:
            temp_dir = Path(tempdirname)

            if limit is not None:
                scenes_to_process = self.scenes_to_process[:limit]
            else:
                scenes_to_process = self.scenes_to_process

            for scene in scenes_to_process:
                if scene not in self.rh.indatabase:
                    e.zonal_stats(scene, scenes_path,
                                  temp_dir, 'rh_era5',
                                  self.rh.catchment_names, self.rh_log,
                                  database=self.rh.database,
                                  pcdatabase=self.rh.pcdatabase,
                                  vector_path=self.vectorpath,
                                  layer="rh")

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
            self.rh.checkdatabase()

        self.common_elements = self.rh.indatabase

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
    - gh: Isotherm geopotential height
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
        db_log (str): Log file path for variable data \n
        variable (str): Variable name \n
        productname (str): Name of the remote sensing product to be processed \n
        productpath (str): Path to the product folder where the product files are located \n
        vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
        product_files (list): List of product files in the product folder \n
        product_ids (list): List of product ids. Each product id is str with common tag by date \n
        all_scenes (list): List of all scenes (no matter the product id here) \n
        scenes_occurrences (list): List of scenes occurrences for each product id \n
        overpopulated_scenes (list): List of overpopulated scenes (more than 1 scene for era5) \n
        complete_scenes (list): List of complete scenes (1 scene for era5) \n
        incomplete_scenes (list): List of incomplete scenes (less than 1 scene for era5) \n
        scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
    """

    def __init__(self, db0, db1, db2, db3, db4,
                 db_log, variable, aggregation,
                 product_path, vectorpath,
                 prec_threshold=1):
        """
        Examples:

        Args:
            db0 (HidroCLVariable): HidroCLVariable object with GFS variable (see avobe) \n
            db1 (HidroCLVariable): HidroCLVariable object with GFS variable (see avobe) \n
            db2 (HidroCLVariable): HidroCLVariable object with GFS variable (see avobe) \n
            db3 (HidroCLVariable): HidroCLVariable object with GFS variable (see avobe) \n
            db4 (HidroCLVariable): HidroCLVariable object with GFS variable (see avobe) \n
            db_log (str): Log file path for extracted data \n
            variable (str): Variable name \n
            aggregation (str): Aggregation type \n
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
            self.prec_threshold = prec_threshold
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
                              days=days,
                              prec_threshold=self.prec_threshold)

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
            self.db0.checkdatabase()
            self.db1.checkdatabase()
            self.db2.checkdatabase()
            self.db3.checkdatabase()
            self.db4.checkdatabase()

        self.common_elements = t.compare_indatabase(self.db0.database,
                                                    self.db1.database,
                                                    self.db2.database,
                                                    self.db3.database,
                                                    self.db4.database)

        self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, "gfs")

        scenes_path = t.get_scenes_path(self.product_files, self.productpath)

        if limit is not None:
            scenes_to_process = self.scenes_to_process[:limit]
        else:
            scenes_to_process = self.scenes_to_process

        for scene in scenes_to_process:
            m.file_maintainer(scene=scene,
                              scenes_path=scenes_path,
                              name='gfs',
                              log_file=log_file)

# """
# Extraction of CSR GRACE and GRACE-FO MASCON RL06Mv2 data product:
# """
#
#
# class Grace:
#     """
#     A class to process GRACE-FO MASCON to hidrocl variables. Where:\n
#
#     liquid water equivalent thickness: lwe_thickness -> lwe (10 * cm) mean \n
#
#     lwe: HidroCLVariable object with Grace data \n
#
#     Attributes:
#         lwe (HidroCLVariable): HidroCLVariable object with GRACE liquid water equivalent thickness data \n
#         lwe_log (str): Log file path for liquid water equivalent thickness data \n
#         productname (str): Name of the remote sensing product to be processed \n
#         productpath (str): Path to the product folder where the product files are located \n
#         vectorpath (str): Path to the vector folder with Shapefile with areas to be processed \n
#         common_elements (list): List of common elements / this case the same elements \n
#         product_files (list): List of product files in the product folder \n
#         product_ids (list): List of product ids. Each product id is str with common tag by date \n
#         all_scenes (list): List of all scenes (no matter the product id here) \n
#         scenes_occurrences (list): List of scenes occurrences for each product id \n
#         overpopulated_scenes (list): List of overpopulated scenes (more than 1 scene for grace) \n
#         complete_scenes (list): List of complete scenes (1 scene for grace) \n
#         incomplete_scenes (list): List of incomplete scenes (less than 1 scene for grace) \n
#         scenes_to_process (list): List of scenes to process (complete scenes no processed) \n
#     """
#
#     def __init__(self, lwe, product_path, vector_path, lwe_log):
#         """
#         Examples:
#             >>> from hidrocl import HidroCLVariable
#             >>> from hidrocl import Grace
#             >>> lwe = HidroCLVariable('lwe', lwe.db, lwepc.db)
#             >>> product_path = '/home/user/grace'
#             >>> vector_path = '/home/user/shapefiles'
#             >>> lwe_log = '/home/user/lwe.log'
#             >>> grace = Grace(lwe, product_path, vector_path, lwe_log)
#             >>> grace
#             "Class to extract GRACE-FO MASCON RL06Mv2"
#             >>> grace.run_extraction()
#
#
#         Args:
#             lwe (HidroCLVariable): HidroCLVariable object with GRACE liquid water equivalent thickness data \n
#             product_path (str): Path to the product folder where the product files are located \n
#             vector_path (str): Path to the vector folder with Shapefile with areas to be processed \n
#             lwe_log (str): Log file path for liquid water equivalent thickness data \n
#
#         Raises:
#             TypeError: If lwe is not HidroCLVariable object \n
#         """
#         if t.check_instance(lwe):
#             self.lwe = lwe
#             self.lwe_log = lwe_log
#             self.productname = "GRACE-FO MASCON RL06Mv2"
#             self.productpath = product_path
#             self.vectorpath = vector_path
#             self.common_elements = self.lwe.indatabase
#             self.product_files = t.read_product_files(self.productpath, "grace")
#             self.product_ids = t.get_product_ids(self.product_files, "grace")
#             self.all_scenes = t.check_product_files(self.product_ids)
#             self.scenes_occurrences = t.count_scenes_occurrences(self.all_scenes, self.product_ids)
#             (self.overpopulated_scenes,
#              self.complete_scenes,
#              self.incomplete_scenes) = t.classify_occurrences(self.scenes_occurrences, "grace")
#             self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes,
#                                                             self.common_elements, what="grace")
#         else:
#             raise TypeError('lwe must be HidroCLVariable object')
#
#     def __repr__(self):
#         """
#         Return a string representation of the object
#
#         Returns:
#              str: String representation of the object
#         """
#         return f'Class to extract {self.productname}'
#
#     def __str__(self):
#         """
#         Return a string representation of the object
#
#         Returns:
#             str: String representation of the object
#         """
#         return f'''
# Product: {self.productname}
#
# Liquid water equivalent thickness records: {len(self.lwe.indatabase)}.
# Liquid water equivalent thickness path: {self.lwe.database}
#                 '''
#
#     def run_extraction(self, limit=None):
#         """
#         Run the extraction of the product.
#         If limit is None, all scenes will be processed.
#         If limit is a number, only the first limit scenes will be processed.
#
#         Args:
#             limit (int): length of the scenes_to_process
#
#         Returns:
#             str: Print
#         """
#
#         with t.HiddenPrints():
#             self.lwe.checkdatabase()
#
#         self.common_elements = self.lwe.indatabase
#
#         self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, "grace")
#
#         scenes_path = t.get_scenes_path(self.product_files, self.productpath)
#
#         with TemporaryDirectory() as tempdirname:
#             temp_dir = Path(tempdirname)
#
#             if limit is not None:
#                 scenes_to_process = self.scenes_to_process[:limit]
#             else:
#                 scenes_to_process = self.scenes_to_process
#
#             for scene in scenes_to_process:
#                 if scene not in self.lwe.indatabase:
#                     e.zonal_stats(scene, scenes_path,
#                                   temp_dir, 'z_era5',
#                                   self.z.catchment_names, self.z_log,
#                                   database=self.z.database,
#                                   pcdatabase=self.z.pcdatabase,
#                                   vector_path=self.vectorpath,
#                                   layer="z")
#
#     def run_maintainer(self, log_file, limit=None):
#         """
#         Run file maintainer. It will remove any file with problems
#
#         Args:
#             log_file (str): log file path
#             limit (int): length of the scenes_to_process
#
#         Returns:
#             str: Print
#         """
#
#         with t.HiddenPrints():
#             self.z.checkdatabase()
#
#         self.common_elements = self.z.indatabase
#
#         self.scenes_to_process = t.get_scenes_out_of_db(self.complete_scenes, self.common_elements, "era5")
#
#         scenes_path = t.get_scenes_path(self.product_files, self.productpath)
#
#         if limit is not None:
#             scenes_to_process = self.scenes_to_process[:limit]
#         else:
#             scenes_to_process = self.scenes_to_process
#
#         for scene in scenes_to_process:
#             m.file_maintainer(scene=scene,
#                               scenes_path=scenes_path,
#                               name='era5',
#                               log_file=log_file)
