"""
file Access Point Official manipulate - This Mododule is created specifically for PwP Bakery Project
requires fileAPOfi

Functions
value_check - checks if a value exists in given filefile [Completed] 
digit_split - splits texts. Numbers will be returned ----[Completed]
find - find said data -----------------------------------[Completed]
replace - replaces data with another. -------------------[Completed]
insert - inserts data to specified areas or insert rows. [Completed]
remove - remove data (replaces with a '-'). -------------[Completed]
copy - temporarily copies either cell, row or column. ---[Completed]
paste - pastes the temporary cell, row, or column. ------[Completed]
add - adds rows or columns ------------------------------[Completed]
delete - deletes rows or columns ------------------------[Completed]
update - updates row indexing ---------------------------[Removed]
"""

import fileAP
import os

# Functional Components
def value_check(dataList:list, checkMethod:str):
    """
    Checks if all or any items in the list.

    Args:
        dataList (list): List to be checked.
        checkMethod (str): Method of checking. All or Any.
    """
    if checkMethod == 'any':
        for i in dataList:
            if i:
                return True    
        return False
    
    elif checkMethod == 'all':
        for i in dataList:
            if not i:
                return False
        return True
    
    else:
        return

def digit_split(data:str):
    """
    Splits words and numbers in strings.

    Args:
        data (str): The string.

    Returns:
        digits (int): The number part.
    """

    digits = ''
    for i in range(len(data)):
        if data[i].isdigit():
            digits += data[i]
    return int(digits) if digits else 0

def word_split(data:str):
    """
    Splits words and numbers in strings.

    Args:
        data (str): The string.

    Returns:
        word (str): The word part.
    """
    word = ''
    for i in range(len(data)):
        if data[i].isdigit():
            continue
        else:
            word = word + data[i]
    return str(word)

def tableFormat(tableName:str, dataList:list): 
    items = dataList
    keys = list(dataList[0].keys())
    lengthList = []
    key = []
    totalTableLength = 0
    totalTableLength = totalTableLength + len(keys)*2 + len(keys)*1 + 1
    
    # Longest Text Locator
    for n in range(len(keys)):
        max_len = len(keys[n])
        
        for i in [item[keys[n]] for item in items]:
            if len(i) > max_len:
                max_len = len(i)

        lengthList.append(max_len)
        key.append(keys[n])

        totalTableLength += max_len
        
    # Table Header Generator
    tableHeading = ''
    for i in range(len(key)):
        tableHeading = tableHeading + f'| {key[i]}{" "*(lengthList[i]-len(key[i])+1)}'
    tableHeading = tableHeading + '|\n'
    for i in lengthList:
        tableHeading = tableHeading + f'|{"_"*((i)+2)}'
    tableHeading = tableHeading + '|'

    # Table Content Generator
    tableContent = ''
    k = 0
    for i in range(len([item[key[k]] for item in dataList])):
        for n in range(len(key)):
            tableContent = tableContent + f'| {[item[key[n]] for item in dataList][i]}{" "*(lengthList[n]-len([item[key[n]] for item in dataList][i])+1)}'
            
        if i+1 < len([item[key[0]] for item in dataList]):
            tableContent = tableContent + f'|\n'
        else:
            tableContent = tableContent + f'|'

        if len(key) >= k:
            k += 1

    # Table Last Line Generator
    tableBottom = ''
    for i in lengthList:
        tableBottom = tableBottom + f'|{"_"*((i)+2)}'
    tableBottom = tableBottom + '|'
        
    # Table Display
    tableTitle = f'\n{"_"*((totalTableLength-len(tableName))//2-1)}|{tableName}|{"_"*((totalTableLength-len(tableName))//2-1)}'

    if len(tableTitle) < len(tableHeading)//2:
        tableTitle = tableTitle + '_'
    else:
        pass

    print(tableTitle)
    print(tableHeading)
    print(tableContent)
    print(tableBottom)


# Main Functions
def find(currentUser:str, tableName:str, dataList:list):
    """
    find by value [Completed]
    """

    while True:
        os.system('cls')
        tableFormat(tableName, dataList)
        userInput = str(input(f'_____[Find Data]_____\n1 - Find by Value\nE - Exit\n{currentUser} - ')).upper()
        
        if userInput == '1':
            try:
                os.system('cls')
                tableFormat(tableName, dataList)
                value = str(input("Enter the value you want to find: "))

                if value_check((value in item.values() for item in dataList), "any"):
                    tableFormat(f"Rows found with {value}", [item for item in dataList if value in item.values()])
                    pause = str(input("=====[Enter to Continue]====="))
                else:
                    print(f'{value} does not exist in database.')
                    pause = str(input("=====[Enter to Continue]====="))

            except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))
            
        elif userInput == 'E':
            break

        else:
            userInput = str(input(f'_____[Find Data]_____\n1 - Find by Value\nE - Exit\n{currentUser} - ')).upper()

def replace(currentUser:str, tableName:str, dataList:list, filename:str, fileExt:str):
    """
    replace single cell -[Completed]
    replace similar cell [Completed]
    replace row ---------[Completed]
    """
    while True:
        os.system('cls')
        tableFormat(tableName, dataList)
        userInput = str(input(f'_____[Replace Data]_____\n1 - Replace One Cell\n2 - Replace Similar Cells\n3 - Replace a Row\nE - Exit\n{currentUser} - ')).upper()

        if userInput == '1':
            try:
                cell = str(input("Enter the cell you want to replace. (Row Number);(Column Name): ")).strip().split(';')
                if len(cell) == 2:
                    rowNum, columnName = cell
                    
                    if value_check((item[list(dataList[0].keys())[0]] == rowNum for item in dataList), "any") and value_check((columnName in key for key in dataList), "any"):
                        userValue = str(input("Enter replacement value (1): "))
                        while True:
                            if len(userValue.split()) == 1:
                                value = userValue
                                dataList[digit_split(rowNum)-1].update({columnName:value})
                                tableFormat(tableName, dataList)
                                fileAP.file_rewrite(filename, fileExt, dataList, True)
                                break

                            else:
                                userValue = str(input("Number of value inserted exceeds requirement.\nRe-insert value (1): "))

                    else:
                        print(f'Cell ({rowNum};{columnName}) not found')
                        pause = str(input("=====[Enter to Continue]====="))
                else:
                    print("Number of values inserted exceeds requirement.")
                    pause = str(input("=====[Enter to Continue]====="))
            
            except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))

        elif userInput == '2':
            try:
                oldValue = str(input("Enter the value you want to replace. (1): ")).strip()
                if len(oldValue.split()) == 1:       
                    if value_check((oldValue in item.values() for item in dataList), "any"):
                        rowNums = [item[list(dataList[0].keys())[0]] for item in dataList if oldValue in item.values()]
                        columnNames = [key for item in dataList for key, item in item.items() if item == oldValue]
                        print(columnNames)
                        userValue = str(input("Enter replacement value (1): "))
                        while True:
                            if len(userValue.split()) == 1:
                                newValue = userValue
                                for r in rowNums:
                                    for c in columnNames:
                                        dataList[digit_split(r)].update({c:newValue})
                                tableFormat(tableName, dataList)
                                fileAP.file_rewrite(filename, fileExt, dataList, True)
                                break

                            else:
                                userValue = str(input("Number of value inserted exceeds requirement.\nRe-insert value (1): "))
                    else:
                        print(f'{userValue}) does not exist in database.')
                        pause = str(input("=====[Enter to Continue]====="))
                else:
                    print("Number of value inserted exceeds requirement.")
                    pause = str(input("=====[Enter to Continue]====="))
            except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))

        elif userInput == '3':
            try:
                userInput = None
                os.system('cls')
                tableFormat(tableName, dataList)
                
                rowNum = str(input("Enter the row you want to replace. (1): ")).strip()
                if len(list(rowNum.split())) == 1:       
                    if value_check(item[list(dataList[0].keys())[0]] == rowNum for item in dataList):
                        columnNames = list(dataList[0].keys())[1:]
                        print(columnNames)
                        userValue = str(input(f'Enter replacement values, excluding {list(dataList[0].keys())[0]}. value1,value2,value3...: ({len(list(dataList[0].keys()))-1})'))
                        while True:
                            if len(userValue.split(",")) == len(list(dataList[0].keys()))-1:
                                value = userValue.split(",")
                                for i in range(len(columnNames)):
                                    dataList[digit_split(rowNum)-1].update({columnNames[i]:value[i]})
                                tableFormat(tableName, dataList)
                                fileAP.file_rewrite(filename, fileExt, dataList, True)
                                break

                            else:
                                userValue = str(input(f'Number of value inserted exceeds requirement.\nRe-insert values, excluding {list(dataList[0].keys())[0]}. value1,value2,value3...: ({len(list(dataList[0].keys()))-1})'))

                    else:
                        print(f'{value}) does not exist in database.')
                        pause = str(input("=====[Enter to Continue]====="))
                else:
                    print("Number of value inserted exceeds requirement.")
                    pause = str(input("=====[Enter to Continue]====="))
            except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))

        elif userInput == 'E':
            userInput = None
            break
            
        else:
            print('Invalid Input.')

def insert(currentUser:str, tableName:str, dataList:list, filename:str, fileExt:str):
    """
    insert into empty cell ----------[Completed]
    insert into multiple empty cells [Completed]
    insert row ----------------------[Completed]
    insert column -------------------[Completed]
    """
    
    while True:
        userInput = str(input(f'_____[Insert Data]_____\n1 - Insert into an Empty Cell\n2 - Insert into multiple Empty Cells\n3 - Insert into a Row\n4 - Insert into a Column\nE - Exit\n{currentUser} - ')).upper()

        if userInput == '1':
            try:
                os.system('cls')
                tableFormat(tableName, dataList)
                inputReq = 2
                cell = str(input("Enter the cell you want to insert. Has to be empty. (Row Number);(Column Name): ")).strip().split(';')
                if len(cell) == inputReq:
                    rowNum, columnName = cell
                    
                    if value_check((item[list(dataList[0].keys())[0]] == rowNum for item in dataList), "any") and value_check((columnName in key for key in dataList), "any"):
                        if dataList[digit_split(rowNum)-1][columnName] == '-':
                            userValue = str(input("Enter value to insert (1): "))
                            while True:
                                if len(list(userValue.split(";"))) == 1:
                                    value = userValue
                                    dataList[digit_split(rowNum)-1].update({columnName:value})
                                    tableFormat(tableName, dataList)
                                    fileAP.file_rewrite(filename, fileExt, dataList, True)
                                    break

                                else:
                                    userValue = str(input(f'Number of values inserted exceeds requirement.\nRe-insert value ({inputReq}): '))
                        else:
                            print("Cell is not empty.")

                    else:
                        print(f'Cell ({rowNum},{columnName}) not found')
                        pause = str(input("=====[Enter to Continue]====="))

                else:
                    print("Number of values inserted exceeds requirement.")
                    pause = str(input("=====[Enter to Continue]====="))

            except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))


        elif userInput == '2':
            try:
                os.system('cls')
                tableFormat(tableName, dataList)
                inputReq = 2
                cells = []

                while True:
                    cell = str(input("Enter the cell you want to insert. Has to be empty. E to stop. (Row Number);(Column Name): "))
                    if cell == 'E':
                        break
                    
                    elif len(cell.split(";")) == inputReq:
                        if value_check((item[list(dataList[0].keys())[0]] == cell.split(",")[0] for item in dataList), "any") and value_check((cell.split(",")[1] in key for key in dataList), "any"):
                            if dataList[digit_split(cell.split(",")[0])][cell.split(",")[1]] == '-':
                                cells.append(cell.split(','))
                                print(cells)

                            else:
                                print("Cell is not empty.")
                        
                        else:
                            print(f'Cell ({rowNum},{columnName}) not found')
                            pause = str(input("=====[Enter to Continue]====="))
                    else:
                        print("Input Not Recognized.")
                        pause = str(input("=====[Enter to Continue]====="))
                        continue
                    

                userValue = str(input("Enter value to insert (1): "))
                while True:
                    if len(list(userValue.split())) == 1:
                        break
                    else:
                        userValue = str(input(f'Number of values inserted exceeds requirement.\nRe-insert value ({inputReq}): '))

                for i in cells:
                    rowNum, columnName = i
                    value = userValue
                    dataList[digit_split(rowNum)-1].update({columnName:value})

                tableFormat(tableName, dataList)
                fileAP.file_rewrite(filename, fileExt, dataList, True)
            except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))
                
        elif userInput == '3':
            try:
                os.system('cls')
                tableFormat(tableName, dataList)
                rowNum = str(input("Enter the row you want to insert. (1): ")).strip()
                if len(list(rowNum.split())) == 1:
                    keys = list(dataList[0].keys())
                    if value_check((item[list(dataList[0].keys())[0]] == rowNum for item in dataList), "any"):
                        columnNames = list(dataList[0].keys())[1:]
                        for i in columnNames:
                            if dataList[digit_split(rowNum)-1][i] != '-':
                                print(f'{rowNum}, {i} is not empty.')
                                break
                                
                            else:
                                userValue = str(input(f'Enter replacement values, excluding {list(dataList[0].keys())[0]}. value1,value2,value3... ({len(list(dataList[0].keys()))-1}): '))
                                while True:
                                    if len(userValue.split(",")) == len(list(dataList[0].keys()))-1:
                                        value = userValue.split(",")
                                        for i in range(len(columnNames)):
                                            dataList[digit_split(rowNum)-1].update({columnNames[i]:value[i]})
                                        tableFormat(tableName, dataList)
                                        fileAP.file_rewrite(filename, fileExt, dataList, True)
                                        break

                                    else:
                                        userValue = str(input(f'Number of value inserted exceeds requirement.\nRe-insert values, excluding {list(dataList[0].keys())[0]}. value1,value2,value3...: ({len(list(dataList[0].keys()))-1})'))
                        
                    else:
                        print(f'{value}) does not exist in database.')
                        pause = str(input("=====[Enter to Continue]====="))
                else:
                    print("Number of value inserted exceeds requirement.")
                    pause = str(input("=====[Enter to Continue]====="))
            except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))

        elif userInput == '4':
            try:
                os.system('cls')
                tableFormat(tableName, dataList)
                columnName = str(input("Enter the column name to insert: ")).strip()
                valueInput = str(input("Enter the value to insert: ")).strip()
                if value_check((columnName in key for key in dataList), "any"):
                    if value_check(((item[columnName] == '-' for item in dataList)), "all"):
                        for item in dataList:
                            item.update({columnName:valueInput})
                        tableFormat(tableName, dataList)
                        fileAP.file_rewrite(filename, fileExt, dataList, True)
                
                    else:
                        print(f'{columnName} is not empty.')
                        pause = str(input("=====[Enter to Continue]====="))
                        break
                else:
                    print(f"Column '{columnName}' not found")
                    pause = str(input("=====[Enter to Continue]====="))
            except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))

        elif userInput == 'E':
            userInput = None
            break
            
        else:
            print("Invalid Input.")

def remove(currentUser:str, tableName:str, dataList:list, filename:str, fileExt:str):
    """
    replaces data values with a dash, meaning empty.
    remove similar cells -[Completed]
    remove single cell ---[Completed]
    remove multiple cells [Completed]
    remove row -----------[Completed]
    remove column --------[Completed]
    """

    while True:
        # Display the current table
        os.system('cls')
        tableFormat(tableName, dataList)

        # Prompt the user for removal action
        userInput = str(input(f'Choose an action: \n1 - Remove single cell\n2 - Remove similar cells\n3 - Remove multiple cells\n4 - Remove row\n5 - Remove column\nE - Exit\nEnter your choice (1-4 , E): \n{currentUser} - ')).strip()

        if userInput == '1':
            try:
                cell = str(input("Enter the cell to remove. (Row Number),(Column Name): ")).strip().split(',')
                if len(cell) == 2:
                    rowNum, columnName = cell
                    if value_check((item[list(dataList[0].keys())[0]] == rowNum for item in dataList), "any") and columnName in dataList[0].keys():
                        dataList[digit_split(rowNum)-1].update({columnName: '-'})
                        tableFormat(tableName, dataList)
                        fileAP.file_rewrite(filename, fileExt, dataList, True)
                    else:
                        print(f"Cell ({rowNum},{columnName}) not found")
                        pause = str(input("=====[Enter to Continue]====="))
            except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))

        elif userInput == '2':
            try:
                oldValue = str(input("Enter the value you want to remove. (1): ")).strip()
                if len(list(oldValue.split())) == 1:       
                    if value_check((oldValue in item.values() for item in dataList), "any"):
                        rowNums = [item[list(dataList[0].keys())[0]] for item in dataList if oldValue in item.values()]
                        columnNames = [key for item in dataList for key, item in item.items() if item == oldValue]
                        #print(columnNames)
                        for r in rowNums:
                            for c in columnNames:
                                dataList[digit_split(r)].update({c:'-'})
                        tableFormat(tableName, dataList)
                        fileAP.file_rewrite(filename, fileExt, dataList, True)
            except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))

        elif userInput == '3':
            try:
                cells = []

                while True:
                    cell = input("Enter cells to remove (format: Row,Column): ").strip()
                    if cell == 'E':
                        break
                    elif value_check((item[list(dataList[0].keys())[0]] == cell.split(',')[0] for item in dataList), "any") and cell.split(',')[1] in dataList[0].keys():
                        cells.append(cell.split(','))
                    else:
                        print(f"Cell ({rowNum},{columnName}) not found")

                for cell in cells:
                    rowNum, columnName = cell
                    dataList[digit_split(rowNum)-1].update({columnName: '-'})

                tableFormat(tableName, dataList)
                fileAP.file_rewrite(filename, fileExt, dataList, True)
            except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))

        elif userInput == '4':  # Remove entire row
            try:
                rowNum = input("Enter the row number to remove: ").strip()
                columnName = list(dataList[digit_split(rowNum)-1].keys())[1:]
                for c in columnName:
                    dataList[digit_split(rowNum)-1].update({c:'-'})
                tableFormat(tableName, dataList)
                fileAP.file_rewrite(filename, fileExt, dataList, True)
            except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))

        elif userInput == '5':
            try:
                columnName = input("Enter the column name to remove: ").strip()
                if columnName in list(dataList[0].keys()):
                    for item in range(len(dataList)):
                        dataList[item].update({columnName:'-'})
                    tableFormat(tableName, dataList)
                    fileAP.file_rewrite(filename, fileExt, dataList, True)
                else:
                    print(f"Column '{columnName}' not found")
                    pause = str(input("=====[Enter to Continue]====="))
            except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))

        elif userInput == 'E':
            break

        else:
            print("Invalid choice, please try again.")

def copy(currentUser:str, tableName:str, dataList:list):
    """
    copy cell value ---[Completed]
    copy entire row ---[Completed]
    copy entire column [Completed]
    copy entire table -[Removed]
    """

    # Display the current table to be copied
    tableFormat(tableName, dataList)

    while True:
        try:
            userInput = str(input(f'_____[Copy Data]_____\n1 - Copy Cell\n2 - Copy Row\n3 - Copy Column\nE - Exit\n{currentUser} - ')).upper()
            if userInput == '1':
                # Copy single cell value
                os.system('cls')
                tableFormat(tableName, dataList)

                cell = str(input("Enter the cell to copy (Row Number, Column Name): ")).strip().split(',')
                if len(cell) == 2:
                    rowNum, columnName = cell

                    if value_check(([item for item in dataList if item[list(dataList[0].keys())[0]] == rowNum]), "any"):
                        data1 = [(dataList[digit_split(rowNum)-1][columnName])]
                        print(f"Copied {data1}.")
                        return data1
                    else:
                        print(f'Cell ({rowNum}, {columnName}) not found')
                else:
                    print("Invalid input format.")

            elif userInput == '2':
                os.system('cls')
                tableFormat(tableName, dataList)
                rowNum = str(input("Enter the row to copy (Row Number): "))
                if value_check(([item for item in dataList if item[list(dataList[0].keys())[0]] == rowNum]), "any"):
                    data1 = list(dataList[digit_split(rowNum)-1].values())[1:].copy()
                    print(f'Copied {data1}')
                    return data1
                else:
                    print(f'{rowNum} is not in file')

            elif userInput == '3':
                os.system('cls')
                tableFormat(tableName, dataList)
                columnName = str(input("Enter the column to copy (Column Name): "))
                if columnName in dataList[0].keys():
                    buffer = []
                    for item in range(len(dataList)):
                        buffer.append(dataList[item][columnName])
                    data1 = buffer.copy()
                    print(f'Copied {data1}.')
                    return data1
                else:
                    print(f'{columnName} does not exist.')

            elif userInput == 'E':
                # Exit the copy function
                userInput = None
                break

            else:
                print("Invalid Input")
        except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))

def paste(currentUser:str, tableName:str, dataList:list, filename:str, fileExt:str, data1:list):
    """
    paste cell value ---[Completed]
    paste entire row ---[Completed]
    paste entire column [Completed]
    """

    while True:
        try:
            userInput = None
            os.system('cls')
            tableFormat(tableName, dataList)
            userInput = str(input(f'_____[Paste Data]_____\n1 - Paste Single Cell\n2 - Paste Entire Row\n3 - Paste Entire Column\nE - Exit\n{currentUser} - '))

            if userInput == '1':  # Paste a single cell
                inputReq = 2

                cell = str(input("Enter the cell you want to paste into (Row Number, Column Name): ")).strip().split(',')
                if len(cell) == inputReq:
                    rowNum, columnName = cell
                    
                    if value_check((item[list(dataList[0].keys())[0]] == rowNum for item in dataList), "any") and columnName in dataList[0]:
                        while True:
                            if len(data1) == 1:
                                dataList[digit_split(rowNum)-1].update({columnName: data1[0]})
                                tableFormat(tableName, dataList)
                                fileAP.file_rewrite(filename, fileExt, dataList, True)
                                break
                            else:
                                print("Data Pasted Exceeds Requirement.")
                    else:
                        print(f'Cell ({rowNum},{columnName}) not found.')
                else:
                    print("Invalid input.")

            elif userInput == '2':
                rowNum = str(input("Enter row to paste data (Row Number): "))
                if value_check((item[list(dataList[0].keys())[0]] == rowNum for item in dataList), "any"):
                    for columnNum in range(1, len(list(dataList[0].keys()))):
                        dataList[digit_split(rowNum)-1].update({list(dataList[0].keys())[columnNum]: data1[columnNum-1]})

                    tableFormat(tableName, dataList)
                    fileAP.file_rewrite(filename, fileExt, dataList, True)

                else:
                    print(f'{rowNum} does not exist.')

            elif userInput == '3':
                columnName = str(input("Enter column to paste data (Column Name): "))
                if columnName in list(dataList[0].keys()):
                    for i in range(len(dataList)):
                        dataList[i].update({columnName:data1[i]})

                    tableFormat(tableName, dataList)
                    fileAP.file_rewrite(filename, fileExt, dataList, True)

                else:
                    print(f'{columnName} does not exist.')

            elif userInput.upper() == 'E':  # Exit
                break

            else:
                print("Invalid Input.")
        except:
                print("Value Provided caused an error.")
                pause = str(input("=====[Enter to Continue]====="))

def add(currentUser:str, tableName:str, dataList:list, filename:str, fileExt:str):
    """
    add row ----[Removed]
    add rows ---[Completed]
    add column -[Removed]
    add columns [Completed]
    """
    while True:
        try:
            os.system('cls')
            tableFormat(tableName, dataList)
            key = list(dataList[0].keys())
            userInput = str(input(f'1 - Add Row(s)\n2 - Add Column(s)\nE - Exit\n{currentUser} - '))

            if userInput == '1':
                rowNum = str(input("Enter the number of row(s) to add:  "))
                latestIndex = digit_split(dataList[-1][key[0]])
                dataDict = {}
                for i in range(latestIndex+1, latestIndex+1+int(rowNum)):
                    dataDict[list(dataList[0].keys())[0]] = f'{word_split(dataList[0][key[0]])}{i:02}'
                    for k in list(dataList[0].keys())[1:]:
                        dataDict[k] = '-'
                    dataList.append(dataDict)
                    dataDict = {}
                tableFormat(tableName, dataList)
                fileAP.file_rewrite(filename, fileExt, dataList, True)

            elif userInput == '2':
                columnNum = str(input("Enter number of column(s) to add: "))
                columnNames = []
                i = 0

                while True:
                    columnName = str(input("Enter Column Name: "))
                    if columnName == "" and i < digit_split(columnNum):
                        print(f'Column names are not fully assigned!')
                    elif columnName == "" and i == digit_split(columnNum):
                        break
                    elif columnName != "":
                        columnNames.append(columnName)
                        i += 1
                    else:
                        continue

                for i in dataList:
                    for c in columnNames:
                        i[c] = '-'
                tableFormat(tableName, dataList)
                fileAP.file_rewrite(filename, fileExt, dataList, True)

            elif userInput.upper() == 'E':
                break

            else:
                print("Invalid Input.")
        except:
            print("Value Provided caused an error.")
            pause = str(input("=====[Enter to Continue]====="))

def delete(currentUser:str, tableName:str, dataList:list, filename:str, fileExt:str):
    """
    delete row ------[Removed]
    delete row(s) ---[Completed]
    delete column(s) [Completed]
    delete columns --[Removed]
    """
    while True:
        try:
            os.system('cls')
            tableFormat(tableName, dataList)
            
            userInput = str(input(f'_____[Delete Data]_____\n1 - Delete Row(s)\n2 - Delete Column(s)\nE - Exit\n{currentUser} - ')).upper()

            if userInput == '1':
                rows = []
                while True:
                    rowNum = str(input("Enter the row number to delete. E to stop: "))
                    if rowNum.upper() == 'E':
                        break
                    elif value_check(([item for item in dataList if item[list(dataList[0].keys())[0]] == rowNum]), "any"):
                        rows.append(rowNum)
                    else:
                        print("1 or more rows does not exist.")
                        continue

                for i in rows:
                    dataList = [item for item in dataList if item[list(dataList[0].keys())[0]] != i]
                tableFormat(tableName, dataList)
                fileAP.file_rewrite(filename, fileExt, dataList, True)

            elif userInput == '2':
                columns = []
                while True:
                    columnName = str(input("Enter the column name to delete. E to stop: ")).strip()
                    if columnName.upper() == 'E':
                        break
                    elif columnName in dataList[0].keys():
                        columns.append(columnName)

                    else:
                        print(f'{columnName} does not exist.')

                for column in columns:
                    for item in dataList:
                        item.pop(column, None)
                tableFormat(tableName, dataList)
                fileAP.file_rewrite(filename, fileExt, dataList, True)

            elif userInput == 'E':  # Exit the loop
                break

            else:
                print("Invalid choice, please try again.")
        except:
            print("Value Provided caused an error.")
            pause = str(input("=====[Enter to Continue]====="))

def init_dbtools(currentUser:str, functionName:str, tableName:str, filename:str, fileExt:str):
    dbToolActions = ["Find", "Replace", "Insert", "Remove", "Copy", "Paste", "Add", "Delete"]
    action = None
    data1 = None
    while True:
        os.system('cls')
        dataList = fileAP.dataframe(fileAP.file_read(filename, fileExt))
        tableFormat(tableName, dataList)
        for i in range(len(dbToolActions)):
            print(f'{i+1} - {dbToolActions[i]}')
        print('E - Exit')
        action = str(input(f'{currentUser} - ')).upper()
        

        if action == '1':
            find(currentUser, tableName, dataList)

        elif action == '2':
            replace(currentUser, tableName, dataList, filename, fileExt) 

        elif action == '3':
            insert(currentUser, tableName, dataList, filename, fileExt)

        elif action == '4':
            remove(currentUser, tableName, dataList, filename, fileExt)

        elif action == '5':
            data1 = copy(currentUser, tableName, dataList)

        elif action == '6':
            if data1 is None:
                print("No data to be pasted.")
                continue
            else:
                paste(currentUser, tableName, dataList, filename, fileExt, data1)

        elif action == '7':
            add(currentUser, tableName, dataList , filename, fileExt)

        elif action == '8':
            delete(currentUser, tableName, dataList, filename, fileExt)

        elif action == 'E':
            print(f"Exiting {functionName}")
            break

        else:
            print('Invalid Input.')
            

# For Testing         
if __name__ == '__main__':
    init_dbtools("Test", "Ingredient Management", "Ingredient_supply", "Ingredient_supply", ".csv")


