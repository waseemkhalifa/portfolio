{{
    config(
        materialized='view',
        schema='mart',
        tags=['silver', 'mart', 'customer_events']
    )
}}

SELECT *
FROM {{ ref('int_customer_add_ons') }}
