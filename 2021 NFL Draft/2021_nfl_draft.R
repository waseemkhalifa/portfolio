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


#--------------------------------------------------------------------------
# EDA visualisations
#--------------------------------------------------------------------------

# now that we're happy with our dataset, we'll conduct some EDA

unique(select(dataset, gender))


# users by gender
users_gender <- data.table(
	dataset %>%
		group_by(gender) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users))
)

# users by age group
users_age <- data.table(
	dataset %>%
		group_by(age_range) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(age_range) %>%
		mutate(percent = users / sum(users))
)

# users by device_type
users_device <- data.table(
	dataset %>%
		group_by(device_type) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users))
)

# users by app type
users_app <- data.table(
	dataset %>%
		filter(app_type %in% c('responsive', 'mobile-app')) %>%
		group_by(device_type, app_type) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users))
)

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
)

# users by nation
users_nation <- data.table(
	dataset %>%
		filter(geo_country_site_visited == 'United Kingdom') %>%
		group_by(nation) %>%
		summarise(users = n_distinct(user_id)) %>%
		ungroup() %>%
		arrange(-users) %>%
		mutate(percent = users / sum(users))
)


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
)


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
)