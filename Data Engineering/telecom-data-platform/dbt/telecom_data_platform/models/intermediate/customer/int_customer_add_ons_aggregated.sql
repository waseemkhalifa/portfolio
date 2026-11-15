{{ 
    config(
        materialized='ephemeral'
    ) 
}}

SELECT
    customer_id,
    event_date,

    1 AS is_add_on,

    MAX(is_add_on__international_calls) AS is_add_on__international_calls,
    MAX(is_add_on__roaming_pass) AS is_add_on__roaming_pass,
    MAX(is_add_on__extra_data) AS is_add_on__extra_data,
    MAX(is_add_on__netflix_bundle) AS is_add_on__netflix_bundle,
    SUM(add_on_cost) AS add_on_cost
FROM 
    {{ ref('int_customer_add_ons') }}

{% if is_incremental() %}
WHERE 
    {{ incremental_date_filter('event_date') }}
{% endif %}

GROUP BY 
    customer_id, event_date
