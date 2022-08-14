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
import plotly.express as px
import plotly.io as pio

# just some formatting options
# allows us to see all columns for a dataframe 
# and numbers aren't displayed in scientific format (4 decimal places)
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:.4f}'.format

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

# that's our clean dataset complete, we can start some EDA
# any other manipulations, we can do specifically during the EDA
# we'll keep this as our base dataset

#--------------------------------------------------------------------------
# EDA
#--------------------------------------------------------------------------

#---------
# what is the split of Type?
#---------
type_split = dataset.groupby('type').\
              agg({'show_id': pd.Series.nunique}).\
              reset_index().\
              rename(columns = {'show_id': 'shows'})
type_split['percent'] = type_split['shows'] / type_split['shows'].sum()
type_split['percent_viz'] = round(type_split['percent'] * 100).astype(str)
type_split['percent_viz'] = type_split['percent_viz'].\
                            str.split('.', expand = True)[0].astype(str) + '%'

type_split_viz = px.bar(
  type_split,
  x = 'type', y = 'percent',
  text = 'percent_viz',
  title = 'Movies vs T-Shows',
  labels = {
    'percent': '% of Shows',
    'type': 'Type',
  },
  color = 'type'
  )
type_split_viz.update_traces(
  textfont_size = 12, 
  textangle = 0, 
  textposition = 'outside', 
  cliponaxis = False
  )
type_split_viz.layout.yaxis.tickformat = ',.0%'
# type_split_viz.show()
type_split_viz.write_image('type_split.png', 
  scale = 1, width = 800, height = 1000)

#---------
# No. of Shows by Country
#---------
# multiple countries can be within one row (seperated by ',')
# so we will need to do some data manipulation
# first we make a copy of our dataset, with two columns
shows_country = dataset[['show_id', 'country']].copy()
# this will split out countries into individual columns
country_columns = shows_country['country'].str.split(',', expand = True).\
                  apply(lambda x: x.str.strip())
# we will now concat to our shows_country dataframe
shows_country = pd.concat([shows_country, country_columns], axis = 1, \
                join = 'outer')
# we'll check if the split has been successful
shows_country[shows_country['country'].str.contains(',', na = False)]
# the split is successful, so we'll drop the country column
shows_country.drop(columns = 'country', inplace = True)
# we'll now re-arrange the dataframe from wide to long
# we'll also remove nulls and duplicates
shows_country = pd.melt(shows_country, id_vars = ['show_id']).\
                drop(columns = 'variable').dropna().\
                rename({'value': 'country'}, axis = 'columns')
# we'll now group the dataset
shows_country = shows_country.groupby(['country']).\
                agg({'show_id': pd.Series.nunique}).\
                rename(columns = {'show_id': 'shows'}).\
                sort_values('shows', ascending = False).\
                reset_index()
shows_country['percent'] = shows_country['shows'] / shows_country['shows'].sum()
shows_country['percent_viz'] = round(shows_country['percent'] * 100).astype(str)
shows_country['percent_viz'] = shows_country['percent_viz'].\
                            str.split('.', expand = True)[0].astype(str) + '%'
shows_country = shows_country.iloc[0:10]

shows_country_viz = px.bar(
  shows_country,
  x = 'country', y = 'shows',
  text = 'percent_viz',
  title = 'Shows per Country (Top 10)',
  labels = {
    'shows': 'No. of Shows',
    'country': 'Country',
  },
  color = 'shows'
)
shows_country_viz.update_traces(
  textfont_size = 12, 
  textangle = 0, 
  textposition = 'outside', 
  cliponaxis = False
)
shows_country_viz.show()
shows_country_viz.write_image('shows_country.png', 
  scale = 1, width = 800, height = 1000)


#---------
# Movie Durations
#---------
# over here we will look at the number of minutes per Movie by genre
movie_duration = dataset[dataset['type'] == 'Movie']\
                  [['show_id', 'title', 'listed_in', 'duration_minutes']].\
                  reset_index(drop = True).copy()
# There are multiple genre's for a single film, so we'll split these out
# this will split out genres into individual columns
genres = movie_duration['listed_in'].str.split(',', expand = True).\
          apply(lambda x: x.str.strip())
# we will now concat to our movie_duration dataframe
movie_duration = pd.concat([movie_duration, genres], axis = 1, join = 'outer')
# the split is successful, so we'll drop the listed_in column
movie_duration.drop(columns = 'listed_in', inplace = True)
# we'll now re-arrange the dataframe from wide to long
# we'll also remove nulls and duplicates
movie_duration = pd.melt(movie_duration,\
                  id_vars = ['show_id', 'title', 'duration_minutes']).\
                  drop(columns = 'variable').dropna().\
                  rename({'value': 'genre'}, axis = 'columns')
# we need to convert duration_minutes from string to int
movie_duration['duration_minutes'] = movie_duration['duration_minutes'].astype(int)

movie_duration_viz = px.box(
  movie_duration,
  x = 'genre', y = 'duration_minutes',
  title = 'Movie Duration by Genre',
  labels = {
    'duration_minutes': 'Minutes',
    'genre': 'Genre',
  },
  color = 'genre'
)
movie_duration_viz.show()
movie_duration_viz.write_image('movie_duration.png', 
  scale = 1, width = 800, height = 1000)