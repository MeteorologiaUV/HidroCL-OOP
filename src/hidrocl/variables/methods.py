# coding=utf-8

import os
import pandas as pd
import matplotlib.pyplot as plt


def checkdatabase(database, catchment_names=None, supportcreation = None):
    """
    Check if the database exists and is valid

    Args:
        database (str): Path to the database
        catchment_names (list): List of catchment names (default is None)
        supportcreation (bool): If True, the function will support the creation of the database (default is None)

    Returns:
        pandas.DataFrame: Dataframe with the observations
    """

    if os.path.exists(database):  # check if db exists
        print('Database found, using ' + database)
        observations = pd.read_csv(database, dtype={'name_id': str})
        observations.date = pd.to_datetime(observations.date, format='%Y-%m-%d')
        observations.set_index(['date'], inplace=True)
        return observations
    else:  # create db
        if catchment_names is None:
            if supportcreation is not None:
                print('Database not found. Please, add catchment names before creating the database')
            else:
                raise ImportError('Database not found. Check filename or create it')


        else:
            print('Database not found, creating it for ' + database)
            header_line = [str(s) for s in catchment_names]
            header_line.insert(0, 'name_id')
            header_line.insert(1, 'date')
            header_line = ','.join(header_line) + '\n'
            with open(database, 'w') as the_file:
                the_file.write(header_line)
            print('Database created!')
            observations = pd.read_csv(database)
            observations.date = pd.to_datetime(observations.date, format='%Y-%m-%d')
            observations.set_index(['date'], inplace=True)
            return observations


def get_catchment_name(catchment, catchment_names):
    """
    Get catchment name from catchment ID

    Args:
        catchment (str or int): Catchment name or ID
        catchment_names (list): List of catchment names

    Returns:
        str: Catchment name
    """
    match catchment:
        case str():
            if catchment in catchment_names:
                return catchment
            else:
                print('Catchment not found')
                return
        case int():
            if catchment < len(catchment_names):
                return catchment_names[catchment]
            else:
                print('Catchment index out of range')
                return
        case _:
            print('Catchment not found')
            return


def plot_variable(catchment, observations, what='valid'):
    """
    Plot variable for a catchment

    Args:
        catchment (str): Catchment name
        observations (pandas.DataFrame): Dataframe with the observations
        what (str): 'valid' or 'all'

    Returns:
        plot
    """

    aim = observations[[catchment]]
    year_ = aim.index.year
    doy_ = aim.index.dayofyear

    match what:
        case 'valid':
            aim = aim.notnull().groupby([year_, doy_]).sum()
            aim = aim.unstack(level=0).transpose()

            plt.imshow(aim, cmap=plt.get_cmap('bwr_r', 2), aspect='equal', vmin=-0.5, vmax=1.5)
            plt.colorbar(ticks=[0, 1], fraction=0.046, pad=0.04).set_ticklabels(['NaN', 'Valid'])

        case 'count':
            aim = aim.groupby([year_, doy_]).mean().div(10)
            aim = aim.unstack(level=0).transpose()

            plt.imshow(aim, cmap=plt.get_cmap('gnuplot_r', 20), aspect='equal', vmin=0, vmax=100)
            plt.colorbar(ticks=[0, 100], fraction=0.046, pad=0.04)

    plt.title(f'Valid observations for catchment ID {catchment}')
    plt.xticks(range(0, len(aim.columns), 3), aim.columns[::3])
    plt.yticks(range(0, len(aim.index), 3), aim.index.get_level_values(1)[::3])

    plt.show()


def plot_variable_all(observations, catchment_names, database, what='obs'):
    """
    Plot variable for a catchment

    Args:
        observations (pandas.DataFrame): Dataframe with the observations
        catchment_names (list): List of catchment names
        database (str): Path to the database
        what (str): 'obs' or 'pc'

    Returns:
        plot
    """

    databasename = database.split('/')[-1]
    len_ = len(catchment_names)
    year_ = observations.index.year
    doy_ = observations.index.dayofyear

    asp = (len(doy_.unique()) + 3) / ((len(year_.unique()) + 3) * 1.5)

    match asp:
        case _ if asp < 0.4:
            asp = 0.4

    match what:
        case 'obs':
            df = observations.notnull().groupby([year_, doy_]).sum().assign(sum=lambda x: x.sum(axis=1))
            df = df["sum"].div(len_).multiply(100).unstack(level=0).transpose()
            message = f'% of valid observations for \n{databasename} by date'
            plt.imshow(df, cmap=plt.get_cmap('rainbow_r', 20), aspect=asp, vmin=0, vmax=100)
            plt.xlabel('Day of year')
            plt.ylabel('Year')
            plt.colorbar(ticks=[0, 100], fraction=0.035, pad=0.04)

        case _:
            df = observations.groupby([year_, doy_]).mean().div(10).assign(mean=lambda x: x.sum(axis=1))
            df = df["mean"].div(len_).unstack(level=0).transpose()
            message = f'% of mean pixel count for \n{databasename} observations by date'
            plt.imshow(df, cmap=plt.get_cmap('gist_ncar_r', 20), aspect=asp, vmin=60, vmax=100)
            plt.xlabel('Day of year')
            plt.ylabel('Year')
            plt.colorbar(ticks=[60, 100], fraction=0.035, pad=0.04)

    plt.title(message)
    plt.xticks(range(0, len(df.columns), len(df.columns)//8), df.columns[::(len(df.columns)//8)])
    plt.yticks(range(0, len(df.index), 3), df.index[::3])

    plt.show()
