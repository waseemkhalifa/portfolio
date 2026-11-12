{{
    config(
        materialized='view',
        schema='staging',
        tags=['silver', 'staging', 'customer_events']
    )
}}

SELECT
    CAST(event_id AS VARCHAR) AS event_id,
    CAST(customer_id AS VARCHAR) AS customer_id,
    CAST(event_type AS VARCHAR) AS event_type,
    CAST(event_timestamp AS TIMESTAMP) AS event_timestamp,
    CAST(channel AS VARCHAR) AS channel,
    CAST(package_name AS VARCHAR) AS package_name,
    CAST(monthly_charge AS DECIMAL(10, 2)) AS monthly_charge,
    CAST(contract_length_months AS INTEGER) AS contract_length_months,
    CAST(old_package AS VARCHAR) AS old_package,
    CAST(new_package AS VARCHAR) AS new_package,
    CAST(monthly_charge_increase AS DECIMAL(10, 2)) AS monthly_charge_increase,
    CAST(monthly_charge_decrease AS DECIMAL(10, 2)) AS monthly_charge_decrease,
    CAST(add_on_name AS VARCHAR) AS add_on_name,
    CAST(add_on_cost AS DECIMAL(10, 2)) AS add_on_cost,
    CAST(renewal_discount AS DECIMAL(10, 2)) AS renewal_discount,
    CAST(case_type AS VARCHAR) AS case_type,
    CAST(resolved_first_contact AS BOOLEAN) AS resolved_first_contact,
    CAST(churn_reason AS VARCHAR) AS churn_reason
FROM 
    {{ source('silver', 'customer_events') }}
