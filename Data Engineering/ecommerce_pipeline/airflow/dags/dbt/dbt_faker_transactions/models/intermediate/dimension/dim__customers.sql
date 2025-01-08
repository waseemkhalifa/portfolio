{{ config(
    materialized="table",
    database="dbt",
    schema="dimension"
)}}

SELECT
    user_id, -- Primary Key
    user_prefix,
    user_first_name,
    user_last_name,
    user_email
FROM
    {{ ref('stg__transactions') }}
