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
revenue_trend <- data.table(
	master %>%
		mutate(period = udf_period(transaction_date, min_last_12_months, 
																max_date, min_prior_12_months)) %>%
		# filter to the last 12 months
		filter(is.na(period) == F) %>%
		filter(transaction_status == 'success') %>%
		mutate(month_date = as.Date(as.yearmon(transaction_date, '%m/%Y')),
						month_name = as.yearmon(transaction_date, '%m/%Y'))
)

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
)


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
	ifelse(state == 'customer' & lag(state) == 'dunning', T, F)
}


test <- data.table(
	master %>%
		select(account_id, account_title, product_title,
						payment_period_title, transaction_date, transaction_id, invoice_date, 
						invoice_id, transaction_amount, transaction_status, failure_reason,
						account_product_id) %>%
		group_by(account_id, transaction_id, invoice_id) %>%
		mutate(state = udf_status(invoice_date, transaction_date, transaction_status)) %>%
		ungroup() %>%
		group_by(account_id, invoice_id) %>%
		arrange(transaction_id) %>%
		ungroup() %>%
		group_by(account_id, invoice_id) %>%
		mutate(churn_to_customer = udf_churn_to_customer(state))
)


filter(test, churn_to_customer == T)
filter(test, account_id == '999')