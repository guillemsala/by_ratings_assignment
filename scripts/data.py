# Classical data science toolbox
import pandas as pd
import numpy as np
import datetime as dt
# Path and direction mgmt packages
import pathlib, glob, os

def get_data_dict() -> dict :

    # Generate data dictionary, whose
    # * keys are filenames without the .csv extension
    # * values are the files stored in a pd.DataFrame object

    # Get project directory
    proj_dir = str(pathlib.Path().resolve().cwd().parent)
    # Get the dir where data is stored
    data_dir = proj_dir + '/data/nsds'
    # Make data dict
    data_dict = {
        # Remove the .csv extension, and read csv into pd.DataFrame object,
        # also get rid of the first "nsds_" part.
        os.path.basename(file).replace('.csv', '').split('_')[-1] : pd.read_csv(file)
        for file in glob.glob(data_dir + '/*.csv')
    }
    # Return
    return data_dict

def get_clean_data_dict() -> dict :

    # Perform cleaning on data_dict following ./notebooks/eda.ipynb
    data_dict = get_data_dict()

    # And store in separate data-frames
    purchases = data_dict['purchases']
    users = data_dict['users']

    # Fix dates
    purchases['purchased_at'] = pd.to_datetime(purchases.purchased_at)
    users['created_at'] = pd.to_datetime(users.created_at)

    # Fix users df following notebook
    users.loc[
        (users.created_at.dt.date >= dt.date.today()) | (users.created_at.dt.date < dt.date(year = 1930, month = 1, day = 1)),
        'created_at'
    ] = np.nan
    users.loc[
        # A user should have less than 100 years...and more than 16
        (users.birthyear <= 1915) | (users.birthyear >= 2006),
        'birthyear'
    ] = np.nan

    # Return clean dictionary
    return {
        'users' : users,
        'purchases' : purchases
    }