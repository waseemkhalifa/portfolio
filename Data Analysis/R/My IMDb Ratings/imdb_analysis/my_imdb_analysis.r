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
    rename(
      runtime_min = runtime,
      year_of_release = year
      ) %>%
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
    mutate(decade = year(decade)) %>%
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
    filter(director != "") %>%
    group_by(director) %>%
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
    filter(genre != "") %>%
    select(film_id, title, genre, my_rating) %>%
    mutate(genre = strsplit(as.character(genre), ", ")) %>% 
    unnest(genre) %>%
    unique() %>%
    group_by(genre) %>%
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
# films by run time
#----------------------------------------------------
runtime_box <- data.table(
  dataset %>%
    select(film_id, title, runtime_min)
) %>%
  ggplot(aes(y = runtime_min)) +
	geom_boxplot() +
	ggtitle('Runtime (Minutes)') +
	labs(y = 'Minutes') +
	scale_y_continuous(breaks = seq(40, 200, 10), limits = c(40, 200))


runtime_hist <- data.table(
  dataset %>%
    select(film_id, title, runtime_min)
) %>%
  ggplot(aes(x = runtime_min)) +
	geom_histogram(binwidth = 5, colour = 'black', fill = 'steelblue') + 
	ggtitle('Runtime (Minutes)') +
	labs(y = 'No. of Films', x = 'Minutes') +
	scale_x_continuous(breaks = seq(40, 200, 5), lim = c(40, 200)) +
	# xlim(0, 200) +
	scale_y_continuous(labels = scales::comma)



#----------------------------------------------------
# films by language
#----------------------------------------------------
language <- data.table(
  dataset %>%
    filter(language != "") %>%
    select(film_id, title, language, my_rating) %>%
    mutate(language = map(strsplit(language, split = ","), 1)) %>% 
    unnest(language) %>%
    unique() %>%
    group_by(language) %>%
    summarise(films = n_distinct(film_id),
              rating_avg = round(mean(my_rating),2),
              rating_median = median(my_rating),
              rating_mode = fn_mode(my_rating) 
            ) %>%
		mutate(percent = films / sum(films)) %>%
    arrange(-films) %>%
    filter(films >= 3)
)


#----------------------------------------------------
# films by country
#----------------------------------------------------
country <- data.table(
  dataset %>%
    filter(country != "") %>%
    select(film_id, title, country, my_rating) %>%
    mutate(country = map(strsplit(country, split = ","), 1)) %>% 
    unnest(country) %>%
    unique() %>%
    group_by(country) %>%
    summarise(films = n_distinct(film_id),
              rating_avg = round(mean(my_rating),2),
              rating_median = median(my_rating),
              rating_mode = fn_mode(my_rating) 
            ) %>%
		mutate(percent = films / sum(films)) %>%
    arrange(-films) %>%
    filter(films >= 3)
)

