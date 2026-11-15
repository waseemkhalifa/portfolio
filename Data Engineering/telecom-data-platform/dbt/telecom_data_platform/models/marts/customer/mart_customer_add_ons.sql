{{
    config(
        materialized='view',
        schema='mart',
        tags=['silver', 'mart', 'customer']
    )
}}

SELECT *
FROM {{ ref('int_customer_add_ons') }}
