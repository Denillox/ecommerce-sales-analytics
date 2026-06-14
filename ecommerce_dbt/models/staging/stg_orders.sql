{{ config(materialized='table') }}

SELECT
    orders_id,
    status,
    full_date
FROM dbo.dim_orders
WHERE status IS NOT NULL