{{ config(materialized='table') }}

SELECT
    order_item_id,
    orders_id,
    customer_id,
    product_id,
    date_id,
    quantity,
    unit_price,
    total_amount
FROM dbo.fact_ordereditem
WHERE total_amount > 0