-- models/dim_dates.sql
WITH date_range AS (
    SELECT
        GENERATE_DATE_ARRAY(
            (SELECT MIN(DATE(published_at)) FROM {{ ref('raw_landing') }}),
            (SELECT MAX(DATE(published_at)) FROM {{ ref('raw_landing') }}),
            INTERVAL 1 DAY
        ) AS date_list
)
SELECT
    date AS date_id,
    EXTRACT(DAYOFWEEK FROM date) AS day_of_week,
    EXTRACT(DAY FROM date) AS day,
    EXTRACT(MONTH FROM date) AS month,
    EXTRACT(QUARTER FROM date) AS quarter,
    EXTRACT(YEAR FROM date) AS year
FROM
    date_range,
    UNNEST(date_list) AS date
