{{ config(materialized='table') }}

SELECT
    us.user_id,
    us.full_name,
    SUM(cos.total_cost) AS total_revenue
FROM {{ ref('user_stg') }} AS us
JOIN {{ ref('clean_orders_stg')}} AS cos 
    ON us.user_id = cos.user_id
GROUP BY
    us.user_id,
    us.full_name