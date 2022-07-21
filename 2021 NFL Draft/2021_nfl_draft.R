#--------------------------------------------------------------------------
# set Working Directory
#--------------------------------------------------------------------------
setwd('/home/waseem/Documents/Self-Development/git_repos/waseem-self-development/2021 NFL Draft/')


#--------------------------------------------------------------------------
# Load libraries
#--------------------------------------------------------------------------
library(data.table)
library(ggplot2)
library(tidyverse)
library(lubridate)
library(gridExtra)
library(readxl)
library(cowplot)


#--------------------------------------------------------------------------
# load dataset
#--------------------------------------------------------------------------

# we'll load the csv from our location
raw_dataset <- data.table(
	read_excel('/home/waseem/Documents/Self-Development/2021 NFL Draft/nfl_draft_summary_table.xlsx')
)


#--------------------------------------------------------------------------
# clean dataset
#--------------------------------------------------------------------------

# create new DF, so we can revert back to this if we mess up
# saves us having to load the data into R again
# good practice for when we have large datasets which take time to load in
# or datasets which incur costs (such as loading in from BigQuery)
dataset <- raw_dataset 

# we'll check the structure of the dataset, to see if any columns need changing
# e.g if string columns need to be changed to date/numeric columns instead
str(dataset)
# the structure of the dataset is fine, no changes required

# we'll run a summary over our dataset to understand it better
summary(dataset)

# look to see if we have any oddities/nulls in our dataset
sapply(dataset, function(x) sum(is.na(x)))
# there are a number of NULLs in the following columns:
	# app_type (is it null when the user is not using app?)
	# gender
	# nation
	# barb_region
	# age_range
	# number_of_sport_page_views (NULL when no sports page was viewed and only video is viewed)

# Other findings:
	# videos_watched_on_iplayer & shows_listened_to_on_sounds are not unique
	# they are duplicated across multiple devices
	# this could also be the case for other fields such as 
		# has_visited_homepage, has_visited_news, has_visited_iplayer, has_visited_sounds

#--------------------------------------------------------------------------
# EDA visualisations
#--------------------------------------------------------------------------

# now that we're happy with our dataset, we'll conduct some EDA

unique(select(dataset, user_id))


# users by gender
users_gender <- data.table(
	dataset %>%
		group_by(gender) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users)) %>%
		mutate(gender = ifelse(is.na(gender) == T, 'Null', gender))
) %>%
	ggplot(aes(x = reorder(gender, users), y = users)) +
	geom_bar(stat = 'identity', fill = '#00A9FF') +
	ggtitle('Gender') +
	labs(x = 'Gender', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()


# users by age group
users_age <- data.table(
	dataset %>%
		group_by(age_range) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(age_range) %>%
		filter(!(age_range %in% c('42309', '44475'))) %>%
		mutate(age_range = ifelse(is.na(age_range) == T, 'Null', age_range)) %>%
		mutate(percent = users / sum(users))
) %>%
	ggplot(aes(x = reorder(age_range, users), y = users)) +
	geom_bar(stat = 'identity', fill = '#F8766D') +
	ggtitle('Age Range') +
	labs(x = 'Age Range', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()


# users by device_type
users_device <- data.table(
	dataset %>%
		group_by(device_type) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users))
) %>%
	ggplot(aes(x = reorder(device_type, users), y = users)) +
	geom_bar(stat = 'identity', fill = '#ED68ED') +
	ggtitle('Device') +
	labs(x = 'Device', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()


# users by app type
users_app <- data.table(
	dataset %>%
		filter(app_type %in% c('responsive', 'mobile-app')) %>%
		group_by(device_type, app_type) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users))
) %>%
	filter(device_type %in% c('Desktop', 'Smartphone')) %>%
	ggplot(aes(x = reorder(app_type, users), y = users)) +
	geom_bar(stat = 'identity', fill = '#0CB702') +
	ggtitle('App Type', '% of Total Users') +
	labs(x = 'Device', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	facet_wrap(device_type ~ ., scales = 'free') +
	coord_flip() + 
	theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))


viz_1 <- grid.arrange(grid.arrange(users_gender, users_age, nrow = 1),
											grid.arrange(users_device, users_app, nrow = 1))
ggsave(file = '/home/waseem/Documents/Self-Development/2021 NFL Draft/viz_1.png', 
				viz_1, width = 9.5, height = 8.5, units = 'in')



# users by geo_country_site_visited
users_country <- data.table(
	dataset %>%
		group_by(geo_country_site_visited) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users)) %>%
		mutate(ranked = row_number(desc(users))) %>%
		filter(ranked <= 5)
) %>%
	ggplot(aes(x = reorder(geo_country_site_visited, users), y = users)) +
	geom_bar(stat = 'identity', fill = '#00A9FF') +
	ggtitle('Country', 'Top 5') +
	labs(x = 'Country', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(format(users, big.mark = ','))), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()


# users by nation
users_nation <- data.table(
	dataset %>%
		filter(geo_country_site_visited == 'United Kingdom') %>%
		group_by(nation) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users)) %>%
		mutate(nation = ifelse(is.na(nation) == T, 'Null', nation))
) %>%
	ggplot(aes(x = reorder(nation, users), y = users)) +
	geom_bar(stat = 'identity', fill = '#F8766D') +
	ggtitle('Nation', 'Top 5 UK Only') +
	labs(x = 'Nation', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()


# users by barb_region
users_region <- data.table(
	dataset %>%
		filter(geo_country_site_visited == 'United Kingdom') %>%
		filter(nation == 'England') %>%
		group_by(barb_region) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users)) %>%
		mutate(ranked = row_number(desc(users))) %>%
		filter(ranked <= 5)
) %>%
	ggplot(aes(x = reorder(barb_region, users), y = users)) +
	geom_bar(stat = 'identity', fill = '#ED68ED') +
	ggtitle('Region', 'Top 5 England Only') +
	labs(x = 'Region', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()


viz_2 <- grid.arrange(users_country, users_nation, users_region, ncol = 1)
ggsave(file = '/home/waseem/Documents/Self-Development/2021 NFL Draft/viz_2.png', 
				viz_2, width = 9.5, height = 8.5, units = 'in')



# looking at visits to sport by user
users_visits_to_sport <- data.table(
	dataset %>%
		group_by(user_id) %>%
		summarise(number_of_visits_to_sport = sum(number_of_visits_to_sport)) %>%
		arrange(-number_of_visits_to_sport)
) %>%
	ggplot(aes(x = number_of_visits_to_sport)) +
	geom_histogram(binwidth = 1, colour = 'black', fill = '#00A9FF') + 
	ggtitle('Visits to Sport') +
	labs(x = 'Visits to Sport', y = 'Unique Users') + 
	guides(fill = 'none') +
	scale_x_continuous(breaks = seq(0, 10, 1), lim = c(0, 10)) +
	scale_y_continuous(labels = scales::comma)

users_visits_to_sport_grouped <- data.table(
	dataset %>%
		group_by(user_id) %>%
		summarise(number_of_visits_to_sport = sum(number_of_visits_to_sport)) %>%
		ungroup() %>%
		mutate(group = ifelse(number_of_visits_to_sport == 1, 'One', 
			'More Than One')) %>%
		group_by(group) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users))
) %>%
	ggplot(aes(x = group, y = users)) +
	geom_bar(stat = 'identity', fill = '#00A9FF') +
	ggtitle('Visits to Sport') +
	labs(x = 'How many?', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()

users_visits_to_sport_grouped_plot <-	
			grid.arrange(users_visits_to_sport_grouped, 
							 		 users_visits_to_sport, 
							     ncol = 1,
							     heights = c(2, 4))


# number_of_sport_page_views
users_sport_pageviews <- data.table(
	dataset %>%
		# remove null pageviews 
		filter(is.na(number_of_sport_page_views) == F) %>%
		group_by(user_id) %>%
		summarise(number_of_sport_page_views = sum(number_of_sport_page_views)) %>%
		arrange(-number_of_sport_page_views)
) %>%
	ggplot(aes(x = number_of_sport_page_views)) +
	geom_histogram(binwidth = 1, colour = 'black', fill = '#F8766D') + 
	ggtitle('Sport Pageviews') +
	labs(x = 'Sport Pageviews', y = 'Unique Users') + 
	guides(fill = 'none') +
	scale_x_continuous(breaks = seq(0, 10, 1), lim = c(0, 10)) +
	scale_y_continuous(labels = scales::comma)

users_sport_pageviews_grouped <- data.table(
	dataset %>%
		filter(is.na(number_of_sport_page_views) == F) %>%
		group_by(user_id) %>%
		summarise(number_of_sport_page_views = sum(number_of_sport_page_views)) %>%
		ungroup() %>%
		mutate(group = ifelse(number_of_sport_page_views == 1, 'One', 
			'More Than One')) %>%
		group_by(group) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users))
) %>%
	ggplot(aes(x = group, y = users)) +
	geom_bar(stat = 'identity', fill = '#F8766D') +
	ggtitle('Sport Pageviews') +
	labs(x = 'How many?', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()

users_sport_pageviews_grouped_plot <-	
			grid.arrange(users_sport_pageviews_grouped, 
							 		 users_sport_pageviews, 
							     ncol = 1,
							     heights = c(2, 4))



# number_of_sport_articles_read
users_sport_articles_read <- data.table(
	dataset %>%
		group_by(user_id) %>%
		summarise(number_of_sport_articles_read = sum(number_of_sport_articles_read)) %>%
		arrange(-number_of_sport_articles_read)
) %>%
	ggplot(aes(x = number_of_sport_articles_read)) +
	geom_histogram(binwidth = 1, colour = 'black', fill = '#ED68ED') + 
	ggtitle('Sport Articles Read') +
	labs(x = 'Sport Articles Read', y = 'Unique Users') + 
	guides(fill = 'none') +
	scale_x_continuous(breaks = seq(-1, 10, 1), lim = c(-1, 10)) +
	scale_y_continuous(labels = scales::comma)

users_sport_articles_read_grouped <- data.table(
	dataset %>%
		filter(is.na(number_of_sport_articles_read) == F) %>%
		group_by(user_id) %>%
		summarise(number_of_sport_articles_read = sum(number_of_sport_articles_read)) %>%
		ungroup() %>%
		mutate(group = ifelse(number_of_sport_articles_read == 1, 'One', 
										ifelse(number_of_sport_articles_read == 0, 'None', 
										'More Than One'))) %>%
		group_by(group) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users)) %>%
		filter(group != 'None')
) %>%
	ggplot(aes(x = group, y = users)) +
	geom_bar(stat = 'identity', fill = '#ED68ED') +
	ggtitle('Sport Articles Read') +
	labs(x = 'How many?', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()

users_sport_articles_read_plot <-	
			grid.arrange(users_sport_articles_read_grouped, 
							 		 users_sport_articles_read, 
							     ncol = 1,
							     heights = c(2, 4))


# number_of_sport_articles_read
users_sport_clips_watched <- data.table(
	dataset %>%
		group_by(user_id) %>%
		summarise(number_of_sport_clips_watched = sum(number_of_sport_clips_watched)) %>%
		arrange(-number_of_sport_clips_watched)
) %>%
	ggplot(aes(x = number_of_sport_clips_watched)) +
	geom_histogram(binwidth = 1, colour = 'black', fill = '#0CB702') + 
	ggtitle('Sport Clips Watched') +
	labs(x = 'Sport Clips Watched', y = 'Unique Users') + 
	guides(fill = 'none') +
	scale_x_continuous(breaks = seq(-1, 10, 1), lim = c(-1, 10)) +
	scale_y_continuous(labels = scales::comma)

users_sport_clips_watched_grouped <- data.table(
	dataset %>%
		group_by(user_id) %>%
		summarise(number_of_sport_clips_watched = sum(number_of_sport_clips_watched)) %>%
		ungroup() %>%
		mutate(group = ifelse(number_of_sport_clips_watched == 1, 'One', 
										ifelse(number_of_sport_clips_watched == 0, 'None', 
										'More Than One'))) %>%
		group_by(group) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users)) %>%
		mutate(group = factor(group, levels = c('More Than One', 'One', 'None')))
) %>%
	ggplot(aes(x = group, y = users)) +
	geom_bar(stat = 'identity', fill = '#0CB702') +
	ggtitle('Sport Clips Watched') +
	labs(x = 'How many?', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()

users_sport_clips_watched_plot <-	
			grid.arrange(users_sport_clips_watched_grouped, 
							 		 users_sport_clips_watched, 
							     ncol = 1,
							     heights = c(2, 4))


viz_3 <- grid.arrange(
						grid.arrange(users_visits_to_sport_grouped_plot, 
												users_sport_pageviews_grouped_plot),
						grid.arrange(users_sport_articles_read_plot,
													users_sport_clips_watched_plot),
						nrow = 1)
ggsave(file = '/home/waseem/Documents/Self-Development/2021 NFL Draft/viz_3.png', 
				viz_3, width = 9.5, height = 8.5, units = 'in')






# visited_homepage
visited_homepage <- data.table(
	dataset %>%
		group_by(has_visited_homepage) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users)) 
) %>%
	ggplot(aes(x = has_visited_homepage, y = users)) +
	geom_bar(stat = 'identity', fill = '#00A9FF') +
	ggtitle('Homepage Visit') +
	labs(x = '', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()


# has_visited_news
visited_news <- data.table(
	dataset %>%
		group_by(has_visited_news) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users)) 
) %>%
	ggplot(aes(x = has_visited_news, y = users)) +
	geom_bar(stat = 'identity', fill = '#F8766D') +
	ggtitle('News Visit') +
	labs(x = '', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()


# has_visited_iplayer
visited_iplayer <- data.table(
	dataset %>%
		group_by(has_visited_iplayer) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users)) 
) %>%
	ggplot(aes(x = has_visited_iplayer, y = users)) +
	geom_bar(stat = 'identity', fill = '#ED68ED') +
	ggtitle('iPlayer Visit') +
	labs(x = '', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()



# has_visited_sounds
visited_sounds <- data.table(
	dataset %>%
		group_by(has_visited_sounds) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users)) 
) %>%
	ggplot(aes(x = has_visited_sounds, y = users)) +
	geom_bar(stat = 'identity', fill = '#0CB702') +
	ggtitle('Sounds Visit') +
	labs(x = '', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()



# videos_watched_on_iplayer
videos_watched_on_iplayer <- data.table(
	dataset %>%
		filter(has_visited_iplayer == T) %>%
		select(user_id, videos_watched_on_iplayer) %>%
		unique() %>%
		arrange(videos_watched_on_iplayer)
) %>%
	ggplot(aes(x = videos_watched_on_iplayer)) +
	geom_histogram(binwidth = 1, colour = 'black', fill = '#ED68ED') + 
	ggtitle('iPlayer Videos', 'Has Visited iPlayer') +
	labs(x = 'iPlayer Videos Watched', y = 'Unique Users') + 
	guides(fill = 'none') +
	scale_x_continuous(breaks = seq(-1, 25, 1), lim = c(-1, 25)) +
	scale_y_continuous(labels = scales::comma) +
	theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1))

watched_show <- data.table(
	dataset %>%
		filter(has_visited_iplayer == T) %>%
		select(user_id, videos_watched_on_iplayer) %>%
		unique() %>%
		mutate(watched = ifelse(videos_watched_on_iplayer == 0,
															"No", 'Yes')) %>%
		group_by(watched) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users)) 
) %>%
	ggplot(aes(x = watched, y = users)) +
	geom_bar(stat = 'identity', fill = '#ED68ED') +
	ggtitle('Watched?', 'Videos On iPlayer') +
	labs(x = '', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma)



# shows_listened_to_on_sounds
shows_listened_to_on_sounds <- data.table(
	dataset %>%
		filter(has_visited_sounds == T) %>%
		select(user_id, shows_listened_to_on_sounds) %>%
		unique() %>%
		arrange(shows_listened_to_on_sounds)
) %>%
	ggplot(aes(x = shows_listened_to_on_sounds)) +
	geom_histogram(binwidth = 1, colour = 'black', fill = '#0CB702') + 
	ggtitle('Sounds Shows', 'Has Visited Sounds') +
	labs(x = 'Sounds Shows Listened', y = 'Unique Users') + 
	guides(fill = 'none') +
	scale_x_continuous(breaks = seq(-1, 25, 1), lim = c(-1, 25)) +
	scale_y_continuous(labels = scales::comma) +
	theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1))

listened_to_show <- data.table(
	dataset %>%
		filter(has_visited_sounds == T) %>%
		select(user_id, shows_listened_to_on_sounds) %>%
		unique() %>%
		mutate(listened = ifelse(shows_listened_to_on_sounds == 0,
															"No", 'Yes')) %>%
		group_by(listened) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users)) 
) %>%
	ggplot(aes(x = listened, y = users)) +
	geom_bar(stat = 'identity', fill = '#0CB702') +
	ggtitle('Listened?', 'Show on BBC Sounds') +
	labs(x = '', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma)




viz_4 <- grid.arrange(
						grid.arrange(visited_homepage, visited_news, nrow = 1),
						grid.arrange(visited_iplayer, visited_sounds, nrow = 1),
						grid.arrange(videos_watched_on_iplayer, watched_show, 
													nrow = 1, widths = c(3, 1)),
						grid.arrange(shows_listened_to_on_sounds, listened_to_show, 
													nrow = 1, widths = c(3, 1)),
						heights = c(2, 2, 2, 2))
ggsave(file = '/home/waseem/Documents/Self-Development/2021 NFL Draft/viz_4.png', 
				viz_4, width = 9.5, height = 8.5, units = 'in')





#--------------------------------------------------------------------------
# Users Segmentation using K-Means Clustering
#--------------------------------------------------------------------------

# We will create customer segments based on the numerical features
segments <- data.table(
	dataset %>%
		filter(geo_country_site_visited == 'United Kingdom') %>%
		group_by(user_id) %>%
		summarise(
			sport_visits = sum(number_of_visits_to_sport),
			sport_pageviews = sum(ifelse(is.na(number_of_sport_page_views) == T, 0,
															number_of_sport_page_views)),
			sport_articles = sum(number_of_sport_articles_read),
			sport_clips = sum(number_of_sport_clips_watched),
			iplayer_videos = max(videos_watched_on_iplayer),
			sounds_shows = max(shows_listened_to_on_sounds),
		)
)


# Elbow Method for finding the optimal number of clusters
set.seed(0)
# Compute and plot wss for k = 2 to k = 15.
k.max <- 10
wss <- sapply(1:k.max, 
              function(k){kmeans(as.matrix(scale(select(segments, -user_id))), 
              			k, nstart = 50, iter.max = 15 )$tot.withinss})
plot(1:k.max, wss,
     type = 'b', pch  =  19, frame  =  FALSE, 
     xlab = 'Number of clusters K',
     ylab = 'Total within-clusters sum of squares')
# we will build with 3 clusters

#Let us apply kmeans for k=3 clusters 
kmm <- kmeans(as.matrix(scale(select(segments, -user_id))), 3, nstart = 50, iter.max = 15)

# add the clusters info in our dataframe
segments$cluster <- kmm$cluster


# this is a summary of our K-means
segments_summary <- data.table(
	segments %>% 
		group_by(cluster) %>% 
		summarise(
			# this will show us the number of customers in each cluster
			users = n_distinct(user_id),
			sport_visits_avg = round(mean(sport_visits)),
			sport_pageviews_avg = round(mean(sport_pageviews)),
			sport_articles_avg = round(mean(sport_articles)),
			sport_clips_avg = round(mean(sport_clips)),
			iplayer_videos_avg = round(mean(iplayer_videos)),
			sounds_shows_avg = round(mean(sounds_shows)),
		)
)

# we'll save our segment_summary as a .csv
write.csv(segments_summary,
					'/home/waseem/Documents/Self-Development/2021 NFL Draft/segment_summary.csv',
					row.names = F)




#--------------------------------------------------------------------------
# Deep Dive on the 'Enthusiasts' Cluster
#--------------------------------------------------------------------------
enthusiasts <- data.table(
	left_join(dataset,
						select(segments, user_id, cluster), 
						by = ('user_id')) %>%
	mutate(cluster_num = cluster,
				 cluster = ifelse(cluster == 2, 'Enthusiasts', 'Others')) %>%
	filter(geo_country_site_visited == 'United Kingdom')
)


# users by gender
enthusiasts_gender <- data.table(
	enthusiasts %>%
		group_by(cluster, gender) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		group_by(cluster) %>%
		mutate(percent = users / sum(users)) %>%
		ungroup() %>%
		mutate(gender = ifelse(is.na(gender) == T, 'Null', gender))
) %>%
	ggplot(aes(x = reorder(gender, users), y = users, fill = cluster)) +
	geom_bar(stat = 'identity') +
	ggtitle('Gender') +
	labs(x = 'Gender', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip() +
	facet_wrap(cluster ~ ., scales = 'free') +
	# we don't want a legend for the fill
	guides(fill = 'none')


# users by age group
enthusiasts_age <- data.table(
	enthusiasts %>%
		group_by(cluster, age_range) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(age_range) %>%
		filter(!(age_range %in% c('42309', '44475'))) %>%
		mutate(age_range = ifelse(is.na(age_range) == T, 'Null', age_range)) %>%
		group_by(cluster) %>%
		mutate(percent = users / sum(users))
) %>%
	ggplot(aes(x = reorder(age_range, users), y = users, fill = cluster)) +
	geom_bar(stat = 'identity') +
	ggtitle('Age Range') +
	labs(x = 'Age Range', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip() +
	facet_wrap(cluster ~ ., scales = 'free') +
	# we don't want a legend for the fill
	guides(fill = 'none')


# users by device_type
enthusiasts_device <- data.table(
	enthusiasts %>%
		group_by(cluster, device_type) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		group_by(cluster) %>%
		mutate(percent = users / sum(users))
) %>%
	ggplot(aes(x = reorder(device_type, users), y = users, fill = cluster)) +
	geom_bar(stat = 'identity') +
	ggtitle('Device') +
	labs(x = 'Device', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip() +
	facet_wrap(cluster ~ ., scales = 'free') +
	# we don't want a legend for the fill
	guides(fill = 'none')


# users by app type
enthusiasts_app <- data.table(
	enthusiasts %>%
		filter(app_type %in% c('responsive', 'mobile-app')) %>%
		group_by(cluster, device_type, app_type) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		group_by(cluster) %>%
		mutate(percent = users / sum(users))
) %>%
	filter(device_type %in% c('Desktop', 'Smartphone')) %>%
	ggplot(aes(x = reorder(app_type, users), y = users, fill = cluster)) +
	geom_bar(stat = 'identity') +
	ggtitle('App Type', '% of Total Users') +
	labs(x = 'Device', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	facet_wrap(device_type ~ cluster, scales = 'free') +
	coord_flip() + 
	theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) +
	coord_flip()


viz_5 <- grid.arrange(grid.arrange(enthusiasts_gender, enthusiasts_age, nrow = 1),
											grid.arrange(enthusiasts_device, enthusiasts_app, nrow = 1))
ggsave(file = '/home/waseem/Documents/Self-Development/2021 NFL Draft/viz_5.png', 
				viz_5, width = 9.5, height = 8.5, units = 'in')




#--------------------------------------------------------------------------
# Cross device users
#--------------------------------------------------------------------------

# cross-device users
# these are users who used more than one device
cross_device <- data.table(
	dataset %>%
		select(user_id, device_type) %>%
		unique() %>%
		group_by(user_id) %>%
		summarise(devices = n_distinct(device_type)) %>%
		ungroup() %>%
		group_by(devices) %>%
		summarise(users = n_distinct(user_id)) %>%
		mutate(percent = users / sum(users))
) %>%
	ggplot(aes(x = reorder(devices, users), y = users)) +
	geom_bar(stat = 'identity', fill = '#00A9FF') +
	ggtitle('How many devices?') +
	labs(x = 'Unique Devices', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()



# cross app_type
cross_app_type <- data.table(
	dataset %>%
		select(user_id, device_type, app_type) %>%
		unique() %>%
		group_by(user_id, device_type) %>%
		summarise(app_types = n_distinct(app_type)) %>%
		ungroup() %>%
		group_by(device_type, app_types) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		group_by(device_type) %>%
		mutate(percent = users / sum(users))
) %>%
	ggplot(aes(x = reorder(devices, users), y = users)) +
	geom_bar(stat = 'identity', fill = '#00A9FF') +
	ggtitle('How many devices?') +
	labs(x = 'Unique Devices', y = 'Unique Users') +
	# text for the conversion
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
	          color = 'black', size = 3, fontface = 'bold',
	          position = position_stack(vjust = 0.5, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	coord_flip()