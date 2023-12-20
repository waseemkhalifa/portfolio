#--------------------------------------------------------------------------
# set working directory
#--------------------------------------------------------------------------
setwd('imdb_analysis')


#--------------------------------------------------------------------------
# Load libraries
#--------------------------------------------------------------------------
library(data.table)
library(ggplot2)
library(tidyverse)
library(lubridate)
library(gridExtra)


#--------------------------------------------------------------------------
# Custom functions
#--------------------------------------------------------------------------
fn_mode <- function(x){ ux <- unique(x)
  ux[which.max(tabulate(match(x, ux)))] }


#--------------------------------------------------------------------------
# load dataset
#--------------------------------------------------------------------------

# we'll load the csv from our location
raw_dataset <- data.table(read.csv('films.csv', stringsAsFactors = F))


#--------------------------------------------------------------------------
# clean dataset
#--------------------------------------------------------------------------

str(raw_dataset)

dataset <- data.table(
  raw_dataset %>%
    rename(runtime_min = runtime) %>%
    mutate(
      rated_date = ymd(rated_date),
      box_office = as.double(gsub("\\$|,", '', box_office)),
      released = dmy(released),
      runtime_min = as.integer(gsub(" min", '', runtime_min)),
    )
)

str(dataset)


#--------------------------------------------------------------------------
# EDA visualisations
#--------------------------------------------------------------------------


#----------------------------------------------------
# films rated by year
#----------------------------------------------------
year_rated <- data.table(
  dataset %>%
    group_by(year_rated = year(rated_date)) %>%
    summarise(films = n_distinct(film_id),
              rating_avg = round(mean(my_rating),2),
              rating_median = median(my_rating),
              rating_mode = fn_mode(my_rating) 
            ) %>%
		mutate(percent = films / sum(films))
)


#----------------------------------------------------
# films by decade
#----------------------------------------------------
decade <- data.table(
  dataset %>%
    mutate(decade = make_date(year_of_release,01,01)) %>%
    mutate(decade = floor_date(decade, years(10))) %>%
    group_by(decade) %>%
    summarise(films = n_distinct(film_id),
              rating_avg = round(mean(my_rating),2),
              rating_median = median(my_rating),
              rating_mode = fn_mode(my_rating) 
            ) %>%
		mutate(percent = films / sum(films))
)


#----------------------------------------------------
# films by director
#----------------------------------------------------
director <- data.table(
  dataset %>%
    filter(directors != "") %>%
    group_by(directors) %>%
    summarise(films = n_distinct(film_id),
              rating_avg = round(mean(my_rating),2),
              rating_median = median(my_rating),
              rating_mode = fn_mode(my_rating) 
            ) %>%
		mutate(percent = films / sum(films)) %>%
    arrange(-films) %>%
    filter(films >= 5)
)


#----------------------------------------------------
# films by genre
#----------------------------------------------------
genre <- data.table(
  dataset %>%
    filter(genres != "") %>%
    select(film_id, title, genres, my_rating) %>%
    mutate(genres = strsplit(as.character(genres), ", ")) %>% 
    unnest(genres) %>%
    unique() %>%
    group_by(genres) %>%
    summarise(films = n_distinct(film_id),
              rating_avg = round(mean(my_rating),2),
              rating_median = median(my_rating),
              rating_mode = fn_mode(my_rating) 
            ) %>%
		mutate(percent = films / sum(films)) %>%
    arrange(-films)
)


#----------------------------------------------------
# films by rating
#----------------------------------------------------
rating <- data.table(
  dataset %>%
    filter(my_rating != "") %>%
    group_by(my_rating) %>%
    summarise(films = n_distinct(film_id)) %>%
		mutate(percent = films / sum(films)) %>%
    arrange(-films)
)


#----------------------------------------------------
# films by director
#----------------------------------------------------
director <- data.table(
  dataset %>%
    filter(directors != "") %>%
    group_by(directors) %>%
    summarise(films = n_distinct(film_id),
              rating_avg = round(mean(my_rating),2),
              rating_median = median(my_rating),
              rating_mode = fn_mode(my_rating) 
            ) %>%
		mutate(percent = films / sum(films)) %>%
    arrange(-films) %>%
    filter(films >= 5)
)


#----------------------------------------------------
# films by run time
#----------------------------------------------------
runtime_box <- data.table(
  dataset %>%
    select(film_id, title, runtime_mins)
) %>%
  ggplot(aes(y = runtime_mins)) +
	geom_boxplot() +
	ggtitle('Runtime (Minutes)') +
	labs(y = 'Minutes') +
	scale_y_continuous(breaks = seq(40, 200, 10), limits = c(40, 200))


runtime_hist <- data.table(
  dataset %>%
    select(film_id, title, runtime_mins)
) %>%
  ggplot(aes(x = runtime_mins)) +
	geom_histogram(binwidth = 5, colour = 'black', fill = 'steelblue') + 
	ggtitle('Runtime (Minutes)') +
	labs(y = 'No. of Films', x = 'Minutes') +
	scale_x_continuous(breaks = seq(0, 200, 5), lim = c(0, 200)) +
	# xlim(0, 200) +
	scale_y_continuous(labels = scales::comma)






