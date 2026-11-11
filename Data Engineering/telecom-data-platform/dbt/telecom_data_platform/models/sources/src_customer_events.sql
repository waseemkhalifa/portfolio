SELECT
    /* event_id,
    customer_id,
    event_type,
    event_timestamp,
    channel,
    package_name,
    monthly_charge,
    contract_length_months,
    old_package,
    new_package,
    monthly_charge_increase,
    monthly_charge_decrease,
    add_on_name,
    add_on_cost,
    renewal_discount,
    case_type,
    resolved_first_contact,
    churn_reason */
    *
FROM read_parquet('/home/waseem/Documents/Self-Development/git_repos/portfolio/Data Engineering/telecom-data-platform/data/silver/customer_events/*.parquet')
