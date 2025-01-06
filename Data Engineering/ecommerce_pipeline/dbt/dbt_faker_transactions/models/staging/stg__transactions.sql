{{ config(
    materialized="table",
    database="dbt",
    schema="staging"
)}}

WITH transactions AS (
    SELECT 
        transaction_id::VARCHAR                         AS transaction_id,
        TO_TIMESTAMP(transaction_date, 
                    'YYY-MM-DD HH-MI-SS')               AS transaction_date,
        
        transaction_data.user_id::VARCHAR               AS user_id,
        transaction_data.user_prefix::VARCHAR           AS user_prefix,
        transaction_data.first_name::VARCHAR            AS user_first_name,
        transaction_data.last_name::VARCHAR             AS user_last_name,
        transaction_data.user_email::VARCHAR            AS user_email,
        transaction_data.product_id::VARCHAR            AS product_id,
        transaction_data.product_category::VARCHAR      AS product_category
    
    FROM 
        {{ ref('src___transactions') }}
),


final AS (
    SELECT
        transaction_id,
        transaction_date,
        
        user_id,
        user_prefix,
        user_first_name,
        user_last_name,
        user_email,
        product_id,
        product_category
    FROM    
        transactions
)

SELECT * FROM final
