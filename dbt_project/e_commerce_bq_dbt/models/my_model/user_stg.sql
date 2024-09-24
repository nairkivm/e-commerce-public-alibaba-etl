{{ config(materialized='view') }}

SELECT
    user_id,
    username,
    full_name,
    address,
    email,
    phone,
    credit_card_number
FROM `store.dim_users`