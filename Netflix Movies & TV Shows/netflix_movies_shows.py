#--------------------------------------------------------------------------
# Load libraries
#--------------------------------------------------------------------------
# this is to have a coloured syntax in the python terminal within vscode
import sys
from IPython.core.ultratb import ColorTB
sys.excepthook = ColorTB()

# libraries we will load
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from rich import print

# just some formatting options
# allows us to see all columns for a dataframe 
# and numbers aren't displayed in scientific format
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:.2f}'.format

#--------------------------------------------------------------------------
# set Working Directory
#--------------------------------------------------------------------------
os.chdir('/home/waseem/Documents/Self-Development/Netflix Movies & TV Shows')

#--------------------------------------------------------------------------
# import dataset
#--------------------------------------------------------------------------
raw_dataset = pd.read_csv('netflix_titles.csv')

#--------------------------------------------------------------------------
# clean dataset
#--------------------------------------------------------------------------
# we'll create a copy of raw_dataset
# we can revert back to this if we ever make a mistake
# saves us having to re import the data
dataset = raw_dataset.copy()

# this gives us information regarding our dataframe
dataset.info()
# we get the following information
  # we have 8807 rows
  # we have nulls in the following columns
    # director
    # cast
    # country 
    # date_added
    # rating
    # duration
  # we need to change the following columns types
    # release_year from int to string
  # we should feature engineer the following
    # date_added as a date format
    # duration = split out those in seasons and those with minutes

# we'll convert release_year from int to string
dataset['release_year'] = dataset['release_year'].astype(str)

# we'll feature engineer here
# let's create date_added as a date column
# we'll keep the orginal date_added column but rename it
dataset['date_added_orginal'] = dataset['date_added']
# create the new date_added column as string