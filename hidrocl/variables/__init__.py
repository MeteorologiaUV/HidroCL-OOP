# coding=utf-8

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from . import methods


class HidroCLVariable:
    """A class to hold information about a hidrocl variable

    Attributes
    ----------
    name : str
        Name of the variable
    database : str
        Path to the database
    pcdatabase : str
        Path to the database with pixel count
    indatabase : list
        List of IDs in the database
    observations : pandas.DataFrame
        Dataframe with the observations
    pcobservations : pandas.DataFrame
        Dataframe with the pixel count
    catchment_names : list
        List of catchment names
    """

    def __init__(self, name, database, pcdatabase):
        """
        Parameters
        ----------
        :param name: str
            Name of the variable
        :param database: str
            Path to the database
        :param pcdatabase: str
            Path to the database with pixel count
        """
        self.name = name
        self.database = database
        self.pcdatabase = pcdatabase
        self.indatabase = ''
        self.observations = None
        self.pcobservations = None
        self.catchment_names = None
        self.checkdatabase()
        self.checkpcdatabase()

    def __repr__(self):
        """
        Representation of the object
        :return: str
        """
        return f'Variable: {self.name}. Records: {len(self.indatabase)}'

    def __str__(self):
        """
        String representation of the object
        :return: str
        """
        return f'''
Variable {self.name}.
Records: {len(self.indatabase)}.
Database path: {self.database}.
Pixel count database path: {self.pcdatabase}.
        '''

    def checkindatabase(self):
        """
        Check IDs in database
        :return: list
        """
        if self.observations is None:
            print('Please, check the database for getting the IDs processed')
            return ''
        else:
            return self.observations[self.observations.columns[0]].values.tolist()

    def checkdatabase(self):
        """
        Check database

        :return: pandas.DataFrame
        """
        self.observations = methods.checkdatabase(self.database, self.catchment_names)
        self.indatabase = self.checkindatabase()
        try:
            self.catchment_names = self.observations.columns[1:].tolist()
        except AttributeError:
            print('Could not load dataframe, perhaps the database has not been created yet')

    def checkpcdatabase(self):
        """
        Check database with pixel count

        :return: pandas.DataFrame
        """
        self.pcobservations = methods.checkdatabase(self.pcdatabase, self.catchment_names)

    def add_catchment_names(self, catchment_names_list):
        """
        Add catchment names to the variable using cathment_names from database

        :param catchment_names_list: list of catchment names
        :return: None
        """
        if self.catchment_names is None:
            if catchment_names_list is not None:
                self.catchment_names = catchment_names_list
                print('Catchment names added. I recommend you to check the database')
            else:
                print("Catchments names can't be None type")
        else:
            print('Catchment names already added!')

    def valid_data(self):
        """
        Return valid data for all catchments

        :return: list with valid data with date index
        """
        return self.observations.notnull().sum()[1:]

    def plot_valid_data_all(self):
        """
        Plot valid data for all catchments

        :return: plot with valid data for all catchments with date index
        """
        df = self.observations.drop(self.observations.columns[0], axis=1).notnull().sum().divide(
            len(self.observations.index)).multiply(100)
        ax = df.plot(title='Valid observations by catchment', ylim=(0, 105), color='lightseagreen')
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        plt.show()

    def plot_valid_data_individual(self, catchment):
        """
        Plot valid data for individual catchments
        :param catchment: str (catchment name) or int (catchment index)
        :return: plot with valid data for individual catchments with date index
        """

        catchment = methods.get_catchment_name(catchment, self.catchment_names)
        methods.plot_variable(catchment, self.observations, what='valid')

    def plot_pixel_count(self, catchment):
        """
        Plot pixel count for individual catchments

        :param catchment: str (catchment name) or int (catchment index)
        :return: plot with pixel count for individual catchments with date index
        """

        catchment = methods.get_catchment_name(catchment, self.catchment_names)
        methods.plot_variable(catchment, self.pcobservations, what='count')

