"""
Customer Account Management: Create, manage, login and update personal information. ------[Completed]
Product Browsing: Customers can explore a variety of bakery items available for purchase. [Completed]
Cart Management: Customers can add, remove, or modify items in their shopping cart. ------[Completed]
Order Tracking: Monitor the status of placed orders. -------------------------------------[Completed]
Product Review: Customers can share feedback and suggestions about purchased items. ------[Completed]
Payment Procedure: Customers can pay after their orders have been confirmed to have stock.[Completed]
"""
import fileUtils
import fileAP
import os
from datetime import datetime
import re
import securitySys as secSys
import paymentSys as paySys

# Supporting Functions
def is_valid_username(valid_user_format, username:str):
    if re.match(valid_user_format, username):
        return True
    else:
        return False
        
def is_valid_email_format(valid_email_format, email:str):
    if re.match(valid_email_format, email):
        return True
    else:
        return False

def menuFormat(const=5, symbol=' '):
    items = fileAP.dataframe(fileAP.file_read("Goods_information", ".csv"))
    prices = fileAP.dataframe(fileAP.file_read("Price_management", ".csv"))
    keys = list(items[0].keys())
    key = []
    lengthList = []
    menuHeading = '[Products]\n'

    # Longest Text Locator
    
    for n in range(len(keys)):
        max_len = len(keys[n])
        if n == 0 or n == 1 or n == 6:
            for i in [item[keys[n]] for item in items]:
                if len(i) > max_len:
                    max_len = len(i)
            lengthList.append(max_len)
            key.append(keys[n])
        elif n == 4:
            for i in [price["New Price"] for price in prices]:
                if len(i) > max_len:
                    max_len = len(i)

            lengthList.append(max_len)
            key.append(keys[n])
    # Menu Content
    menuContent = ''
    menuContentLengths = []
    k = 0
    for i in range(len([item[key[k]] for item in items])):
        for n in range(len(key)):
            if n == 3:
                menuContent = menuContent + f'{[item[key[n]] for item in items][i]}'
            elif n == 0 or n == 1:
                menuContent = menuContent + f'{[item[key[n]] for item in items][i]}{symbol*(lengthList[n]-len([item[key[n]] for item in items][i])+const)}'
            elif n == 2:
                menuContent = menuContent + f'{[fileUtils.digit_split(price["New Price"]) for price in prices][i]}{symbol*(lengthList[n]-len([item[key[n]] for item in items][i])+const)}'
        
        menuContentLengths.append(len(menuContent))
        if i+1 < len([item[key[0]] for item in items]):
            menuContent = menuContent + f'\n'
        else:
            menuContent = menuContent + f''

        if len(key) >= k:
            k += 1

        # Menu Header 
        #print(lengthList)
    for i in range(len(key)):
        menuHeading += f'{key[i]}{" "*(lengthList[i]-len(key[i])+const)}'
    menuHeading = menuHeading + f'\n{"_"*(menuContentLengths[0]+4)}'

    #Menu Display
    print(menuHeading)
    print(menuContent)
    
    return items


# Core Functions
def cart_management(currentUser:str, user_email:str):
    tableName = "Cart"
    products = fileAP.dataframe(fileAP.file_read("Price_management",".csv"))# Get the available products
    dataList = [{"ID":"-", "Name":"-", "Quantity":"-", "Cost": "-"}]
    while True:
        fileBool, fileName= fileAP.is_fileType("Orders", ".csv")
        if fileBool:
            break
        else:
            with open(fileName, "a") as file:
                file.write("No.Order,OrderID,Order_details,Status\n")
            continue

    #Main Loop for Cart Management
    while True:
        menuFormat()
        fileUtils.tableFormat(tableName, dataList)
        userInput = str(input(f'1 - Add Product\n2 - Remove Product\n3 - Modify Quantity\n4 - Confirm Cart\nE - Exit\n{currentUser} - '))
        #Add Product 
        if userInput == '1':
            productID = input("Enter the proudct ID to add: ").strip().upper()
            quantity = input("Enter the Quanity: ").strip()
            
            #Check if the product ID is valid
            found = False
            for product in products:
                if product["ProductID"] == productID:
                    found = True
                    
                    # Removes first index
                    if dataList[0] == {"ID":"-", "Name":"-", "Quantity":"-", "Cost":"-"}:
                        dataList.pop(0)
                    #Check if the product is already in the cart
                    in_cart = False
                    for item in dataList:
                        if item["ID"] == productID:
                            item["Quantity"] = str(int(item["Quantity"]) + int(quantity)) #Increase quantity
                            item["Cost"] = f'RM{str(int(item["Quantity"]) * fileUtils.digit_split(products[fileUtils.digit_split(productID)-1]['New Price']))}'
                            in_cart = True
                            break
                    if not in_cart:
                        cost = int(quantity) * fileUtils.digit_split(products[fileUtils.digit_split(productID)-1]['New Price'])
                        dataList.append({"ID": productID, "Name": product["Name"], "Quantity": quantity, "Cost": f'RM{cost}'})
                        break
            if not found:
                print("Invalid Product ID")
            os.system('cls')
        
        # Remove Product
        elif userInput == '2':
            productID = input("Enter the Product ID to remove: ").strip().upper()
            if len(dataList) == 1 and dataList[0]["ID"] == productID:
                dataList = [{"ID":"-", "Name":"-", "Quantity":"-", "Cost": "-"}]
            else:
                dataList = [item for item in dataList if item["ID"] !=productID] # Remove item from cart if ID matches
            os.system('cls')

        # Modify Product
        elif userInput == '3':
            productID = input("Enter the Product ID to modify: ").strip().upper()
            newQuantity = input("Enter the New Quantity: ").strip()
            try:
                newCost = int(newQuantity) * fileUtils.digit_split(products[fileUtils.digit_split(productID)-1]['New Price'])
            except:
                print("Invalid Value.")
            found = False
            for item in dataList:
                if item["ID"] == productID:
                    item["Quantity"] = newQuantity  # Update quantity
                    item["Cost"] = f'RM{newCost}'
                    found = True
                    break
            if not found:
                print("Product not found in cart.")
            os.system('cls')

        # Confirming cart - Saves the cart into Orders.csv Format of {No.Order (OID0001), OrderID (ODDindexMM), Order_details (Item1 Quantity: Item2 Quantity:...), Completion (Completed or Pending)}
        elif userInput == '4':
            if len(dataList) == 0:
                print("Your cart is empty, cannot confirm an empty cart.")
            else:
                now = datetime.now()
                #Generate a new order ID
                existing_orders = fileAP.dataframe(fileAP.file_read("Orders", ".csv"))
                if existing_orders == None:
                    order_no = 1
                else:
                    order_no = fileUtils.digit_split(existing_orders[-1]['No.Order']) + 1

                order_id = now.strftime("%H%d%M%m%S%Y")
            
                # Create order details (e.g., "Item1 Quantity: Item2 Quantity: ...")
                order_details = "; ".join([f'{item["Name"]} {item["Quantity"]}' for item in dataList])
                totalCost = 0
                for item in dataList:
                    totalCost += fileUtils.digit_split(item["Cost"])
                
                # Create Record for Order storage
                order_record ={
                    "No.Order": f'O{order_no:04}',
                    "OrderID": f'OID{order_id}',
                    "email": f'{user_email}',
                    "Order_details": order_details,
                    "Cost":f'RM{totalCost}',
                    "Status": "Pending"
                }

                fileAP.file_write("Orders",".csv", [order_record])
                dataList = [{"ID":"-", "Name":"-", "Quantity":"-", "Cost": "-"}]
                print(f"Order confirmed! Order ID: {order_id}")
                paySys.store_payment_record(order_id, totalCost)

                fileBool, filename = fileAP.is_fileType("Finance_records", ".csv")
                if fileBool:
                    pass
                else:
                    with open(filename, "x") as file:
                        file = file

                paySys.store_payment_record(order_id, totalCost)
            os.system('cls')             
                
        elif userInput.upper() == 'E':
            print("Exiting cart managment.....")
            break

        else:
            print("Invalid Input")

def account_management(currentUser:str, user_email:str):
    valid_email_format = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.(com|org|net|edu|gov|mil|co)$'
    valid_user_format = r'^[A-Za-z ]+$'
    filename = 'Accounts'
    fileExt = '.csv'
    accountList = fileAP.dataframe(fileAP.file_read(filename, fileExt))
    oldEmail = user_email
    
    while True:
    # Update Personal Information
        userInput = str(input(f'Account Management\n1 - Change Email\n2 - Change Username\n3 - Change Password\nE - Exit\n{currentUser} - '))

        # Email
        if userInput == '1':
            newEmail = str(input("Enter your new email: "))
            if is_valid_email_format(valid_email_format, newEmail):
                for i in accountList:
                    if oldEmail in i['Email']:
                        i.update({'Email':newEmail})
                        fileAP.file_rewrite(filename, fileExt, accountList)
                for i in fileAP.dataframe(fileAP.file_read("Orders", ".csv")):
                    if oldEmail in i['Email']:
                        i.update({'Email':newEmail})
                        fileAP.file_rewrite("Orders", ".csv", accountList)
                user_email = newEmail
            os.system('cls')

        # Username
        elif userInput == '2':
            newUsername = str(input("Enter your new username: "))
            if is_valid_username(valid_user_format, newUsername):
                for i in accountList:
                    if oldEmail in i['Email']:
                        i.update({'User_name':newUsername})
                        user_email = i['Email']
                        fileAP.file_rewrite(filename, fileExt, accountList)
            os.system('cls')

        # Password
        elif userInput == '3':
            oldPassword = str(input("Enter your old password: "))
            
            for i in accountList:
                if oldEmail in i['Email']:

                    if oldPassword == secSys.custom_decrypt(i['Encrypted_password'], i['Salt'], i['Join_date(ddSSmmMMyyyyHH)']):
                        newPassword = str(input("Enter your new password: "))
                        confirmPassword = str(input("Enter your new password again: "))

                        if newPassword == confirmPassword:
                            encrypted_password = secSys.custom_encrypt(newPassword, i['Salt'], i['Join_date(ddSSmmMMyyyyHH)'])
                            i.update({'Encrypted_password':encrypted_password})
                            fileAP.file_rewrite(filename, fileExt, accountList)

                        else:
                            print("Password is different. Process cancelled.")
                    else:
                        print("Incorrect Password. Process cancelled.")
            os.system('cls')

        # Exit 
        elif userInput.upper() == 'E':
            break

        else:
            print("Invalid Input")
    return user_email

def order_tracking(user_email:str):
    orderList = fileAP.dataframe(fileAP.file_read("Orders.csv", ".csv"))
    user_orders = [order for order in orderList if order['Email'] == user_email]
    if len(user_orders) == 0:
        print("You have no orders.")

    else:
        fileUtils.tableFormat('Your Orders', user_orders)
    pause = str(input("=====[Enter to Continue]====="))
    os.system('cls')
    
def product_review(currentUser:str,user_email:str):
    orderList = fileAP.dataframe(fileAP.file_read('Orders', '.csv'))
    accountList = fileAP.dataframe(fileAP.file_read('Accounts', '.csv'), False)
    user_orders = []
    orderIDs = []
    for i in orderList:
        if user_email == i['Email']:
            user_order = {
                'OrderID':i['OrderID'],
                'Order details':i["Order_details"],
                'Status':i['Status']
            }
            user_orders.append(user_order)
            orderIDs.append(i['OrderID'])

    

    def is_eligible_for_review(userOrderSelection, user_orders):
    # Find the order by OrderID
        for order in user_orders:
            if order["OrderID"] == userOrderSelection and order["Status"] == "Completed":
                return True
        return False
    
    while True:
        userInput = str(input(f'1 - Review Product\nE - Exit\n{currentUser} - '))
        if userInput == '1':
            fileUtils.tableFormat("Your Orders", user_orders)
            fileBool, _ = fileAP.is_fileType("Customer", ".csv")
            userOrderSelection = str(input("Enter the Order you want to review: "))
            if fileBool:
                if fileAP.dataframe(fileAP.file_read("Customer_reviews", ".csv")) is None:
                    reviewID = 0

                else:
                    reviewID = fileUtils.digit_split(fileAP.dataframe(fileAP.file_read("Customer_reviews", ".csv"))[-1]['ReviewID'])
            else:
                with open("Customer_reviews.csv", "a") as file:
                    file = file
                    reviewID = 0


            # Check if the order is eligible for review
            if not is_eligible_for_review(userOrderSelection, user_orders):
                print(f"Order {userOrderSelection} is not eligible for review. Only completed orders can be reviewed.")
                continue

            userReview = str(input(f'Enter you review for {userOrderSelection}: '))
            for i in accountList[1:]:
                if i[2] == user_email:
                    accountID = i[0]
                    orderID = userOrderSelection
                    for i in orderList:
                        if userOrderSelection in list(i.values()):
                            orderDetails = i["Order_details"]
                    else:
                        continue

            # Create the review dictionary
            review = {
                "ReviewID": f'Rev{reviewID+1:04}',
                "AccountID": accountID,
                "OrderID": orderID,
                "UserReview": userReview,
                "OrderDetails": orderDetails,  # Link the review to the order's items
                "ReviewStatus": "Open",  # Default status is 'Open'
                "ManagerResponse": '-',  # Initially no manager response
                "ReviewDate": str(datetime.now())
            }

            print(f"Review added.")
            fileAP.file_write("Customer_reviews", ".csv", [review])
        elif userInput.upper() == 'E':
            break
        else:
            print("Invalid Input.")

def customer_payements(currentUser:str, user_email:str):
    while True:
        orders = fileAP.dataframe(fileAP.file_read("Orders", ".csv"))
        payLogs = fileAP.dataframe(fileAP.file_read("payment_log", ".csv"))
        userPayLogs = [payment for order in orders for payment in payLogs if order["Email"] == user_email and order["OrderID"] == payment["OrderID"]]

        userInput = str(input(f'1 - Order History\n2 - Make Payment\nE - Exit\n{currentUser} - '))
        if userInput == '1':
            fileUtils.tableFormat("Payment History", userPayLogs)
            pause = str(input("=====[Hit Enter To Continue]====="))
        elif userInput == '2':
            existingOrders = set()
            unpaidOrders = [payment for order in orders for payment in payLogs 
                            if order["Email"] == user_email and order["Status"] == 'Completed' 
                            and payment["Payment_status"] == "Unpaid" 
                            and order["OrderID"] == payment["OrderID"]
                            and not (order["OrderID"] in existingOrders or existingOrders.add(order["OrderID"]))]
            try:
                fileUtils.tableFormat("Unpaid Orders", unpaidOrders)
                selection = str(input("Enter OrderID to pay: "))
                paySys.init_main(selection)
                pause = str(input("=====[Enter to Continue]====="))
            except:
                print("No unpaid orders pending.")

        elif userInput.upper() == 'E':
            break
        else:
            print("Invalid Input.")
       
def init_customer(currentUser:str, user_email:str):
    while True:
        userInput = str(input(f'1 - Online Order\n2 - Order Tracking\n3 - Manage Account\n4 - Product Review\nE - Exit\n{currentUser} - '))
        if userInput == '1':
            cart_management(currentUser, user_email)

        elif userInput == '2':
            order_tracking(user_email)

        elif userInput == '3':
            user_email = account_management(currentUser, user_email)

        elif userInput == '4':
            product_review(currentUser, user_email)
            
        elif userInput.upper() == 'E':
            break
            
# For Testing         
if __name__ == '__main__':
    init_customer('Test', 'Nathanielkou@mail.com')