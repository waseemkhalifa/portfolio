#--------------------------------------------------------------------------
# set Working Directory
#--------------------------------------------------------------------------
setwd('/home/waseem/Documents/Self-Development/git_repos/waseem-self-development/BoF/')


#--------------------------------------------------------------------------
# Load libraries
#--------------------------------------------------------------------------
library(data.table)
library(ggplot2)
library(tidyverse)
library(lubridate)
library(gridExtra)
library(sqldf)
library(arules)
library(scales)
library(zoo)


#--------------------------------------------------------------------------
# load datasets
#--------------------------------------------------------------------------

# account table
# PK: account_id
raw_account <- data.table(
	read.csv('/home/waseem/Documents/Self-Development/BoF/Tables/ACCOUNT.csv', 
				stringsAsFactors = F)
)

# account_product table
# PK: account_product_id
raw_account_product <- data.table(
	read.csv('/home/waseem/Documents/Self-Development/BoF/Tables/ACCOUNTPRODUCT.csv', 
				stringsAsFactors = F)
)

# product table
# PK: product_id
raw_product <-  data.table(
	read.csv('/home/waseem/Documents/Self-Development/BoF/Tables/PRODUCT.csv', 
				stringsAsFactors = F)
)

# payment_period table
# PK: payment_period_id
raw_payment_period <- data.table(
	read.csv('/home/waseem/Documents/Self-Development/BoF/Tables/PAYMENTPERIOD.csv', 
				stringsAsFactors = F)
)

# invoice table
# PK: invoice_id
raw_invoice <- data.table(
	read.csv('/home/waseem/Documents/Self-Development/BoF/Tables/INVOICE.csv', 
				stringsAsFactors = F)
)

# transaction table
# PK: transaction_id
raw_transaction <- data.table(
	read.csv('/home/waseem/Documents/Self-Development/BoF/Tables/TRANSACTION.csv', 
				stringsAsFactors = F)
)


#--------------------------------------------------------------------------
# clean datasets
#--------------------------------------------------------------------------

# account
str(raw_account)
account <- data.table(
	raw_account %>%
	rename(account_id = ACCOUNT_ID,
					account_title = ACCOUNT_TITLE,
					account_type_id = ACCOUNT_TYPE_ID) %>%
	# we'll convert these columns from int to string
	# as they won't be treated as int (not summing etc)
	mutate(account_id = as.character(account_id),
					account_type_id = as.character(account_type_id))
)


# account_product
str(raw_account_product)
account_product <- data.table(
	raw_account_product %>%
	rename(account_product_id = ACCOUNT_PRODUCT_ID,
					account_id = ACCOUNT_ID,
					product_id = PRODUCT_ID) %>%
	# we'll convert these columns from int to string
	# as they won't be treated as int (not summing etc)
	mutate(account_product_id = as.character(account_product_id),
					account_id = as.character(account_id),
					product_id = as.character(product_id))
)


# account_product
str(raw_product)
product <- data.table(
	raw_product %>%
	rename(product_title = PRODUCT_TITLE,
					product_id = PRODUCT_ID) %>%
	# we'll convert these columns from int to string
	# as they won't be treated as int (not summing etc)
	mutate(product_id = as.character(product_id))
)


# payment_period
str(raw_payment_period)
payment_period <- data.table(
	raw_payment_period %>%
	rename(payment_period_title = PAYMENT_PERIOD_TITLE,
					payment_period_id = PAYMENT_PERIOD_ID) %>%
	# we'll convert these columns from int to string
	# as they won't be treated as int (not summing etc)
	mutate(payment_period_id = as.character(payment_period_id))
)


# invoice
str(raw_invoice)
invoice <- data.table(
	raw_invoice %>%
	rename(invoice_id = INVOICE_ID,
					account_product_id = ACCOUNT_PRODUCT_ID,
					payment_period_id = PAYMENT_PERIOD_ID,
					created_date_time = CREATED_DATETIME
				) %>%
	# we'll convert these columns from int to string
	# as they won't be treated as int (not summing etc)
	mutate(invoice_id = as.character(invoice_id),
					account_product_id = as.character(account_product_id),
					payment_period_id = as.character(payment_period_id)) %>%
	# we'll create a new field for date
	# as the timestamp stores no time
	mutate(invoice_date = ymd(substr(created_date_time, 1, 10)))
)


# transaction
str(raw_transaction)
transaction <- data.table(
	raw_transaction %>%
	rename(transaction_id = TRANSACTION_ID,
					invoice_id = INVOICE_ID,
					transaction_amount = TRANSACTION_AMOUNT_IN_CENTS,
					transaction_status = TRANSACTION_STATUS,
					failure_reason = FAILURE_REASON,
					created_date_time = CREATED_DATETIME
				) %>%
	# we'll convert these columns from int to string
	# as they won't be treated as int (not summing etc)
	mutate(transaction_id = as.character(transaction_id),
					invoice_id = as.character(invoice_id)) %>%
	# we'll create a new field for date
	# as the timestamp stores no time
	mutate(transaction_date = ymd(substr(created_date_time, 1, 10)))
)


#--------------------------------------------------------------------------
# Master dataset
#--------------------------------------------------------------------------

# our master dataset
# row count for transaction = 10064
# we'll now join transaction to invoice
master <- data.table(
	left_join(select(transaction, -created_date_time),
						select(invoice, -created_date_time), by = c('invoice_id'))
)
# we'll now join to account_product to get product_id
master <- data.table(
	left_join(master, account_product, by = c('account_product_id'))
)
# we find that 32 rows have NULL for product_id
# we'll now join to product to get product_title
master <- data.table(
	left_join(master, product, by = c('product_id')) 
)
# let's join to account and see if any account with null product_id
# had other invoices which had a product id
master <- data.table(
	left_join(master, account, by = c('account_id')) 
)
# we also find that they don't have account_id's
# this looks like bad data and we should remove it
# let's now join with payment_period so that we have everything
master <- data.table(
	left_join(master, payment_period, by = c('payment_period_id')) 
)
# no duplicates, row count = 10064
# we'll remove any rows which don't have an account_id
master <- data.table(
	master %>%
		filter(is.na(account_id) == F)
)


#--------------------------------------------------------------------------
# EDA
#--------------------------------------------------------------------------

max_date <- max(master$transaction_date)
min_last_12_months <- add_with_rollback(max_date, months(-12), 
																					roll_to_first = TRUE)
min_prior_12_months <- add_with_rollback(min_last_12_months - 1, months(-12), 
																					roll_to_first = TRUE)

# custom function for period
udf_period <- function(transaction_date, min_last_12_months, max_date, 
												min_prior_12_months) {
	ifelse(between(transaction_date, min_last_12_months, max_date), 
					'This Year', 
	ifelse(between(transaction_date, min_prior_12_months, min_last_12_months - 1), 
					'Last Year', 
					NA))
}


# Calculate and visualise revenue for the latest 12 month period?
# How does that compare to the prior 12 month period?
# Last Year 2017-11-20 2018-11-19             
# This Year 2018-11-20 2019-11-07 
revenue_trend <- data.table(
	master %>%
		mutate(period = udf_period(transaction_date, min_last_12_months, 
																max_date, min_prior_12_months)) %>%
		# filter to the last 12 months
		filter(is.na(period) == F) %>%
		filter(transaction_status == 'success') %>%
		mutate(month_date = as.Date(as.yearmon(transaction_date, '%m/%Y')),
						month_name = as.yearmon(transaction_date, '%m/%Y')) %>%
		group_by(period, month_date, month_name) %>%
		summarise(transaction_amount = sum(transaction_amount)) %>%
		ungroup() %>%
		mutate(revenue = transaction_amount / 100)
) %>%
	ggplot(aes(x = month_date, y = revenue, fill = period)) +
	geom_bar(stat = 'identity') +
	ggtitle('12 Month Revenue', '20/11/17 to 19/11/18 vs 20/11/18 to 19/11/19') +
	labs(x = 'Month', y = 'Revenue ($)') +
	# text for the conversion
	geom_text(aes(label = paste0('$', format(round(revenue), big.mark = ','))), 
	          color = 'black', size = 4, #angle = 90,
	          position = position_stack(vjust = 0.8, reverse = FALSE)) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
  scale_x_date(date_breaks = '1 month', date_labels = '%b %Y') +
	theme(legend.position = 'bottom', legend.title = element_blank()) +
	facet_wrap(period ~ ., scales = 'free_x', ncol = 1)


revenue_total <- data.table(
	master %>%
		mutate(period = udf_period(transaction_date, min_last_12_months, 
																max_date, min_prior_12_months)) %>%
		# filter to the last 12 months
		filter(is.na(period) == F) %>%
		filter(transaction_status == 'success') %>%
		group_by(period) %>%
		summarise(transaction_amount = sum(transaction_amount)) %>%
		ungroup() %>%
		arrange(period) %>%
		mutate(diff = ifelse(period == 'This Year', 
					(transaction_amount - lag(transaction_amount, 1)) / lag(transaction_amount, 1), NA)) %>%
		ungroup() %>%
		mutate(revenue = transaction_amount / 100)
) %>%
	ggplot(aes(x = period, y = revenue, fill = period)) +
	geom_bar(stat = 'identity') +
	ggtitle('Total 12 Month Revenue', '20/11/17 to 19/11/18 vs 20/11/18 to 19/11/19') +
	labs(x = 'Period', y = 'Revenue ($)') +
	# text for the conversion
	geom_text(aes(label = paste0('$', format(round(revenue), big.mark = ','))), 
	          color = 'black', size = 4, #angle = 90,
	          position = position_stack(vjust = 0.8, reverse = FALSE)) +
	 # text for the percent
	  geom_text(aes(label = ifelse(is.na(diff) == F, 
	  								paste0(round(diff * 100, 2), '%'), '')), 
	            color = 'white', size = 4, fontface = 'bold',
	            position = position_dodge(width = 1), vjust = 5) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	# we don't want a legend for the fill
	guides(fill = 'none') 




# What is our revenue split between Careers and Memberships products?
product_title_viz <- data.table(
	master %>%
		mutate(period = udf_period(transaction_date, min_last_12_months, 
																max_date, min_prior_12_months)) %>%
		# filter to the last 12 months
		filter(is.na(period) == F) %>%
		filter(transaction_status == 'success') %>%
		group_by(period, product_title) %>%
		summarise(transaction_amount = sum(transaction_amount)) %>%
		ungroup() %>%
		group_by(period) %>%
		mutate(percent = transaction_amount / sum(transaction_amount)) %>%
		arrange(period, -percent)
) %>%
	ggplot(aes(x = period, y = revenue, fill = period)) +
	geom_bar(stat = 'identity') +
	ggtitle('Total 12 Month Revenue', '20/11/17 to 19/11/18 vs 20/11/18 to 19/11/19') +
	labs(x = 'Period', y = 'Revenue ($)') +
	# text for the conversion
	geom_text(aes(label = paste0('$', format(round(revenue), big.mark = ','))), 
	          color = 'black', size = 4, #angle = 90,
	          position = position_stack(vjust = 0.8, reverse = FALSE)) +
	 # text for the percent
	  geom_text(aes(label = ifelse(is.na(diff) == F, 
	  								paste0(round(diff * 100, 2), '%'), '')), 
	            color = 'white', size = 4, fontface = 'bold',
	            position = position_dodge(width = 1), vjust = 5) +
	# gives the y axis the percentage scale
	scale_y_continuous(labels = scales::comma) +
	theme(legend.position = 'bottom', legend.title = element_blank()) 







# What are the top three reasons for payment failures (in descending order)
payment_failures <- data.table(
	master %>%
		filter(transaction_status == 'failed') %>%
		group_by(failure_reason) %>%
		summarise(transactions = n_distinct(transaction_id)) %>%
		ungroup() %>%
		mutate(percent = transactions / sum(transactions)) %>%
		arrange(-percent)
)




# Over the last 12 months what amount of accounts have churned?
# Which month had the highest churn?

# this is a user defined function
# we'll use this to determine if the customer goes into the following states:
	# dunning, churn or successfully paid customer
udf_status <- function(invoice_date, transaction_date, transaction_status) {
	ifelse(between(transaction_date, invoice_date, invoice_date + 6) 
					& transaction_status != 'success', 
					'dunning',
	ifelse(!(between(transaction_date, invoice_date, invoice_date + 6))
					& transaction_status != 'success', 
					'churned',
	ifelse(between(transaction_date, invoice_date, invoice_date + 6) 
					& transaction_status == 'success', 
					'renewal',
					NA
	)))
} 

# this is a user defined function
# we'll use this to uncover invoices which have 
# gone from dunning to churned
udf_dunning_to_churned <- function(state) {
	ifelse(state == 'churned' & lag(state) == 'dunning', T, F)
}

churn_trend <- data.table(
	master %>%
		mutate(period = udf_period(transaction_date, min_last_12_months, 
																max_date, min_prior_12_months)) %>%
		# filter to the last 12 months
		filter(period == 'This Year') %>%
		mutate(month_date = as.Date(as.yearmon(transaction_date, '%m/%Y')),
						month_name = as.yearmon(transaction_date, '%m/%Y')) %>%
		group_by(account_id, transaction_id, invoice_id) %>%
		mutate(state = udf_status(invoice_date, transaction_date, transaction_status)) %>%
		ungroup %>%
		group_by(account_id, invoice_id) %>%
		arrange(transaction_id) %>%
		mutate(dunning_to_churned = udf_dunning_to_churned(state)) %>%
		ungroup() %>%
		filter(dunning_to_churned == T) %>%
		group_by(month_date, month_name) %>%
		summarise(churned_accounts = n_distinct(account_id))
)


# Over the past 12 months, how many account renewals have been recovered 
# from the dunning process on a month by month basis?

# this is a user defined function
# we'll use this to uncover invoices which have been recovered from dunning
# dunning to successfully renewal
udf_dunning_to_renewal <- function(state) {
	ifelse(state == 'renewal' & lag(state) == 'dunning', T, F)
}

renewal_trend <- data.table(
	master %>%
		mutate(period = udf_period(transaction_date, min_last_12_months, 
																max_date, min_prior_12_months)) %>%
		# filter to the last 12 months
		filter(period == 'This Year') %>%
		mutate(month_date = as.Date(as.yearmon(transaction_date, '%m/%Y')),
						month_name = as.yearmon(transaction_date, '%m/%Y')) %>%
		group_by(account_id, transaction_id, invoice_id) %>%
		mutate(state = udf_status(invoice_date, transaction_date, transaction_status)) %>%
		ungroup %>%
		group_by(account_id, invoice_id) %>%
		arrange(transaction_id) %>%
		mutate(dunning_to_renewal = udf_dunning_to_renewal(state)) %>%
		ungroup() %>%
		filter(dunning_to_renewal == T) %>%
		group_by(month_date, month_name) %>%
		summarise(dunning_to_renewal = n_distinct(account_id))
)


# On a month by month basis what is our total MRR (Monthly Recurring Revenue) 
# across all products? 

# we'll find the latest transaction state for each account and product
# we'll then divide by 12 any yearly transaction_amount
# monthly transaction amount will stay the same
# we'll then group up the revenue by account_id and state of the latest order
mmr <- data.table(
	master %>%
		group_by(account_id, transaction_id, invoice_id) %>%
		mutate(state = udf_status(invoice_date, transaction_date, transaction_status)) %>%
		ungroup %>%
		group_by(account_id, product_title) %>%
		mutate(lastest_transaction = row_number(desc(transaction_date))) %>%
		filter(lastest_transaction == 1) %>%
		ungroup() %>%
		# we'll divide the transaction_amount by 12 if it is paid yearly
		# else we'll leave as is
		mutate(revenue = ifelse(payment_period_title == 'Yearly', 
															transaction_amount / 12, 
											ifelse(payment_period_title == 'Monthly', 
															transaction_amount,
											NA))) %>%
		group_by(account_id, state) %>%
		summarise(revenue = sum(revenue)) 
)
# we'll now join to the account table
# any account without a transaction value, is a new account and is still active
# we will only count accounts which are 'renewal' or without a transaction
# as active accounts
# all accounts have a trans value
mmr <- data.table(
	left_join(account, mmr, by = c('account_id')) %>%
	filter(state == 'renewal') %>%
	mutate(total = 'total') %>%
	group_by(total) %>%
	summarise(active_accounts = n_distinct(account_id),
						avg_revenue_per_account = mean(revenue)) %>%
	ungroup() %>%
	mutate(mmr = active_accounts * avg_revenue_per_account)
)

filter(active_account, is.na(revenue))




both_products %>% filter(lastest_transaction > 1)
both_products %>% filter(account_id == '999')
filter(account, account_id == '999')
test %>% filter(account_id == '666')