{{ config(
    materialized="table",
    database="dbt",
    schema="dimension"
)}}

SELECT
    product_id, -- Primary Key
    product_category
FROM
    {{ ref('stg__transactions') }}
