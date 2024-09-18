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

class SourceRequirements:
    def __init__(self) -> None:
        self.requirements = {
            'carts_has_products': {
                'source_path': './data_source/carts_has_products.txt',
                'columns': {
                    'shopping_cart_id': {'type': 'object'},
                    'product_id': {'type': 'object'},
                    'option_id': {'type': 'object'},
                    'quantity': {'type': 'int64'}
                }
            },
            'categories': {
                'source_path': './data_source/category.txt',
                'columns': {
                    'category_id': {'type': 'object'},
                    'category_name': {'type': 'object'}
                }
            },
            'options': {
                'source_path': './data_source/option.txt',
                'columns': {
                    'option_id': {'type': 'object'},
                    'option_name': {'type': 'object'}
                }
            },
            'orders': {
                'source_path': './data_source/order.txt',
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
                    'delivery_status': {'type': 'bool'}
                }
            },
            'orders_has_products': {
                'source_path': './data_source/orders_has_products.txt',
                'columns': {
                    'order_id': {'type': 'object'},
                    'product_id': {'type': 'object'},
                    'option_id': {'type': 'object'},
                    'quantity': {'type': 'int64'}
                }
            },
            'orders_paid_creditcard': {
                'source_path': './data_source/orders_paid_creditcard.txt',
                'columns': {
                    'credit_card_number': {'type': 'object'},
                    'order_id': {'type': 'object'}
                }
            },
            'orders_placed_user': {
                'source_path': './data_source/orders_placed_user.txt',
                'columns': {
                    'user_id': {'type': 'object'},
                    'order_id': {'type': 'object'}
                }
            },
            'products_sold_vendor': {
                'source_path': './data_source/product_sold_vendor.txt',
                'columns': {
                    'vendor_id': {'type': 'object'},
                    'product_id': {'type': 'object'}
                }
            },
            'products': {
                'source_path': './data_source/products.txt',
                'columns': {
                    'product_id': {'type': 'object'},
                    'product_name': {'type': 'object'},
                    'descriptions': {'type': 'object'}
                }
            },
            'products_belong_category': {
                'source_path': './data_source/products_belong_category.txt',
                'columns': {
                    'product_id': {'type': 'object'},
                    'category_id': {'type': 'object'}
                }
            },
            'products_has_options': {
                'source_path': './data_source/products_has_options.txt',
                'columns': {
                    'product_id': {'type': 'object'},
                    'option_id': {'type': 'object'},
                    'quantity': {'type': 'int64'},
                    'price': {'type': 'int64'},
                    'on_sale': {'type': 'bool'},
                    'specs': {'type': 'object'}
                }
            },
            'shoppingcarts': {
                'source_path': './data_source/shoppingcart.txt',
                'columns': {
                    'shopping_cart_id': {'type': 'object'},
                    'status': {'type': 'bool'}
                }
            },
            'users': {
                'source_path': './data_source/user.txt',
                'columns': {
                    'user_id': {'type': 'object'},
                    'username': {'type': 'object'},
                    'password': {'type': 'object'},
                    'username': {'type': 'object'},
                    'full_name': {'type': 'object'},
                    'address': {'type': 'object'},
                    'email': {'type': 'object'},
                    'phone': {'type': 'object'}
                }
            },
            'user_has_creditcards': {
                'source_path': './data_source/user_has_creditcard.txt',
                'columns': {
                    'user_id': {'type': 'object'},
                    'credit_card_number': {'type': 'object'}
                }
            },
            'vendors': {
                'source_path': './data_source/vendor.txt',
                'columns': {
                    'vendor_id': {'type': 'object'},
                    'vendor_name': {'type': 'object'},
                    'vendor_phone': {'type': 'object'},
                    'vendor_email': {'type': 'object'}
                }
            }
        }
