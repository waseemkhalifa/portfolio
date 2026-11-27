{% macro incremental_date_filter(date_column) %}
    
    {{ date_column }} >= (
        SELECT DATE_SUB(MAX({{ date_column }}), INTERVAL 3 DAY)
        FROM {{ this }}
    )

{% endmacro %}
