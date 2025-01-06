{{ config(
    materialized="table",
    database="dbt",
    schema="dimension"
)}}

SELECT
    transaction_id, -- Primary Key
    transaction_date
FROM
    {{ ref('stg__transactions') }}