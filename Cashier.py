"""
Product Display: Access a digital menu or product catalogue to view available items (In Main Script).
Manage Discount: Add, delete, or modify discounts or promotions for items.
Transaction Completion: Generate receipts for customers.
Reporting: Generate reports on sales performance and product popularity.
"""
import fileAP
import fileUtils
from datetime import datetime

def price_management(currentUser: str, fileExt: str):
    functionName = "Price Management"
    tableName = "Prices"
    csvBool, filename = fileAP.is_fileType("price_management", fileExt)
    
    if csvBool:
        data = fileAP.file_read(filename, fileExt)
        if not data or len(data) <= 1:  # If file is empty or only has headers
            prices = []
            products = fileAP.dataframe(fileAP.file_read("Goods_information", ".csv"))
            
            for i in products:
                price = {
                    'ProductID': i['ProductID'],
                    'Name': i['Name'],
                    'Original Price': f"RM{i['Price(RM)']}",
                    'Discount(%)': '0',
                    'New Price': f"RM{i['Price(RM)']}"
                }
                prices.append(price)
            
            fileAP.file_rewrite(filename, fileExt, prices)
        fileUtils.init_dbtools(currentUser, functionName, tableName, filename, fileExt)
    elif not csvBool:
        prices = []
        products = fileAP.dataframe(fileAP.file_read("Goods_information", ".csv"))
        
        for i in products:
            price = {
                'ProductID': i['ProductID'],
                'Name': i['Name'],
                'Original Price': f"RM{i['Price(RM)']}",
                'Discount(%)': '0',
                'New Price': f"RM{i['Price(RM)']}"
            }
            prices.append(price)
        
        fileAP.file_write("Price_management", fileExt, prices)
        price_management(currentUser, fileExt)
    else:
        print("Error at price_management(currentUser, fileExt)")

def transaction_management(currentUser: str, fileExt: str):
    functionName = "Transaction Management"
    tableName = "Transactions"
    csvBool, filename = fileAP.is_fileType("payment_log", fileExt)
    
    if csvBool:
        data = fileAP.file_read(filename, fileExt)
        if not data or len(data) <= 1:  # If file is empty or only has headers
            initial_transaction = [{
                'TransactionID': 'INIT0001',
                'Date': datetime.now().strftime('%Y-%m-%d'),
                'CustomerID': 'N/A',
                'TotalAmount': 'RM0.00',
                'Status': 'SYSTEM_INIT'
            }]
            fileAP.file_rewrite(filename, fileExt, initial_transaction)
        fileUtils.init_dbtools(currentUser, functionName, tableName, filename, fileExt)
    elif not csvBool:
        initial_transaction = [{
            'TransactionID': 'INIT0001',
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'CustomerID': 'N/A',
            'TotalAmount': 'RM0.00',
            'Status': 'SYSTEM_INIT'
        }]
        fileAP.file_create(filename, fileExt)
        fileAP.file_write(filename, fileExt, initial_transaction)
        fileUtils.init_dbtools(currentUser, functionName, tableName, filename, fileExt)
    else:
        print("Error at transaction_management(currentUser, fileExt)")

def report_management(currentUser: str, fileExt: str):
    functionName = "Report Management"
    tableName = "Reports"
    csvBool, filename = fileAP.is_fileType("report_management", fileExt)
    
    try:
        if csvBool:
            data = fileAP.file_read(filename, fileExt)
            if not data or len(data) <= 1:  # If file is empty or only has headers
                initial_report = [{
                    'ReportID': 'RPT0001',
                    'Date': datetime.now().strftime('%Y-%m-%d'),
                    'Type': 'Daily Sales',
                    'TotalSales': 'RM0.00',
                    'ItemsSold': '0',
                    'Status': 'INITIALIZED'
                }]
                fileAP.file_rewrite(filename, fileExt, initial_report)
            fileUtils.init_dbtools(currentUser, functionName, tableName, filename, fileExt)
        elif not csvBool:
            initial_report = [{
                'ReportID': 'RPT0001',
                'Date': datetime.now().strftime('%Y-%m-%d'),
                'Type': 'Daily Sales',
                'TotalSales': 'RM0.00',
                'ItemsSold': '0',
                'Status': 'INITIALIZED'
            }]
            fileAP.file_create(filename, fileExt)
            fileAP.file_write(filename, fileExt, initial_report)
            fileUtils.init_dbtools(currentUser, functionName, tableName, filename, fileExt)
        else:
            print("Error at report_management(currentUser, fileExt)")
    except Exception as e:
        print(f"Error in report management: {str(e)}")
        print("Creating new report file with initial data...")
        try:
            initial_report = [{
                'ReportID': 'RPT0001',
                'Date': datetime.now().strftime('%Y-%m-%d'),
                'Type': 'Daily Sales',
                'TotalSales': 'RM0.00',
                'ItemsSold': '0',
                'Status': 'INITIALIZED'
            }]
            fileAP.file_create(filename, fileExt)
            fileAP.file_write(filename, fileExt, initial_report)
            fileUtils.init_dbtools(currentUser, functionName, tableName, filename, fileExt)
        except Exception as e:
            print(f"Failed to create new report file: {str(e)}")

def init_cashier(currentUser: str):
    cashierNames = ["Manage Prices", "Manage Transactions", "Manage Reports"]
    fileExt = ".csv"
    
    while True:
        try:
            print("\nCashier Management System")
            print("-" * 25)
            for i in range(len(cashierNames)):
                print(f'{i+1} - {cashierNames[i]}')
            print('E - Exit')
            
            action = input(f'{currentUser} - ').upper()
            
            if action == '1':
                price_management(currentUser, fileExt)
            elif action == '2':
                transaction_management(currentUser, fileExt)
            elif action == '3':
                report_management(currentUser, fileExt)
            elif action == 'E':
                print("Exiting Cashier Page.")
                break
            else:
                print("Invalid Input. Please try again.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try again.")

if __name__ == '__main__':
    init_cashier("Test")