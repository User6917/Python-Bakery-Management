import fileAP
import fileUtils

def order_sent(currentUser:str):
    while True:
        pendingList = fileAP.dataframe(fileAP.file_read("Ordered_list", ".csv"))
        userInput = str(input(f'1 - Complete Ingredient\nE - Exit\n{currentUser} - '))
        if userInput == '1':
            fileUtils.tableFormat("Ingredient Orders", pendingList)
            selection = str(input(f'Enter RecordID to complete order or E to exit.\n{currentUser}: '))
            if selection.upper == 'E':
                break
            elif selection in [record['RecordID'] for record in pendingList]:
                for record in pendingList:
                    if selection == record['RecordID']:
                        record.update({'Status':'Completed'})
                        fileAP.file_rewrite("Ordered_list", ".csv", pendingList)
                fileUtils.tableFormat("Ingredient Orders", pendingList)
        elif userInput.upper() == 'E':
            break
        else:
            print("Invalid Input")

def init_supplier(currentUser:str):
    while True:
        userInput = str(input(f'1 - Ingredient Requests\nE - Exit\n{currentUser}'))
        if userInput == '1':
            order_sent(currentUser)
        elif userInput.upper() == 'E':
            break
        else:
            print("Invalid Input")

# For Testing         
if __name__ == '__main__':
    init_supplier('Test')