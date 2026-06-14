{{ config(materialized='table') }}

SELECT
    date_id,
    full_date,
    year,
    month,
    day,
    quarter,
    weekday,
    weekday_number
FROM dbo.dim_date