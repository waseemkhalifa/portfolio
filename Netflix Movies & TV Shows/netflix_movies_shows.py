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
# first we'll seperate out day, month and year
dataset['month'] = dataset['date_added'].str.split(' ', expand = True)[0].\
                    str.strip()
dataset['day'] = dataset['date_added'].str.split(' ', expand = True)[1].\
                  str.split(',', expand = True)[0].str.zfill(2)
dataset['year'] = dataset['date_added'].str.split(',', expand = True)[1].\
                  str.strip()
# we'll create the new data_added column now
dataset['date_added'] = pd.to_datetime(dataset[['year', 'month', 'day']].\
                        astype(str).apply(''.join, 1), format = '%Y%B%d',\
                        errors = 'coerce')

# we'll see the unique values in the duration column
# we want to see if it only holding min or seasons
dataset['duration'].unique()
# it's only holding min or seasons, let's feature engineer seasons and mins
# we'll create a custom functions which will help us achieve this
# this function checks if the column contains 'min', if it does
# it extracts the minutes
def udf_minutes(var1):
  if 'min' in str(var1).lower():
    return str(var1).split(' ')[0].strip()
# we'll derive minutes using our function in lambda
dataset['duration_minutes'] = dataset['duration'].apply(lambda x: \
                              udf_minutes(x))
# this function checks if the column contains 'seasons', if it does
# it extracts the seasons
def udf_seasons(var1):
  if 'seasons' in str(var1).lower():
    return str(var1).split(' ')[0].strip()
# we'll derive minutes using our function in lambda
dataset['duration_seasons'] = dataset['duration'].apply(lambda x: \
                              udf_seasons(x))
