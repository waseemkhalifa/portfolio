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

    UNION

    SELECT customer_id, event_date
    FROM {{ ref('int_customer_packages_aggregated') }}
)

SELECT
    customers.customer_id,
    customers.event_date,

    STRUCT_PACK(
        is_add_on := COALESCE(add_ons.is_add_on, 0),
        is_package := COALESCE(packages.is_package, 0)
    ) AS customer_event_type_0,

    STRUCT_PACK(
        is_add_on__international_calls := COALESCE(add_ons.is_add_on__international_calls, 0),
        is_add_on__roaming_pass := COALESCE(add_ons.is_add_on__roaming_pass, 0),
        is_add_on__extra_data := COALESCE(add_ons.is_add_on__extra_data, 0),
        is_add_on__netflix_bundle := COALESCE(add_ons.is_add_on__netflix_bundle, 0),
        is_package_upgrade := COALESCE(packages.is_package_upgrade, 0),
        is_package_downgrade := COALESCE(packages.is_package_downgrade, 0)
    ) AS customer_event_type_1,

    STRUCT_PACK(
        add_on_cost := COALESCE(add_ons.add_on_cost, 0)
    ) AS add_on_details,

    STRUCT_PACK(
        package_old := packages.package_old,
        package_new := packages.package_new,
        package_monthly_charge_change := packages.package_monthly_charge_change
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
