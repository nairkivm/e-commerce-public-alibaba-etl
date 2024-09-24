{{ config(materialized='view') }}

SELECT
    order_id,
    total_item,
    shipping_fee,
    tax,
    total_cost,
    order_date,
    delivery_date,
    ship_name,
    ship_address,
    tracking_number,
    delivery_status,
    user_id,
    credit_cart_number
FROM `store.fact_orders`
WHERE delivery_status = True;