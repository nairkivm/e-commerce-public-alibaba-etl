import pandas as pd

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

from utils.helper import Helper
from utils.validate_data import getDataValidation
from utils.destination_requirements import DestinationRequirements

class TableTransformation:
    def __init__(self, dfs: dict[str, pd.DataFrame]):
        # Data preprocessing
        for table_name in dfs.keys():
            print(f"Data Preprocessing for '{table_name}'")
            dfs[table_name].columns = [str(col).strip() for col in dfs[table_name].columns]
            getDataValidation(dfs[table_name], table_name)
        self.dfs = dfs
    
    def transformToFactOrders(self) -> pd.DataFrame:
        # Data wrangling for 'orders' table
        print(f"Data Wrangling for 'orders'")
        orders_df = self.dfs['orders'].copy()
        orders_df = Helper.assignProperType(orders_df, "orders")
        getDataValidation(orders_df, "orders")
        # Data wrangling for 'orders_placed_user' table
        print(f"Data Wrangling for 'orders_placed_user'")
        orders_user_df = self.dfs['orders_placed_user'].copy()
        orders_user_df = Helper.assignProperType(orders_user_df, "orders_placed_user")
        getDataValidation(orders_user_df, "orders_placed_user")        
        # Data wrangling for 'orders_paid_creditcard' table
        print(f"Data Wrangling for 'orders_paid_creditcard'")
        order_cards_df = self.dfs['orders_paid_creditcard'].copy()
        order_cards_df = Helper.assignProperType(order_cards_df, "orders_paid_creditcard")
        getDataValidation(order_cards_df, "orders_paid_creditcard")
        # Data Transformation
        print(f"Data Transformation for 'store.fact_orders'")
        df = pd.merge(
            orders_df,
            orders_user_df,
            how='left',
            on=['order_id']
        )
        df = pd.merge(
            df,
            order_cards_df,
            how='left',
            on=['order_id']
        )
        getDataValidation(df, "store.fact_orders", DestinationRequirements().requirements)
        return df
    
    def transformToFactOrderDetails(self) -> pd.DataFrame:
        # Data wrangling for 'orders_has_products' table
        print(f"Data Wrangling for 'orders_has_products'")
        order_details_df = self.dfs['orders_has_products'].copy()
        order_details_df = Helper.assignProperType(order_details_df, "orders_has_products")
        getDataValidation(order_details_df, "orders_has_products")
        # Data wrangling for 'products_has_options' table
        print(f"Data Wrangling for 'products_has_options'")
        products_df = self.dfs['products_has_options'].copy()        
        products_df = products_df[['option_id', 'price']]
        products_df = Helper.assignProperType(products_df, "products_has_options")
        getDataValidation(products_df, "products_has_options")        
        # Data Transformation
        print(f"Data Transformation for 'store.fact_order_details'")
        df = pd.merge(
            order_details_df,
            products_df,
            how='left',
            on=['option_id']
        )
        df['raw_cost'] = df['price'].multiply(df['quantity'])
        df = df.drop(columns=['price'])
        getDataValidation(df, "store.fact_order_details", DestinationRequirements().requirements)
        return df
    
    def transformToDimProducts(self) -> pd.DataFrame:
        # Data wrangling for 'products' table
        print(f"Data Wrangling for 'products'")
        products_df = self.dfs['products'].copy()
        products_df = Helper.assignProperType(products_df, "products")
        getDataValidation(products_df, "products")
        # Data wrangling for 'products_belong_category' table
        print(f"Data Wrangling for 'products_belong_category'")
        products_category_df = self.dfs['products_belong_category'].copy()
        products_category_df = Helper.assignProperType(products_category_df, "products_belong_category")
        getDataValidation(products_category_df, "products_belong_category") 
        # Data wrangling for 'categories' table
        print(f"Data Wrangling for 'categories'")
        category_df = self.dfs['categories'].copy()
        category_df = Helper.assignProperType(category_df, "categories")
        getDataValidation(products_category_df, "categories") 
        # Data wrangling for 'products_has_options' table
        print(f"Data Wrangling for 'products_has_options'")
        products_options_df = self.dfs['products_has_options'].copy()
        products_options_df = Helper.assignProperType(products_options_df, "products_has_options")
        getDataValidation(products_options_df, "products_has_options") 
        # Data wrangling for 'options' table
        print(f"Data Wrangling for 'options'")
        options_df = self.dfs['options'].copy()
        options_df = Helper.assignProperType(options_df, "options")
        getDataValidation(options_df, "options") 
        # Data Transformation
        print(f"Data Transformation for 'store.dim_products'")
        df = pd.merge(
            products_df,
            products_category_df,
            how='left',
            on=['product_id']
        )
        df = pd.merge(
            df,
            category_df,
            how='left',
            on=['category_id']
        )
        df = pd.merge(
            df,
            products_options_df,
            how='left',
            on=['product_id']
        )
        df = pd.merge(
            df,
            options_df,
            how='left',
            on=['option_id']
        )
        getDataValidation(df, "store.dim_products", DestinationRequirements().requirements)
        return df
    
    def transformToDimUsers(self) -> pd.DataFrame:
        # Data wrangling for 'users' table
        print(f"Data Wrangling for 'users'")
        users_df = self.dfs['users'].copy()
        users_df = Helper.assignProperType(users_df, "users")
        getDataValidation(users_df, "users")
        # Data wrangling for 'user_has_creditcards' table
        print(f"Data Wrangling for 'user_has_creditcards'")
        users_creditcard_df = self.dfs['user_has_creditcards'].copy()
        users_creditcard_df = Helper.assignProperType(users_creditcard_df, "user_has_creditcards")
        getDataValidation(users_creditcard_df, "user_has_creditcards") 
        # Data Transformation
        print(f"Data Transformation for 'store.dim_users'")
        df = pd.merge(
            users_df,
            users_creditcard_df,
            how='left',
            on=['user_id']
        )
        getDataValidation(df, "store.dim_users", DestinationRequirements().requirements)
        return df
    
    def transformToDimVendors(self) -> pd.DataFrame:
        # Data wrangling for 'vendors' table
        print(f"Data Wrangling for 'vendors'")
        vendors_df = self.dfs['vendors'].copy()
        vendors_df = Helper.assignProperType(vendors_df, "vendors")
        getDataValidation(vendors_df, "vendors")
        # Data Transformation
        print(f"Data Transformation for 'store.dim_vendors'")
        df = vendors_df
        getDataValidation(df, "store.dim_vendors", DestinationRequirements().requirements)
        return df
    
    def transformToDimVendors(self) -> pd.DataFrame:
        # Data wrangling for 'vendors' table
        print(f"Data Wrangling for 'vendors'")
        vendors_df = self.dfs['vendors'].copy()
        vendors_df = Helper.assignProperType(vendors_df, "vendors")
        getDataValidation(vendors_df, "vendors")
        # Data Transformation
        print(f"Data Transformation for 'store.dim_vendors'")
        df = vendors_df
        getDataValidation(df, "store.dim_vendors", DestinationRequirements().requirements)
        return df
    
    def transformToFactCartsProducts(self) -> pd.DataFrame:
        # Data wrangling for 'carts_has_products' table
        print(f"Data Wrangling for 'carts_has_products'")
        carts_products_df = self.dfs['carts_has_products'].copy()
        carts_products_df = Helper.assignProperType(carts_products_df, "carts_has_products")
        # getDataValidation(carts_products_df, "carts_has_products")
        # Data Transformation
        print(f"Data Transformation for 'store.fact_carts_has_products'")
        df = carts_products_df
        getDataValidation(df, "store.fact_carts_has_products", DestinationRequirements().requirements)
        return df
    
    def transformToFactCarts(self) -> pd.DataFrame:
        # Data wrangling for 'shoppingcarts' table
        print(f"Data Wrangling for 'shoppingcarts'")
        carts_df = self.dfs['shoppingcarts'].copy()
        carts_df = Helper.assignProperType(carts_df, "shoppingcarts")
        # getDataValidation(carts_df, "shoppingcarts")
        # Data Transformation
        print(f"Data Transformation for 'store.fact_shoppingcarts'")
        df = carts_df
        getDataValidation(df, "store.fact_shoppingcarts", DestinationRequirements().requirements)
        return df
    
    def transformToFactProductSoldVendor(self) -> pd.DataFrame:
        # Data wrangling for 'products_sold_vendor' table
        print(f"Data Wrangling for 'products_sold_vendor'")
        products_sold_vendors_df = self.dfs['products_sold_vendor'].copy()
        products_sold_vendors_df = Helper.assignProperType(products_sold_vendors_df, "products_sold_vendor")
        # getDataValidation(products_sold_vendors_df, "products_sold_vendor")
        # Data Transformation
        print(f"Data Transformation for 'store.fact_products_sold_vendor'")
        df = products_sold_vendors_df
        getDataValidation(df, "store.fact_products_sold_vendor", DestinationRequirements().requirements)
        return df