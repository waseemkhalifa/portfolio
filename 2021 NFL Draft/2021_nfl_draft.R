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
	# number_of_sport_page_views (NULL when no sports page was viewed?)

# Other findings:
	# 

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
	geom_text(aes(label = paste0(round(percent * 100), '%')), 
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
		filter(device_type %in% c('Smartphone', 'Desktop')) %>%
		group_by(user_id, device_type) %>%
		summarise(number_of_visits_to_sport = sum(number_of_visits_to_sport)) %>%
		arrange(-number_of_visits_to_sport)
) %>%
	ggplot(aes(x = order_value, fill = country)) +
	geom_histogram(binwidth = 50, colour = 'black') + 
	ggtitle('Order values by Country',
					'Top 5 Markets, in £50 bins') +
	labs(x = 'Order Value (£)', y = 'No. of Orders') + 
	guides(fill = 'none') +
	# scale_x_continuous(breaks = seq(0, 3000, 250), lim = c(-50, 3000)) +
	xlim(-50, 3000) +
	facet_wrap(country ~ ., scales = 'free') +
	scale_y_continuous(labels = scales::comma)