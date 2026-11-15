{{
    config(
        materialized='ephemeral'
    )
}}

WITH latest_package AS (
    SELECT
        customer_id,
        event_date,
        package_old,
        package_new
    FROM 
        {{ ref('int_customer_packages') }}
    
    {% if is_incremental() %}
    WHERE 
        {{ incremental_date_filter('event_date') }}
    {% endif %}

    QUALIFY
        -- For each customer take the latest package event on the day
        ROW_NUMBER() OVER (PARTITION BY customer_id, event_date ORDER BY event_date DESC) = 1
),

packages_aggregated AS (
    SELECT
        customer_id,
        event_date,

        MAX(is_package_upgrade) AS is_package_upgrade,
        MAX(is_package_downgrade) AS is_package_downgrade,
        SUM(package_monthly_charge_change) AS package_monthly_charge_change
    FROM 
        {{ ref('int_customer_packages') }}
    
    {% if is_incremental() %}
    WHERE 
        {{ incremental_date_filter('event_date') }}
    {% endif %}

    GROUP BY 
        customer_id, event_date
)

SELECT
    packages_aggregated.customer_id,
    packages_aggregated.event_date,
    1 AS is_package,
    packages_aggregated.is_package_upgrade,
    packages_aggregated.is_package_downgrade,
    packages_aggregated.package_monthly_charge_change,

    latest_package.package_old,
    latest_package.package_new
FROM
    packages_aggregated
LEFT JOIN 
    latest_package
    ON packages_aggregated.customer_id = latest_package.customer_id
    AND packages_aggregated.event_date = latest_package.event_date
