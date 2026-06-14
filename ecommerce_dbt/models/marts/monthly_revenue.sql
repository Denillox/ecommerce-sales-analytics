{{ config(materialized='table') }}

SELECT
    d.year,
    d.month,
    DATENAME(MONTH, d.full_date) AS month_name,
    SUM(f.total_amount) AS total_revenue
FROM dbo.stg_fact f 
INNER JOIN dbo.stg_date d
ON f.date_id = d.date_id
GROUP BY d.year, d.month, DATENAME(MONTH, d.full_date)