import pandas as pd

class TableTransformation:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def transformToDimCustomer(self):
        df = self.df
        df['contactFullName'] = df['contactFirstName'] + ' ' + df['contactLastName']
        df.drop(['contactFirstName','contactLastName','addressLine2','salesRepEmployeeNumber'], axis=1, inplace=True)
        new_order = ['customerNumber','customerName','contactFullName','phone','addressLine1','city','state','postalCode','country','creditLimit']
        df = df.reindex(columns=new_order)
        df[['customerNumber']] = df[['customerNumber']].astype('string')
        df[['creditLimit']] = df[['creditLimit']].astype('float') 
        return df
    
    def transformToDimDate(self):
        df = self.df
        return df

    def transformToDimEmployee(self):
        df = self.df
        df['Employee_Key'] = df['employeeNumber'].astype('str') + df['officeCode'].astype('str')
        df['Employee_Number'] = df['employeeNumber']
        df["Employee_Name"] = df["firstName"] + " " + df["lastName"]
        df["Email"] = df["email"]
        df["Job_Title"] = df["jobTitle"]
        df["Office_Key"] = df["officeCode"].astype('int')
        columns = [
            "Employee_Key",
            "Employee_Number",
            "Employee_Name",
            "Email",
            "Job_Title",
            "Office_Key"
        ]
        df = df[columns]
        return df

    def transformToDimOffice(self):
        df = self.df
        df.drop(
            [
                "addressLine2",
            ],
            axis=1,
            inplace=True,
        )
        new_order = [
            "officeCode",
            "city",
            "phone",
            "addressLine1",
            "state",
            "country",
            "postalCode",
            "territory",
        ]
        df = df.reindex(columns=new_order)
        return df
    
    def transformToProduct(self):
        df = self.df
        new_order = [
            "productCode",
            "productName",
            "productLine",
            "productScale",
            "productVendor",
            "productDescription",
            "quantityInStock",
            "buyPrice",
            "MSRP",
        ]
        df = df.reindex(columns=new_order)
        df[["quantityInStock"]] = df[["quantityInStock"]].astype("int")
        df[["buyPrice", "MSRP"]] = df[["buyPrice", "MSRP"]].astype("float")
        return df

    def transformToFactSales(self):
        df = self.df
        df["Total_Sale_Amount"] = df["quantityOrdered"] * df["priceEach"]
        df.drop(
            [
                "priceEach",
            ],
            axis=1,
            inplace=True,
        )
        new_order = [
            "orderNumber",
            "productCode",
            "quantityOrdered",
            "Total_Sale_Amount",
        ]
        df = df.reindex(columns=new_order)
        df[["orderNumber"]] = df[["orderNumber"]].astype("int")
        df[["quantityOrdered"]] = df[["quantityOrdered"]].astype("int")
        df[["Total_Sale_Amount"]] = df[["Total_Sale_Amount"]].astype("float")
        return df