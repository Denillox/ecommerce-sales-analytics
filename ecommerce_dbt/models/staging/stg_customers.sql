{{ config(materialized='table') }}

SELECT
    customer_id,
    TRIM(first_name) AS first_name,
    TRIM(last_name) AS last_name,
    LOWER(email) AS email,
    address,
    country,
    phone_number,
    city,
    signup_date
FROM dbo.dim_customer
WHERE email IS NOT NULL