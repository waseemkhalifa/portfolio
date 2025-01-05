
{{ config(
    materialized="table",
    database="dbt",
    schema="source"
)}}


WITH src AS (
    SELECT 
        transaction_id::VARCHAR             AS transaction_id,
        TO_TIMESTAMP(transaction_date, 
                    'YYY-MM-DD HH-MI-SS')   AS transaction_date,
        JSON_PARSE(transaction_data)        AS transaction_data
    FROM 
        {{ source('src__faker_transactions', 'faker__transactions') }}
)

SELECT * FROM src
