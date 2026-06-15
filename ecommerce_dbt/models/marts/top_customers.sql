{{ config(materialized='table') }}

WITH customer_totals AS (
    SELECT
        f.customer_id,
        SUM(f.total_amount) AS total_spend,
        COUNT(DISTINCT f.orders_id) AS total_orders
    FROM dbo.stg_fact f
    GROUP BY f.customer_id
)
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.country,
    c.city,
    ct.total_spend,
    ct.total_orders,
    ROW_NUMBER() OVER (ORDER BY ct.total_spend DESC) AS spend_rank
FROM customer_totals ct
JOIN dbo.stg_customers c ON ct.customer_id = c.customer_id