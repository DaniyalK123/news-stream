-- models/dim_sources.sql
SELECT DISTINCT
    source_id,
    source_name
FROM
    {{ ref('raw_landing') }}
