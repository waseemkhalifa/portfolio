{{
    config(
        materialized='incremental',
        schema='intermediate',
        tags=['silver', 'intermediate', 'customer_events']
    )
}}

SELECT
    customer_id,
    event_id,
    event_timestamp,
    channel,
    add_on_name,
    add_on_cost,

    IF(LOWER(event_type) = 'international calls', 1, 0) AS is_international_calls,
    IF(LOWER(event_type) = 'roaming pass', 1, 0) AS is_roaming_pass,
    IF(LOWER(event_type) = 'extra data', 1, 0) AS is_extra_data,
    IF(LOWER(event_type) = 'netflix bundle', 1, 0) AS is_netflix_bundle

FROM
    {{ ref('stg_customer_events') }}
WHERE event_type = 'add_on_purchase'
    
    {% if is_incremental() %}
    AND event_timestamp > (SELECT MAX(event_timestamp) FROM {{ this }})
    {% endif %}
