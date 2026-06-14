{{ config(materialized='table') }}

SELECT
    p.category,
    SUM(f.total_amount) AS total_revenue,
    SUM(f.quantity) AS total_units_sold
FROM dbo.stg_products p
INNER JOIN dbo.stg_fact f
ON p.product_id = f.product_id
GROUP BY p.category