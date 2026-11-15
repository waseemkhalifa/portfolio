{% macro incremental_date_filter(date_column) %}

    {% if is_incremental() %}
        {{ date_column }} >= (
            SELECT DATE_SUB(MAX({{ date_column }}), INTERVAL 3 DAY)
            FROM {{ this }}
        )
    {% endif %}

{% endmacro %}
