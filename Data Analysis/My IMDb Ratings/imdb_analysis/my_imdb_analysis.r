#--------------------------------------------------------------------------
# set working directory
#--------------------------------------------------------------------------
setwd("My IMDb Ratings/imdb_analysis")


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

viz_export_folder <- paste0("/home/waseem/Documents/Self-Development/",
                  "git_repos/portfolio/Data Analysis/My IMDb Ratings/plots/")


#--------------------------------------------------------------------------
# load dataset
#--------------------------------------------------------------------------

# we"ll load the csv from our location
raw_dataset <- data.table(read.csv("films.csv", stringsAsFactors = F))

# we"ll load the csv from our location
raw_top_250 <- data.table(read.csv("imdb_top_250_all.csv", 
                          stringsAsFactors = F))


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
  
  scale_y_continuous(breaks = seq(0, 310, 10), limits = c(0, 310), 
                      expand = expansion(add=c(0,0))) +
  
  labs(title = "No. of Films Rated Per Year", 

      subtitle = str_wrap("I watched a lot of films during 2006-2010,\n
          which was when I was 'studying' at 6th Form and University \n
          (ah freedom!)."),

       caption="source: IMDb",
       x = "Year Rated", 
       y = "No. of Films") +
  
  geom_text(aes(label = films), color="#000000", vjust=-0.5, size=3) +
  
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
  
  scale_y_continuous(breaks = seq(0, 420, 15), limits = c(0, 420), 
                      expand = expansion(add=c(0,0))) +
  
  labs(title = "No. of Films Rated Based on Release Decade", 

      subtitle = str_wrap("Most of the films I've watched are from the 90s to 2000s. \n
                          I clearly need to catch up on some 80s classics!"),

       caption="source: IMDb",
       x = "Decade Film was released in", 
       y = "No. of Films") +
  
  geom_text(aes(label = films), color="#000000", vjust=-0.5, size=3) +

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

  geom_point(size=1) +
  
  geom_segment(aes(x=director, xend=director, y=0, yend=films)) + 
  
  scale_y_continuous(breaks = seq(0, 18, 1), limits = c(0, 18), 
                      expand = expansion(add=c(0,0))) +
  
  labs(title = "No. of Films by Director", 

      subtitle = str_wrap("Swedish director Ingmar Bergman tops the list quite\n 
          comfortably. Though I believe Chris Nolan will eventually overtake \n 
          him here."),

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

genre_viz <- genre %>%
  ggplot(aes(x=reorder(genre, films), y=films)) + 

  geom_point(size=2) +
  
  geom_segment(aes(x=genre, xend=genre, y=0, yend=films)) + 
  
  scale_y_continuous(breaks = seq(0, 650, 20), limits = c(0, 650), 
                      expand = expansion(add=c(0,0))) +
  
  labs(title = "No. of Films by Genre", 

      subtitle = str_wrap("A variety of Genres, with Drama at top\n 
          comfortably. (Though keep in mind alot of films are classified as \n
          'Drama' by IMDb)"),

       caption="source: IMDb",
       x = "Genres", 
       y = "No. of Films") +
  
  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff"),
        axis.text.x = element_text(angle = 90)) +
  coord_flip()


ggsave(genre_viz, 
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

rating_viz <- rating %>%
  ggplot(aes(x=reorder(my_rating, my_rating), y=films)) + 
  
  geom_bar(stat="identity", width=0.8, fill="#000000") +
  
  scale_y_continuous(breaks = seq(0, 410, 20), limits = c(0, 410), 
                      expand = expansion(add=c(0,0))) +
  
  labs(title = "No. of Films by Rating", 

      subtitle = str_wrap("No real suprises here, I've rated most films a 7 or 8, \n
        I generally avoid watching films rated less than 7 on IMDB. \n
        No films have been rated 1 or 10, as no film is truely that bad or \n
        perfect. Only 53 films have been rated the highest rating of 9."),

       caption="source: IMDb",
       x = "Rating (out of 10)", 
       y = "No. of Films") +
  
  geom_text(aes(label = films), color="#000000", vjust=-0.5, size=3) +

  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff"))


ggsave(rating_viz, 
      file = paste0(viz_export_folder, "films_by_rating.png"),
      width = 9.25, height = 5, units = 'in')

#----------------------------------------------------
# films by run time
#----------------------------------------------------
runtime_box <- data.table(
  dataset %>%
    select(film_id, title, runtime_min)
) %>%
  ggplot(aes(y = runtime_min, x = "")) +
	
  geom_boxplot(color="#ffffff", fill = "#000000") +

  labs(title = "Films by Runtime (Minutes)", 

      subtitle = str_wrap("75% of films I've seen are 2 hours and \n
                          15 mins long."),

       caption="source: IMDb",
       y = "Minutes") +
	
  scale_y_continuous(breaks = seq(55, 200, 10), limits = c(55, 200),
                      labels = scales::comma) +
  
  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff"))

ggsave(runtime_box, 
      file = paste0(viz_export_folder, "films_by_runtime_box.png"),
      width = 9.25, height = 5, units = 'in')




runtime_hist <- data.table(
  dataset %>%
    select(film_id, title, runtime_min)
) %>%
  ggplot(aes(x = runtime_min)) +
	
  geom_histogram(binwidth = 5, colour = "#dba506", fill = "#000000") + 

  labs(title = "No. of Films by Runtime (Minutes)", 

      subtitle = str_wrap("Films between 90mins and just over 2 hours are \n
        sweet spot for me."),

       caption="source: IMDb",
       x = "Minutes", 
       y = "No. of Films") +
	
  scale_x_continuous(breaks = seq(50, 250, 5), lim = c(50, 250)) +
	
  scale_y_continuous(labels = scales::comma, 
                      expand = expansion(add=c(0,0)),
                      breaks = seq(0, 105, 5), lim = c(0, 105)) +
  
  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff"),
        axis.text.x = element_text(angle = 90))


ggsave(runtime_hist, 
      file = paste0(viz_export_folder, "runtime_histogram.png"),
      width = 9.25, height = 5, units = 'in')


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
    mutate(language = ifelse(tolower(language) == "hindi" | tolower(language) == "urdu", 
                              "Hindi/Urdu", language)) %>%
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


language_viz <- language %>%
  ggplot(aes(x=reorder(language, films), y=films)) + 

  geom_point(size=2) +
  
  geom_segment(aes(x=language, xend=language, y=0, yend=films)) + 
  
  scale_y_continuous(breaks = seq(0, 900, 50), limits = c(0, 900), 
                      expand = expansion(add=c(0,0))) +
  
  labs(title = "No. of Films by Language", 

      subtitle = str_wrap("Unsurprisingly English makes up the majority of the \n
            films I've rated, with Hindi/Urdu films coming in second."),

       caption="source: IMDb",
       x = "Language", 
       y = "No. of Films") +
  
  geom_text(aes(label = films), hjust=-0.8, size=3) +
  
  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff")) +
  coord_flip()


ggsave(language_viz, 
      file = paste0(viz_export_folder, "films_by_language.png"),
      width = 9.25, height = 5, units = 'in')


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

country_viz <- country %>%
  ggplot(aes(x=reorder(country, films), y=films)) + 

  geom_point(size=2) +
  
  geom_segment(aes(x=country, xend=country, y=0, yend=films)) + 
  
  scale_y_continuous(breaks = seq(0, 710, 50), limits = c(0, 710), 
                      expand = expansion(add=c(0,0))) +
  
  labs(title = "No. of Films by Country", 

      subtitle = str_wrap("Unsprisingly USA/UK & India makes up the majority \n
            of the films I've rated."),

       caption="source: IMDb",
       x = "Language", 
       y = "No. of Films") +
  
  geom_text(aes(label = films), hjust=-0.8, size=3) +
  
  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff")) +
  coord_flip()


ggsave(country_viz, 
      file = paste0(viz_export_folder, "films_by_country.png"),
      width = 9.25, height = 5, units = 'in')

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


writer_viz <- writer %>%
  ggplot(aes(x=reorder(writer, films), y=films)) + 

  geom_point(size=2) +
  
  geom_segment(aes(x=writer, xend=writer, y=0, yend=films)) + 
  
  scale_y_continuous(breaks = seq(0, 17, 1), limits = c(0, 17), 
                      expand = expansion(add=c(0,0))) +
  
  labs(title = "No. of Films by Writer", 

      subtitle = str_wrap("Swedish director/writer Ingmar Bergman tops the list quite\n 
        comfortably. With his films usually being 90 mins, and with many of \n
        being shown on Film4, it's largely not a suprise he's topped the list. \n
        I was suprised seeing Stallone so high on the list, then remembered \n 
        he wrote the Rocky films!"),

       caption="source: IMDb",
       x = "Film Writers", 
       y = "No. of Films") +
  
  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff")) +
  coord_flip()


ggsave(writer_viz, 
      file = paste0(viz_export_folder, "films_by_writer.png"),
      width = 9.25, height = 5, units = 'in')


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
    filter(films >= 10)
)


actors_viz <- actors %>%
  ggplot(aes(x=reorder(actors, films), y=films)) + 

  geom_point(size=2) +
  
  geom_segment(aes(x=actors, xend=actors, y=0, yend=films)) + 
  
  scale_y_continuous(breaks = seq(0, 21, 1), limits = c(0, 21), 
                      expand = expansion(add=c(0,0))) +
  
  labs(title = "No. of Films by Actors", 

      subtitle = str_wrap("Shah Rukh Khan may top the list but \n
          I've rated films by De Niro, Pacino & Christian Bale the highest \n
          - terrific actors!"),

       caption="source: IMDb",
       x = "Actors", 
       y = "No. of Films") +
  
  geom_text(aes(label = paste0("Avg. Rating: ", rating_avg), 
            vjust = 2, hjust = 1.15), size=2) +
  
  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff")) +
  coord_flip()


ggsave(actors_viz, 
      file = paste0(viz_export_folder, "films_by_actors.png"),
      width = 9.25, height = 5, units = 'in')


#----------------------------------------------------
# films by imdb_rating
#----------------------------------------------------
imdb_rating_hist <- data.table(
  dataset %>%
    select(film_id, title, imdb_rating)
) %>%
  ggplot(aes(x = imdb_rating)) +
	
  geom_histogram(binwidth = 0.25, colour = "#dba506", fill = "#000000") + 

  labs(title = "No. of Films by IMDb Rating", 

      subtitle = str_wrap("Most of the films I've watched are also rated \n
        highly by other users at IMDb."),

       caption="source: IMDb",
       x = "IMDB Rating", 
       y = "No. of Films") +
	
  scale_x_continuous(breaks = seq(2.5, 9.5, 0.25), lim = c(2.5, 9.5)) +
	
  scale_y_continuous(labels = scales::comma, 
                      expand = expansion(add=c(0,0)),
                      breaks = seq(0, 215, 10), lim = c(0, 215)) +
  
  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff"),
        axis.text.x = element_text(angle = 90))


ggsave(imdb_rating_hist, 
      file = paste0(viz_export_folder, "films_by_imdb_rating.png"),
      width = 9.25, height = 5, units = 'in')


#----------------------------------------------------
# films by imdb_votes
#----------------------------------------------------

imdb_votes_box <- data.table(
  dataset %>%
    select(film_id, title, imdb_votes)
) %>%
  ggplot(aes(y = imdb_votes, x = "")) +
	
  geom_boxplot(color="#ffffff", fill = "#000000") +

  labs(title = "Films by IMDb Votes", 

      subtitle = str_wrap("25% of films I've rated have less than 50k IMDb \n
                            votes. Generally it seems I rate more obsure films \n
                            than popular ones on IMDb based on votes."),

       caption="source: IMDb",
       y = "IMDB Votes") +
	
  scale_y_continuous(breaks = seq(0, 850000, 50000), limits = c(0, 850000),
                      labels = scales::comma) +
  
  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff"))

ggsave(imdb_votes_box, 
      file = paste0(viz_export_folder, "films_by_imdb_votes_box.png"),
      width = 9.25, height = 5, units = 'in')


imdb_votes_hist <- data.table(
  dataset %>%
    select(film_id, title, imdb_votes)
) %>%
  ggplot(aes(x = imdb_votes)) +
	
  geom_histogram(binwidth = 5000, colour = "#dba506", fill = "#000000") + 

  labs(title = "No. of Films by IMDb Votes", 

      subtitle = str_wrap("A suprise to me, I've watched alot more obsure \n
          films than I had thought"),

       caption="source: IMDb",
       x = "IMDB Votes", 
       y = "No. of Films") +
	
  scale_x_continuous(breaks = seq(0, 800000, 20000), lim = c(0, 800000),
                      labels = scales::comma) +
	
  scale_y_continuous(labels = scales::comma, 
                      expand = expansion(add=c(0,0)),
                      breaks = seq(0, 50, 5), lim = c(0, 50)) +
  
  theme(panel.background = element_rect(fill="#dba506"),
        plot.background = element_rect(fill = "#ffffff"),
        axis.text.x = element_text(angle = 90))


ggsave(imdb_votes_hist, 
      file = paste0(viz_export_folder, "films_by_imdb_votes.png"),
      width = 9.25, height = 5, units = 'in')
