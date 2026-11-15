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
    old_package AS package_old,
    new_package AS package_new,
    IF(LOWER(event_type) = 'package_upgrade', 1, 0) AS is_package_upgrade,
    IF(LOWER(event_type) = 'package_downgrade', 1, 0) AS is_package_downgrade,

    CASE
        WHEN LOWER(event_type) = 'package_upgrade'
            THEN monthly_charge_increase
        WHEN LOWER(event_type) = 'package_downgrade'
            THEN monthly_charge_decrease * -1
    END AS package_monthly_charge_change

FROM
    {{ ref('stg_customer') }}
WHERE
    event_type IN ('package_upgrade', 'package_downgrade')
    AND {{ incremental_date_filter('event_date') }}
