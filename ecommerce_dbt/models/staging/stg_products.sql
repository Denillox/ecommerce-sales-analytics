{{ config(materialized='table') }}

SELECT
    product_id,
    TRIM(name) AS name,
    UPPER(category) AS category,
    price,
    brand,
    supplier
FROM dbo.dim_product
WHERE price > 0
