# coding=utf-8

import os
import pandas as pd


def checkdatabase(database, catchment_names=None):
    """check database"""

    if os.path.exists(database):  # check if db exists
        print('Database found, using ' + database)
        observations = pd.read_csv(database)
        observations.date = pd.to_datetime(observations.date, format='%Y-%m-%d')
        observations.set_index(['date'], inplace=True)
        return observations
    else:  # create db
        if catchment_names is None:
            print('Database not found. Please, add catchment names before creating the database')
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
    """Get catchment name"""
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