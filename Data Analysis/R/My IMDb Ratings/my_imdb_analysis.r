#--------------------------------------------------------------------------
# set working directory
#--------------------------------------------------------------------------
setwd('/home/waseem/Documents/Self-Development/git_repos/portfolio/Data Analysis/R/My IMDb Ratings/')


#-----------------------------------------------------------r---------------
# Load libraries
#--------------------------------------------------------------------------
library(data.table)
library(ggplot2)
library(tidyverse)
library(lubridate)
library(gridExtra)


#--------------------------------------------------------------------------
# load dataset
#--------------------------------------------------------------------------

# we'll load the csv from our location
raw_dataset <- data.table(read.csv('ratings.csv', stringsAsFactors = F))


#--------------------------------------------------------------------------
# clean dataset
#--------------------------------------------------------------------------

str(raw_dataset)

dataset <- data.table(
  raw_dataset %>%
    rename(
      film_id = Const,
      my_rating = Your.Rating,
      rated_date = Date.Rated,
      title_type = Title.Type,
      imdb_rating = IMDb.Rating,
      runtime_mins = Runtime..mins.,
      year_of_release = Year,
      number_of_votes = Num.Votes
    ) %>%
    rename_with(tolower) %>%
    mutate(rated_date = ymd(rated_date))
)

str(dataset)


#--------------------------------------------------------------------------
# EDA visualisations
#--------------------------------------------------------------------------


#----------------------------------------------------
# number of films rated by year
#----------------------------------------------------
year_rated <- data.table(
  dataset %>%
    group_by(year_rated = year(rated_date)) %>%
    summarise(films = n_distinct(film_id)) %>%
		mutate(percent = films / sum(films))
)



#----------------------------------------------------
# number of films by decade
#----------------------------------------------------
decade <- data.table(
  dataset %>%
    mutate(decade = make_date(year_of_release,01,01)) %>%
    mutate(decade = floor_date(decade, years(10))) %>%
    group_by(decade) %>%
    summarise(films = n_distinct(film_id)) %>%
		mutate(percent = films / sum(films))
)
