{{ config(
    materialized="table",
    database="dbt",
    schema="mart"
)}}


SELECT
    trans.transaction_date::DATE    AS transaction_date,
    COUNT(DISTINCT transaction_id)  AS orders
FROM
    {{ ref('fct__transactions') }} AS trans
GROUP BY 
    1
