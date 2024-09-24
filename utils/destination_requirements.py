import sys
import os
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '..'
        )
    )
)

class DestinationRequirements:
    def __init__(self) -> None:
        self.credentials_path = './c_destination.json'
        self.requirements = {
            'store.fact_orders': {
                'source_tables': [
                    'orders',
                    'orders_placed_user',
                    'orders_paid_creditcard'
                ],
                'columns': {
                    'order_id': {'type': 'object'},
                    'total_item': {'type': 'int64'},
                    'shipping_fee': {'type': 'float64'},
                    'tax': {'type': 'float64'},
                    'total_cost': {'type': 'float64'},
                    'order_date': {'type': 'datetime64[ns]'},
                    'delivery_date': {'type': 'datetime64[ns]'},
                    'ship_name': {'type': 'object'},
                    'ship_address': {'type': 'object'},
                    'tracking_number': {'type': 'object'},
                    'delivery_status': {'type': 'bool'},
                    'user_id': {'type': 'object'},
                    'credit_card_number': {'type': 'object'},
                }
            },
            'store.fact_order_details': {
                'source_tables': [
                    'orders_has_products',
                    'products_has_options'
                ],
                'columns': {
                    'order_id': {'type': 'object'},
                    'product_id': {'type': 'object'},
                    'option_id': {'type': 'object'},
                    'quantity': {'type': 'int64'},
                    'raw_cost': {'type': 'int64'},
                }
            },
            'store.dim_products': {
                'source_tables': [
                    'products',
                    'products_belong_category',
                    'categories',
                    'products_has_options',
                    'options'
                ],
                'columns': {
                    'product_id': {'type': 'object'},
                    'product_name': {'type': 'object'},
                    'descriptions': {'type': 'object'},
                    'category_id': {'type': 'object'},
                    'category_name': {'type': 'object'},
                    'option_id': {'type': 'object'},
                    'quantity': {'type': 'int64'},
                    'price': {'type': 'int64'},
                    'on_sale': {'type': 'bool'},
                    'specs': {'type': 'object'},
                    'option_name': {'type': 'object'}
                }
            },
            'store.dim_users': {
                'source_tables': [
                    'users',
                    'user_has_creditcards'
                ],
                'columns': {
                    'user_id': {'type': 'object'},
                    'username': {'type': 'object'},
                    'password': {'type': 'object'},
                    'full_name': {'type': 'object'},
                    'address': {'type': 'object'},
                    'email': {'type': 'object'},
                    'phone': {'type': 'object'},
                    'credit_card_number': {'type': 'object'}
                }
            },
            'store.dim_vendors': {
                'source_tables': [
                    'vendors'
                ],
                'columns': {
                    'vendor_id': {'type': 'object'},
                    'vendor_name': {'type': 'object'},
                    'vendor_phone': {'type': 'object'},
                    'vendor_email': {'type': 'object'}
                }
            },
            'store.fact_carts_has_products': {
                'source_tables': [
                    'carts_has_products'
                ],
                'columns': {
                    'shopping_cart_id': {'type': 'object'},
                    'product_id': {'type': 'object'},
                    'option_id': {'type': 'object'},
                    'quantity': {'type': 'int64'}
                }
            },
            'store.fact_shoppingcarts': {
                'source_tables': [
                    'shoppingcarts'
                ],
                'columns': {
                    'shopping_cart_id': {'type': 'object'},
                    'status': {'type': 'bool'}
                }
            },
            'store.fact_products_sold_vendor': {
                'source_tables': [
                    'products_sold_vendor'
                ],
                'columns': {
                    'vendor_id': {'type': 'object'},
                    'product_id': {'type': 'object'}
                }
            },
        }
