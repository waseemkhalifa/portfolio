#--------------------------------------------------------------------------
# set working directory
#--------------------------------------------------------------------------
setwd("imdb_analysis")


#--------------------------------------------------------------------------
# Load libraries
#--------------------------------------------------------------------------
library(data.table)
library(ggplot2)
library(tidyverse)
library(lubridate)
library(gridExtra)
library(stringr)


#--------------------------------------------------------------------------
# Custom functions / variables
#--------------------------------------------------------------------------
fn_mode <- function(x){ ux <- unique(x)
  ux[which.max(tabulate(match(x, ux)))] }

viz_export_folder <- "/home/waseem/Documents/Self-Development/git_repos/portfolio/Data Analysis/R/My IMDb Ratings/plots/"


#--------------------------------------------------------------------------
# load dataset
#--------------------------------------------------------------------------

# we"ll load the csv from our location
raw_dataset <- data.table(read.csv("films.csv", stringsAsFactors = F))


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
      box_office = as.double(gsub("\\$|,", "", box_office)),
      released = dmy(released),
      runtime_min = as.integer(gsub(" min", "", runtime_min)),
      imdb_votes = as.integer(gsub(",", "", imdb_votes))
    )
)

str(dataset)


#--------------------------------------------------------------------------
# EDA visualisations
#--------------------------------------------------------------------------
theme_set(theme_classic())

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
		mutate(percent = films / sum(films)) %>%
    arrange(year_rated)
)


year_rated_viz <- year_rated %>%
  ggplot(aes(x=reorder(year_rated, year_rated), y=films)) + 
  
  geom_bar(stat="identity", width=0.8, fill="#000000") +
  
  scale_y_continuous(breaks = seq(0, 280, 10), limits = c(0, 280), 
                      expand = expansion(add=c(0,0))) +
  
  labs(title = "No. of Films Rated Per Year", 

      subtitle = str_wrap("I watched a lot of films during 2006-2010.\n
          This was during my time at 6th Form and University (ah freedom!).\n
          I also had a lovefilm account during this time (Film4 also deserves a worthy mention!),\n
          which opened up a whole new world of films I had never come across before."),

       caption="source: IMDb",
       x = "Year Rated", 
       y = "No. of Films") +
  
  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff"))

ggsave(year_rated_viz, 
      file = paste0(viz_export_folder, "films_by_year_rated.png"),
      width = 9.25, height = 5, units = 'in')


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


decade_viz <- decade %>%
  ggplot(aes(x=reorder(decade, decade), y=films)) + 
  
  geom_bar(stat="identity", width=0.8, fill="#000000") +
  
  scale_y_continuous(breaks = seq(0, 400, 15), limits = c(0, 400), 
                      expand = expansion(add=c(0,0))) +
  
  labs(title = "No. of Films Rated Based on Release Decade", 

      subtitle = str_wrap("Most of the films I've watched are from the 90s to 2010s. \n
                          I clearly need to catch up on some 80s classics!"),

       caption="source: IMDb",
       x = "Decade Film was released in", 
       y = "No. of Films") +
  
  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff"))

ggsave(decade_viz, 
      file = paste0(viz_export_folder, "films_by_decade.png"),
      width = 9.25, height = 5, units = 'in')


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


director_viz <- director %>%
  ggplot(aes(x=reorder(director, films), y=films)) + 

  geom_point(size=5) +
  
  geom_segment(aes(x=director, xend=director, y=0, yend=films)) + 
  
  scale_y_continuous(breaks = seq(0, 18, 1), limits = c(0, 18), 
                      expand = expansion(add=c(0,0))) +
  
  labs(title = "No. of Films by Director", 

      subtitle = str_wrap("I watched a lot of films during 2006-2010.\n
          This was during my time at 6th Form and University (ah freedom!).\n
          I also had a lovefilm account during this time (Film4 also deserves a worthy mention!),\n
          which opened up a whole new world of films I had never come across before."),

       caption="source: IMDb",
       x = "Directors", 
       y = "No. of Films") +
  
  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff")) +
  coord_flip()

ggsave(director_viz, 
      file = paste0(viz_export_folder, "films_by_director.png"),
      width = 9.25, height = 5, units = 'in')


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

director_viz <- genre %>%
  ggplot(aes(x=reorder(genre, films), y=films)) + 

  geom_point(size=5) +
  
  geom_segment(aes(x=genre, xend=genre, y=0, yend=films)) + 
  
  scale_y_continuous(breaks = seq(0, 575, 10), limits = c(0, 575), 
                      expand = expansion(add=c(0,0))) +
  
  labs(title = "No. of Films by Genre", 

      subtitle = str_wrap("I watched a lot of films during 2006-2010.\n
          This was during my time at 6th Form and University (ah freedom!).\n
          I also had a lovefilm account during this time (Film4 also deserves a worthy mention!),\n
          which opened up a whole new world of films I had never come across before."),

       caption="source: IMDb",
       x = "Genres", 
       y = "No. of Films") +
  
  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff"),
        axis.text.x = element_text(angle = 90)) +
  coord_flip()

ggsave(director_viz, 
      file = paste0(viz_export_folder, "films_by_genre.png"),
      width = 9.25, height = 5, units = 'in')

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
	ggtitle("Runtime (Minutes)") +
	labs(y = "Minutes") +
	scale_y_continuous(breaks = seq(40, 200, 10), limits = c(40, 200))


runtime_hist <- data.table(
  dataset %>%
    select(film_id, title, runtime_min)
) %>%
  ggplot(aes(x = runtime_min)) +
	geom_histogram(binwidth = 5, colour = "#000000", fill = "#f2db83") + 
	ggtitle("Runtime (Minutes)") +
	labs(y = "No. of Films", x = "Minutes") +
	scale_x_continuous(breaks = seq(40, 200, 5), lim = c(40, 200)) +
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

#----------------------------------------------------
# films by writers
#----------------------------------------------------
writer <- data.table(
  dataset %>%
    filter(writer != "") %>%
    group_by(writer) %>%
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
# films by actors
#----------------------------------------------------
actors <- data.table(
  dataset %>%
    filter(actors != "") %>%
    select(film_id, title, actors, my_rating) %>%
    mutate(actors = strsplit(as.character(actors), ", ")) %>% 
    unnest(actors) %>%
    unique() %>%
    group_by(actors) %>%
    summarise(films = n_distinct(film_id),
              rating_avg = round(mean(my_rating),2),
              rating_median = median(my_rating),
              rating_mode = fn_mode(my_rating) 
            ) %>%
		mutate(percent = films / sum(films)) %>%
    arrange(-films) %>%
    filter(films >= 9)
)

#----------------------------------------------------
# films by actors
#----------------------------------------------------
actors <- data.table(
  dataset %>%
    filter(actors != "") %>%
    select(film_id, title, actors, my_rating) %>%
    mutate(actors = strsplit(as.character(actors), ", ")) %>% 
    unnest(actors) %>%
    unique() %>%
    group_by(actors) %>%
    summarise(films = n_distinct(film_id),
              rating_avg = round(mean(my_rating),2),
              rating_median = median(my_rating),
              rating_mode = fn_mode(my_rating) 
            ) %>%
		mutate(percent = films / sum(films)) %>%
    arrange(-films) %>%
    filter(films >= 9)
)


#----------------------------------------------------
# films by imdb_rating
#----------------------------------------------------
imdb_rating_hist <- data.table(
  dataset %>%
    select(film_id, title, imdb_rating)
) %>%
  ggplot(aes(x = imdb_rating)) +
	geom_histogram(binwidth = 0.25, colour = "#000000", fill = "#f2db83") + 
	ggtitle("Films by IMDB Rating") +
	labs(y = "No. of Films", x = "IMDB Rating") +
	scale_x_continuous(breaks = seq(2.25, 9.75, 0.25), lim = c(2.25, 9.75)) +
	scale_y_continuous(labels = scales::comma, breaks = seq(0, 200, 5)) +
  theme(axis.text.x = element_text(angle = 90))


#----------------------------------------------------
# films by imdb_votes
#----------------------------------------------------
imdb_votes_box <- data.table(
  dataset %>%
    select(film_id, title, imdb_votes)
) %>%
  ggplot(aes(y = imdb_votes)) +
	geom_boxplot() +
	ggtitle("Films by IMDB Votes") +
	labs(y = "IMDB Votes") +
	scale_y_continuous(breaks = seq(0, 850000, 50000), limits = c(0, 850000))


imdb_votes_hist <- data.table(
  dataset %>%
    select(film_id, title, imdb_votes)
) %>%
  ggplot(aes(x = imdb_votes)) +
  geom_histogram(binwidth = 10000, colour = "#000000", fill = "#dba506") + 
  ggtitle("Films by IMDB Votes") +
  labs(y = "No. of Films", x = "IMDB Votes") +
  scale_x_continuous(breaks = seq(0, 850000, 10000), lim = c(0, 850000)) +
  scale_y_continuous(labels = scales::comma, breaks = seq(0, 65, 5)) +
  theme(axis.text.x = element_text(angle = 90))



