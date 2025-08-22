import fileAP                       # (Created) Used for handling files
import fileUtils                    # (Created) Used for manipulating files
import os                           # Used for clearing terminal 
import securitySys as secSys        # (Created) Used for encoding passwords of the user.
import re                           # Used for formatting valid email formats.
from datetime import datetime as dt # Used for storing account creation date as well as password encoding.
import Baker                        # (Created) Baker Interface Initializer
import Cashier                      # (Created) Cashier Interface Initializer
import Customer                     # (Created) Customer Interface Initializer
import Manager                      # (Created) Manager Interface Initializer
import Superadmin                   # (Created) Superadmin Interface Initializer
import Supplier                     # (Created) Supplier Interface Initializer
"""
Page Loader - Loads the Homepages Text and boarder
login_sys - Login system, logout is outer function
    is_valid_email_format - checks if given email fits generic email format (Uses RegEx)
    is_valid_username - checks if given username has non-word symbols (Uses RegEx)
    login - checks if email, and password is same with store
    signup - creates email and password
logout - used to logout of account
main - Main script that loads the app
"""
def page_Load(totalDimension, pageName, content, currentUser = "Guest"):

    pageNameDimension = len(pageName)
    leftDimension = rightDimension = totalDimension//2

    if pageNameDimension%2 == 1:
        rightDimension -= 1
    
    else:
        pass

    print(f'{"-"*(leftDimension-(pageNameDimension//2+1))}[{pageName}]{"-"*(rightDimension-(pageNameDimension//2+1))}'
          f'\nUser: {currentUser}')
    action = input(f'{content}\n')
    pass

def login_sys(currentUser:str):
    dataList = fileAP.dataframe(fileAP.file_read("Accounts", ".csv"))
    valid_email_format = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.(com|org|net|edu|gov|mil|co)$'
    valid_user_format = r'^[A-Za-z ]+$'

    def is_valid_email_format(valid_email_format, email:str):
        if re.match(valid_email_format, email):
            return True
        else:
            return False
    
    def is_valid_username(valid_user_format, username:str):
        if re.match(valid_user_format, username):
            return True
        else:
            return False

    def login():
        while True:
            email = str(input("Enter your registered email: "))
            email_found = False
            for i in dataList:
                if email in i.values():
                    user_password = str(input("Enter your password: "))
                    encrypted_password = i["Encrypted_password"]
                    salt = i["Salt"]
                    key = i["Join_date(ddSSmmMMyyyyHH)"]
                    user_role = i["Current_role"]
                    user_name = i["User_name"]
                    user_email = i["Email"]
                    email_found = True
                    break
                else:
                    continue
            break
        if email_found:
            if secSys.validate_password(encrypted_password, salt, user_password, key):
                print(f'Welcome, {user_name}.')
                currentUser = user_role
                user_email = user_email

            else:
                print("Incorrect password and email.")
                currentUser = "Guest"
                user_email = '-'
        else:
            currentUser = "Guest"
            user_email = '-'
            print("Invalid Email")

        return currentUser, user_email

    def signup():
        while True:
            email = str(input("Register your email: "))
            if is_valid_email_format(valid_email_format, email):
                while True:
                    password = str(input("Register your password: ")).strip()
                    passConfirm = str(input("Enter password again to confirm: ")).strip()
                    if passConfirm.upper() == 'E':
                        print("Password not confirmed.")
                        password = None
                        break
                    elif passConfirm == password:
                        print("Password Confirmed.")
                        now = dt.now()
                        join_date = now.strftime("%d%S%m%M%Y%H")
                        salt = secSys.create_salt()
                        encrypted_password = secSys.custom_encrypt(password, salt, join_date)
                        break
                    else:
                        print("Password is different.")
                while True:
                    user_name = str(input("Enter your user name. Only alphabets and spaces: "))
                    if is_valid_username(valid_user_format, user_name):
                        break
                    else:
                        print("Invalid Username format")

                break

            else:
                print("Invalid Email Format.")
        if fileAP.dataframe(fileAP.file_read("Accounts", ".csv")) is None:
            latestID = 1
        else:
            latestID = fileUtils.digit_split(fileAP.dataframe(fileAP.file_read("Accounts", ".csv"))[-1]['AccountID']) + 1

        fileAP.file_write("Accounts", ".csv", [{"AccountID":f'AC{latestID:04}', "User_name":user_name,"Email":email,"Encrypted_password":encrypted_password,"Salt":salt,"Join_date(ddSSmmMMyyyyHH)":join_date,"Current_role":"Customer"}])
        return "Customer", email
    
    while True:
        action = str(input(f'New User? (S)ign up!\nExisting User? (L)ogin!\nExit Page? (E)xit!\n{currentUser} - '))
        if action.upper() == 'S':
            currentUser, user_email = signup()
            break

        elif action.upper() == 'L':
            currentUser, user_email = login()
            if currentUser.upper() != "GUEST":
                break

        elif action.upper() == 'E':
            currentUser = "Guest"
            break

        else:
            print("Invalid Input.")

    return currentUser, user_email

def logout():
    currentUser = "Guest"
    user_email = ''
    return currentUser, user_email


def main(projectName, dimension):
    currentUser = "Guest"
    #totalDimension = len(f'{"="*dimension}[{projectName}]{"="*dimension}')
    
    while True:
        print(f'{"="*dimension}[{projectName}]{"="*dimension}')

        if currentUser.upper() == "GUEST":
            while True:
                userInput = str(input(f'1 - View Products\n2 - Login Page\nE - Exit Bakery\n{currentUser} - '))
                if userInput == '1':
                    Customer.menuFormat()
                    pause = input("=====[Enter to Continue]=====\n")
                    os.system('cls')

                elif userInput == '2':
                    currentUser, user_email = login_sys(currentUser)
                    break
                
                elif userInput.upper() == 'E':
                    return
                else:
                    print("Invalid Input")

        elif currentUser.upper() == 'BAKER':
            while True:
                userInput = str(input(f'1 - Baker Page\n2 - Logout\nE - Exit Bakery\n{currentUser} - '))
                if userInput == '1':
                    Baker.init_baker(currentUser)

                elif userInput == '2':
                    currentUser, user_email = logout()
                    pause = input("=====[Logout Successful, Enter to Continue]=====\n")
                    os.system('cls')
                    break
                
                elif userInput.upper() == 'E':
                    return
                
                else:
                    print("Invalid Input")
            

        elif currentUser.upper() == 'CASHIER':
            while True:
                userInput = str(input(f'1 - Cashier Page\n2 - Logout\nE - Exit Bakery\n{currentUser} - '))
                if userInput == '1':
                    Cashier.init_cashier(currentUser)
                elif userInput == '2':
                    currentUser, user_email = logout()
                    pause = input("=====[Logout Successful, Enter to Continue]=====\n")
                    os.system('cls')
                    break
                
                elif userInput.upper() == 'E':
                    return
                
                else:
                    print("Invalid Input")
            

        elif currentUser.upper() == "CUSTOMER":
            while True:
                userInput = str(input(f'1 - Customer Page\n2 - Logout\nE - Exit Bakery\n{currentUser} - '))
                if userInput == '1':
                    Customer.init_customer(currentUser, user_email)
                elif userInput == '2':
                    currentUser, user_email = logout()
                    pause = input("=====[Logout Successful, Enter to Continue]=====\n")
                    os.system('cls')
                    break

                elif userInput.upper() == 'E':
                    return
                
                else:
                    print("Invalid Input")

        elif currentUser.upper() == 'MANAGER':
            while True:
                userInput = str(input(f'1 - Manager Page\n2 - Logout\nE - Exit Bakery\n{currentUser} - '))
                if userInput == '1':
                    Manager.init_manager(currentUser)
                elif userInput == '2':
                    currentUser, user_email = logout()
                    pause = input("=====[Logout Successful, Enter to Continue]=====\n")
                    os.system('cls')
                    break

                elif userInput.upper() == 'E':
                    return
                
        elif currentUser.upper() == 'SUPERADMIN':
            while True:
                userInput = str(input(f'1 - Superadmin Page\n2 - Logout\nE - Exit Bakery\n{currentUser} - '))
                if userInput == '1':
                    Superadmin.init_superadmin(currentUser)
                elif userInput == '2':
                    currentUser, user_email = logout()
                    pause = input("=====[Logout Successful, Enter to Continue]=====\n")
                    os.system('cls')
                    break

        elif currentUser.upper() == 'SUPPLIER':
            while True:
                userInput = str(input(f'1 - Supplier Page\n2 - Logout\nE - Exit Bakery\n{currentUser} - '))
                if userInput == '1':
                    Supplier.init_supplier(currentUser)
                elif userInput == '2':
                    currentUser, user_email = logout()
                    pause = input("=====[Logout Successful, Enter to Continue]=====\n")
                    os.system('cls')
                    break

                elif userInput.upper() == 'E':
                    return

        
        
    #menuFormat(7)

    #page_Load(totalDimension, "Baker Page", content = None)
    #print(fileAP.dataframe(fileAP.file_read("Ingredient_supply")))


projectName = "PwP Bakery"
dimension = 80//2

if __name__ == "__main__":
    os.system('cls')  # Command to clear the terminal on Windows
    main(projectName, dimension)
    #print(fileAP.dataframe(fileAP.file_read("Baked_goods")))