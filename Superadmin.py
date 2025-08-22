"""
view_all_files - Super administrator is able to view all files, 
"""
import fileAP
import fileUtils
import os

def view_all_files():
    fileAP.view_files('.csv')
    fileAP.view_files('.py')
    fileAP.view_files('.txt')

def manage_data_files(currentUser:str):
    while True:
        current_dir = os.getcwd()
        files = [f for f in os.listdir(current_dir) if f.endswith('.csv')]
        for i in range(len(files)):
            print(f'{i+1} - {files[i]}')
        selection = str(input(f'E - Exit\n{currentUser} - '))
        try:
            if selection.upper() == 'E':
                break

            elif 0 <= int(selection) < len(files):
                selectedFile = files[int(selection)-1].split('.')
                selectedFile[1] = '.csv'
                fileUtils.init_dbtools(currentUser, "Administrator", selectedFile[0], selectedFile[0], selectedFile[1])
            else:
                print("Invalid Input.")
        except:
            print("Invalid Input")

def view_code_files(currentUser:str):
    while True:
        current_dir = os.getcwd()
        files = [f for f in os.listdir(current_dir) if f.endswith('.py')]
        for i in range(len(files)):
            print(f'{i+1} - {files[i]}')
        selection = str(input(f'E - Exit\n{currentUser} - '))

        if selection == '':
            print("Invalid Input.")

        elif selection.upper() == 'E':
            break
        
        elif selection != '':
            selection = int(selection)
            if 0 < selection <= len(files):
                with open(files[int(selection)], "r") as file:
                    print(file.read())
                    pause = str(input("=====[Enter to Continue]====="))
            else:
                print("Unknown Number")

        else:
            print("Invalid Input.")

def init_superadmin(currentUser:str):
    while True:
        userInput = str(input(f'1 - View all Files\n2 - Manage Data Files(Change Roles Here -> Account)\n3 - View Code Files\nE - Exit\n{currentUser} - '))
        if userInput == '1':
            view_all_files()

        elif userInput == '2':
            manage_data_files(currentUser)

        elif userInput == '3':
            view_code_files(currentUser)

        elif userInput.upper() == 'E':
            break

        else:
            print("Invalid Input.")

# For Testing         
if __name__ == '__main__':
    init_superadmin("Test")
