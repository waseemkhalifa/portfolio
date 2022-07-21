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
	mutate(created_date = ymd(substr(created_date_time, 1, 10)))
)


# transaction
str(raw_transaction)
transaction <- data.table(
	raw_transaction %>%
	rename(transaction_id = TRANSACTION_ID,
					invoice_id = INVOICE_ID,
					transaction_ammount = TRANSACTION_AMOUNT_IN_CENTS,
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
	mutate(created_date = ymd(substr(created_date_time, 1, 10)))
)






#--------------------------------------------------------------------------
# EDA visualisations
#--------------------------------------------------------------------------



# Calculate and visualise revenue for the latest 12 month period?
	# How does that compare to the prior 12 month period?
	# What is our revenue split between Careers and Memberships products?

revenue <- data.table(
	left_join(transaction, product, by = c('product_id'))
)

max(transaction$created_date)