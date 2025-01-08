{{ config(
    materialized="table",
    database="dbt",
    schema="fact"
)}}

SELECT
    transaction_id, -- Primary Key
    product_id,
    user_id,
    transaction_date
FROM
    {{ ref('stg__transactions') }}
