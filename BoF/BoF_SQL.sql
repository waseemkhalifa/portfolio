/*
	- this is the master table
	- which joins all the tables together
	- it will make it easier to conduct the analysis by only querying
	- one table
*/
CREATE OR REPLACE TABLE 
	test_day.sandbox_1.master
AS
SELECT
	-- columns from transaction table
	a.transaction_id,
	a.invoice_id,
	a.TRANSACTION_AMOUNT_IN_CENTS AS transaction_amount, 
	a.transaction_status, 
	a.failure_reason,
	TO_DATE(a.CREATED_DATETIME) AS transaction_date,  
	-- columns from invoice table
	b.account_product_id, 
	b.payment_period_id, 
	TO_DATE(b.CREATED_DATETIME) AS invoice_date,
	-- columns from accountproduct table
	c.account_id,
	c.product_id,
	-- columns from product table
	d.product_title,
	-- columns from account table
	e.account_title,
	e.account_type_id,
	-- columns from paymentperiod table
	f.payment_period_title
FROM
	test_day.test.transaction AS a
LEFT JOIN
	test_day.test.invoice AS b
	USING(invoice_id)
LEFT JOIN
	test_day.test.accountproduct AS c
	USING(account_product_id)
LEFT JOIN
	test_day.test.product AS d
	USING(product_id)
LEFT JOIN
	test_day.test.account AS e
	USING(account_id)
LEFT JOIN
	test_day.test.paymentperiod AS f
	USING(payment_period_id)
WHERE
	c.account_id IS NOT NULL
;




/*
	- Calculate and visualise revenue for the latest 12 month period?
	- How does that compare to the prior 12 month period?
*/

-- this is the maximum date in our dataset
SET max_date = to_date('2019-11-20');
-- we find the last 12 months from this date range
SET min_last_12_months = DATEADD(MONTH, -12, $max_date);
-- we find the previous 12 months (for last year period)
SET min_prior_12_months = DATEADD(MONTH, -12, DATEADD(DAY, -1, $min_last_12_months));

CREATE OR REPLACE TABLE 
	test_day.sandbox_1.question_1
AS

WITH


base AS (

	SELECT
		CASE 
			WHEN transaction_date BETWEEN $min_last_12_months AND $max_date 
			THEN 'This Year'
			WHEN transaction_date BETWEEN $min_prior_12_months AND DATEADD(DAY, -1, $min_prior_12_months) 
			THEN 'Last Year'
		END AS period,
		
)