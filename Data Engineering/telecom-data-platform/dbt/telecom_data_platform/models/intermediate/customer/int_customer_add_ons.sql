{{
    config(
        materialized='incremental',
        schema='intermediate',
        tags=['silver', 'intermediate', 'customer']
    )
}}

SELECT
    customer_id,
    event_id,
    event_date,
    event_timestamp,
    channel,
    add_on_name,
    add_on_cost,

    IF(LOWER(add_on_name) = 'international calls', 1, 0) AS is_add_on__international_calls,
    IF(LOWER(add_on_name) = 'roaming pass', 1, 0) AS is_add_on__roaming_pass,
    IF(LOWER(add_on_name) = 'extra data', 1, 0) AS is_add_on__extra_data,
    IF(LOWER(add_on_name) = 'netflix bundle', 1, 0) AS is_add_on__netflix_bundle

FROM
    {{ ref('stg_customer') }}
WHERE
    event_type = 'add_on_purchase'
    AND {{ incremental_date_filter('event_date') }}
