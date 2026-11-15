{{
    config(
        materialized='incremental',
        schema='intermediate',
        tags=['silver', 'intermediate', 'customer']
    )
}}

WITH customers AS (
    SELECT customer_id, event_date
    FROM {{ ref('int_customer_add_ons_aggregated') }} 
    WHERE {{ incremental_date_filter('event_date') }}

    UNION

    SELECT customer_id, event_date
    FROM {{ ref('int_customer_packages_aggregated') }} 
    WHERE {{ incremental_date_filter('event_date') }}
),

SELECT
    customers.customer_id,
    customers.event_date,

    STRUCT(
        add_ons.is_add_on,
        packages.is_package
    ) AS customer_event_type_0,

    STRUCT(
        add_ons.is_add_on__international_calls,
        add_ons.is_add_on__roaming_pass,
        add_ons.is_add_on__extra_data,
        add_ons.is_add_on__netflix_bundle,
        packages.is_package_upgrade,
        packages.is_package_downgrade,
    ) AS customer_event_type_1,

    STRUCT(
        add_ons.add_on_cost
    ) AS add_on_details,

    STRUCT(
        packages.package_old,
        packages.package_new,
        packages.package_monthly_charge_change
    ) AS package_details
FROM
    customers
LEFT JOIN
    {{ ref('int_customer_add_ons_aggregated') }} AS add_ons
    ON customers.customer_id = add_ons.customer_id
    AND customers.event_date = add_ons.event_date
LEFT JOIN
    {{ ref('int_customer_packages_aggregated') }} AS packages
    ON customers.customer_id = packages.customer_id
    AND customers.event_date = packages.event_date
