import fileAP
import fileUtils
from datetime import datetime

def manage_inventory(currentUser:str, fileExt:str):
    while True:
        userInput = str(input(f'Inventory Management\n1 - Ingredients Stock\n2 - Hardware Stock\nE - Exit\n{currentUser} - '))
        if userInput == '1':
            functionName = "Ingredient Management"
            tableName = 'Ingredients'
            csvBool, filename = fileAP.is_fileType("Ingredient_supply", fileExt)
            if csvBool:
                fileUtils.init_dbtools(currentUser, functionName, tableName, filename, fileExt)

            elif csvBool is False:
                filename = fileAP.file_create(filename, fileExt)
                print("Ingredient Table Created")
                continue

        elif userInput == '2':
            functionName = "Hardware Management"
            tableName = 'Hardware'
            csvBool, filename = fileAP.is_fileType("Hardware_supply", fileExt)
            if csvBool:
                fileUtils.init_dbtools(currentUser, functionName, tableName, filename, fileExt)

            elif csvBool is False:
                filename = fileAP.file_create(filename, fileExt)
                print("Hardware Table Created")
                continue

        elif userInput.upper() == 'E':
            break

        else:
            print("Invalid Input")

def order_management():
    goods = fileAP.dataframe(fileAP.file_read("Goods_information", ".csv"))
    orders = fileAP.dataframe(fileAP.file_read("Orders", ".csv"))  # Load the existing orders
    pending_orders = [order for order in orders if order["Status"] == "Pending"]  # Filter pending orders
    now = datetime.now()
    orderListItem = []
    orderListNum = []
    if len(pending_orders) == 0:
        print("No pending orders to approve.")
        return
    
    # Loop through each pending order for approval
    for order in pending_orders:
        print(f'Order No: {order["No.Order"]}, Order ID: {order["OrderID"]}')
        print(f'Order Details: {order["Order_details"]}')
        print("Pending Approval\n")
        
        # Manager input for approving/rejecting
        userInput = input("Enter 'A' to approve or 'R' to reject this order or 'P' to remain as pending: ").strip().upper()
        
        if userInput.upper() == 'A':
            order["Status"] = "Completed"
            orderList = order["Order_details"].split('; ')
            totalCost = order["Cost"]
            print(f"Order {order['OrderID']} approved and marked as Completed.\n")
            # Create Record for Finance Book

            for o in orderList:
                orderListItem.append(fileUtils.word_split(o))
                orderListNum.append(fileUtils.digit_split(o))
            for i in range(len(orderListItem)):
                for g in goods:
                    if orderListItem[i].strip() == g['Name']:
                        g.update({'Quantity' : str(int(g['Quantity']) - int(orderListNum[i]))})
            fileUtils.tableFormat("Goods Information", goods)
            pause = input('=====[Enter to Continue]=====')
            
            existing_finance = fileAP.dataframe(fileAP.file_read("Finance_records", ".csv"))    
            if existing_finance == None:
                fin_id = 1
            else:
                fin_id = fileUtils.digit_split(existing_finance[-1]['FinanceID']) + 1
            finance_record = {
                "FinanceID": f'FID{fin_id:04}',
                "Flow Type": "In",
                "Cash Flow": f'{totalCost}',
                "Date(DDMMYYYY)": now.strftime("%d-%m-%Y"),
                "Time": now.strftime("%H:%M:%S")
            }

            fileAP.file_write("Finance_records",".csv", [finance_record])

        elif userInput.upper() == 'P':
            order["Status"] = "Pending"
            print(f"Order {order['OrderID']} pending and marked as Rejected.\n")
            # Create Record for Finance Book

        elif userInput.upper() == 'R':
            order["Status"] = "Rejected"
            print(f"Order {order['OrderID']} rejected and marked as Rejected.\n")
        else:
            print("Invalid input. Skipping this order.\n")
            continue

    # Save the updated orders back to the Orders.csv file
    fileAP.file_rewrite("Orders", ".csv", orders)  # Assuming file_write overwrites the file with updated data
    print("All orders processed.")

def request_tickets(currentUser:str, fileExt:str):
    requests = fileAP.dataframe(fileAP.file_read("Ingredient_request", ".csv"))
    while True:
        fileUtils.tableFormat("Ingredient Requests", requests)
        userInput = str(input(f'1 - Respond to All\nE - Exit\n{currentUser} - '))
        if userInput == '1':
            for request in requests:
                if request["RequestStatus"] == "Not fulfilled":
                    while True:
                        userFulfillment = str(input(f'{request} Fulfilled? [Y/N]'))
                        if userFulfillment.upper() == 'Y':
                            request.update({"RequestStatus":"Fulfilled"})
                            break
                        elif userFulfillment.upper() == "N":
                            request.update({"RequestStatus":"Not fulfilled"})
                            break
                        else:
                            print("Invalid Input")
            
            fileAP.file_rewrite("Ingredient_request", fileExt, requests)

        elif userInput.upper() == 'E':
            break
        
        else:
            print("Invalid Input")
    return

def manager_response(currentUser:str):
    reviews = fileAP.dataframe(fileAP.file_read("Customer_reviews", ".csv"))
    while True:
        fileUtils.tableFormat("Customer Reviews", reviews)
        userInput = str(input(f'1 - Respond to All\nE - Exit\n{currentUser} - '))
        if userInput == '1':
            
            for i in reviews:
                if i["ReviewStatus"] == 'Open':
                    print(f'Currently responding to {i["OrderID"]}')
                    while True:
                        response = str(input("Enter your response: "))
                        if ',' in response:
                            print("Character \",\" is invalid")
                        else:
                            break
                    i.update({"ManagerResponse":response})
                    i.update({"ReviewStatus":"Resolved"})
                    print("Response returned. ")

                else:
                    print("This review has been resolved.")

            fileUtils.tableFormat("Customer Reviews", reviews)
            fileAP.file_rewrite("Customer_reviews", ".csv", reviews)
        
        elif userInput.upper() == 'E':
            break

        else:
            print("Invalid Input")

def order_inventory(currentUser:str, fileExt:str):
    fileBool, filename = fileAP.is_fileType("Ordered_list", fileExt)
    if fileBool:
        pass
    else:
        with open(filename, "x") as file:
            file = file

    while True:
        userInput = str(input(f'1 - Order Ingredients\n2 - Add Suppliers\n{currentUser} - '))
        if userInput == "1":
            ingredientSupplier = fileAP.dataframe(fileAP.file_read("Ingredient_supply", fileExt))
            fileUtils.tableFormat("Ingredient Suppliers", ingredientSupplier)
            ingredient = str(input("Enter Ingredient ID to order: "))
            for i in ingredientSupplier:
                if i['UUID'] == ingredient:
                    found = True
                    price = i['Price(RM)']
                    supplier = i['Supplier']
                    quantity = str(input(f'Ingredient: {i['Name']} | Price: RM{i['Price(RM)']} | Supplier: {i['Supplier']}\nQuantity: '))
                    break
                else:
                    found = False

            if found:
                ordered_list = fileAP.dataframe(fileAP.file_read('Ordered_list', fileExt))
                num, unit = price.split('/')
                totalCost = f'RM{int(num)*int(quantity)}'
                totalQuantity = f'{quantity}{unit}'
                print(f'Total: {totalCost} | Quantity: {totalQuantity}')
                orderedRecord = {
                    'RecordID': f'RID{1:04}' if ordered_list is None else f'{fileUtils.digit_split(ordered_list[-1]['RecordID']) + 1:04}',
                    'Cost':totalCost,
                    'Quantity':totalQuantity,
                    'Supplier':supplier,
                    'Status':'Pending'
                    }
                fileAP.file_write('Ordered_list', fileExt, [orderedRecord])
                now = datetime.now()

                existing_finance = fileAP.dataframe(fileAP.file_read("Finance_records", ".csv"))    
                if existing_finance == None:
                    fin_id = 1
                else:
                    fin_id = fileUtils.digit_split(existing_finance[-1]['No.Order']) + 1
                finance_record = {
                    "FinanceID": f'FID{fin_id:04}',
                    "Flow Type": "Out",
                    "Cash Flow": totalCost,
                    "Date(DDMMYYYY)": now.strftime("%d-%m-%Y"),
                    "Time": now.strftime("%H:%M:%S")
                }

                fileAP.file_write("Finance_records",".csv", [finance_record])

            else:
                print("Item Not Found.")

        elif userInput == '2':
            ingredientSupplier = fileAP.dataframe(fileAP.file_read("Ingredient_supply", fileExt))
            fileUtils.tableFormat("Ingredient Suppliers", ingredientSupplier)
            action = str(input("1 - Add Ingredient\n2 - Remove Ingredient"))
            if action == '1':
                pass
            elif action == '2':

                for i in range(0, len(ingredientSupplier)):
                    continue
            elif action.upper() == 'E':
                break
            else:
                print("Invalid Input")

        elif userInput.upper() == "E":
            break
        else:
            print("Invalid Input")

def manage_finance(currentUser:str):
    fileExt = '.csv'

    while True:
        userInput = str(input(f'1 - Manage Finance\nE - Exit\n{currentUser} - '))
        if userInput == '1':
            functionName = "Finance Management"
            tableName = 'Finances'
            fileBool, filename = fileAP.is_fileType("Finance_records", fileExt)
            if fileBool:
                fileUtils.init_dbtools(currentUser, functionName, tableName, filename, fileExt)

            elif fileBool is False:
                filename = fileAP.file_create(filename, fileExt)
                print("Finance Table Created")
                continue

        elif userInput.upper() == 'E':
            break
        else:
            print("Invalid Input.")

def init_manager(currentUser:str):
    managerNames = ["Manage Inventory", "Order Management", "Tickets Request", "Manager Response", "Order Inventory", "Manage Finance"]
    fileExt = ".csv"
    while True:
        for i in range(len(managerNames)):
                print(f'{i+1} - {managerNames[i]}')
        print('E - Exit')

        action = str(input(f'{currentUser} - '))

        if action == '1':
            manage_inventory(currentUser, fileExt)

        elif action == '2':
            order_management()

        elif action == '3':
            request_tickets(currentUser, fileExt)

        elif action == '4':
            manager_response(currentUser)

        elif action == '5':
            order_inventory(currentUser, fileExt)

        elif action == '6':
            manage_finance(currentUser)

        elif action.upper() == 'E':
            print("Exiting Cashier Page.")
            break

        else:
            print("Invalid Input.")

# For Testing         
if __name__ == '__main__':
    init_manager("Test")

