"""
file Access Point - This Mododule is created specifically for PwP Bakery Project
Functions: 
is_fileType(filename:str) - Used in this module by default, checks if the accessed file has fileType as an extention
dataframe(typeDict:bool,dataList:list) - Converts a a listed of lists datas into listed dictionaries or remains as listed lists
file_create() - intended to use separately as a command. Will ask users for a filename,
file_read(filename:str) - reads the file, will convert directly into listed lists
file_save()
file_write(filename:str, dataframe:list) - takes in listed dictionaries or listed lists and writes into file provided. !THIS ONLY APPENDS THEM!
file_rewrite(filename:str, dataframe:list) - same as file_write, but !THIS WILL WIPE ALL EXISTING DATA OF THAT FILE! WIL ASK FOR USER CONFIRMARTION!
file_delete() - will require which file to be deleted !WILL AS USER FOR CONFIRMATION!
check_file() - will check for all files with given extention in the folder that the module is currently held. Bt default it checks in this python folder

**IMPORTANT** Select what dataList you prefer, True for Listed Dictionaries, False for List of Lists. Default is List of Dictionaries, in True state
"""


import os # For deleting file

# File checking
def is_fileType(filename:str, fileExt:str):
    """
    Checks to see if file provided is fileExt, and returns a True value as well as the full name.

    Args:
        filename (str): The name of the file to save the data to.
        fileExt (str): The files extension.
    Returns:
        is_fileType (bool): True if file is same as fileExt, false if it is not.
        
        full_filename (str): The files name with fileExt.
    """

    full_filename = f"{filename}{fileExt}"
    try:
        
        if os.path.isfile(full_filename): # Checks if filename provided is a supported file
            return True, full_filename
        
        else:
            return False, full_filename
        
    except:
        print("Error occured at file confirmation. Refer: is_fileType(filename:str, fileExt:str)")

# Data formatting [Uses Listed Dictionaries]
def dataframe(dataList:list, typeDict:bool=True):
    """
    Converts Raw data into formatted and cleaned data.

    Args:
        dataList (list): The raw data to be formatted and cleaned.
        typeDict (bool, optional): Indicates whether the data is a list of dictionaries (True) or a list of lists (False). Defaults to True.
    Returns:
        list: The cleaned and formatted dataList
    """

    try:
        
        if typeDict:
            df = []            
            if dataList[0] != ['']: # Header is present
                headerList = dataList[0]
            elif dataList[0] == ['']: # Headers not present
                headerList = str(input("No headers detected: [Please enter headers] - ")).split(" ")
            else:
                return
            
            for n in range(1, len(dataList)): # Appending the data into the frame
                dataDict = {}
                for i in range(len(dataList[n])):
                    dataDict[headerList[i]] = dataList[n][i]
                df.append(dataDict)
            return df
        
        else:
            if dataList[0] != ['']: # Header is present
                headerList = dataList[0]
            elif dataList[0] == ['']: # Headers not present
                headerList = str(input("No headers detected: [Please enter headers] - ")).split(" ")
            else:
                return

            dataList[0] = headerList # Setting the header

            df = dataList # setting df with dataList
            
            return df

    except:
        print("Error occured at creating dataframe. Refer: dataframe(dataList:list)")

# File reading
def file_read(filename:str, fileExt:str):
    """
    Gets data from file

    Args:
        filename (str): The name of the file to read data from.
        fileExt (str): The files Extention.
    Returns:
        dataList (list): The raw data list from the file.
    """
    if filename.endswith(fileExt):
        fileBool = True
        pass
    else:
        fileBool, filename = is_fileType(filename, fileExt)

    dataList = []

    try:
        if fileBool:
            with open(filename, "r") as file:
                bufferList = file.readlines() # Initial data reading

                for i in range(len(bufferList)):
                    dataList.append(bufferList[i].strip().split(",")) # Cleaned dataList

                return dataList
        
        else:
            print(f'{filename} is not a valid file.')
            return

    except:
        return print(f'{filename} does not exist.')

# File creation
def file_create(filename:str, fileExt:str):
    """
    Creates a file. No external parameters. Function is self sufficient. Can be automated.

    Args:
    filename (str) : Default None. Name of the file to be created.
    """
        
    if filename is None:
        filename = str(input("Please enter the file name: ")) # File naming
        fileExt = str(input("Please enter the files extension: ")) # File Extension
        filename = f'{filename}{fileExt}'

    else:
        with open(filename, 'x') as file:
            pass


    with open(filename, 'a') as file:
        file = open(filename, "a")

        decision = str(input("Are there are headers in this file: [Y/N]")).upper() # File creation with headers

        if decision == 'Y':
            headerList = []
            c = 1
            while True:
                header = str(input(f'Please enter your header. Enter blank to stop: [{c}]')).strip()
                if header != "":
                    headerList.append(header)
                    c = c + 1

                else:
                    indexMethod = str(input("Enter row id format: "))
                    row1 = []
                    row1.append(indexMethod)
                    for i in range(len(headerList)-1):
                        row1.append("-")
                    file.write(f'{",".join(headerList)}\n{",".join(row1)}')
                    break

        elif decision == 'N':
            pass

        print(f'{filename} has been created')
    return

# File deletion
def file_delete():
    """
    Deletes the file directly. No external parameters. Function is self sufficient.
    """

    try:
        filename = str(input("Please enter the file to be deleted: "))
        fileExt = str(input("Please enter the files extension with the dot: "))
        filename = f'{filename}{fileExt}' 

        if os.path.exists(filename): # Check if file exists

            decision = input(f'Warning! Deleting {filename}. [C]onfirm to proceed or [D]eny: ').upper()

            if decision == 'C':
                os.remove(filename) # Deleting the file
                print(f'{filename} has been deleted.')

            elif decision == 'D':
                print(f'{filename} deletion aborted.')

            else:
                print("Unknown input. Action Aborted")

        else:
            print(f'{filename} does not exist. Aborting...')

    except:
        print(f'Error occured at deleting {filename}. Refer file_delete().')

    return 

# File saving
def file_save_data(filename:str, dataList:list, fileExt:str, typeDict:bool=True, overwrite:bool=False):
    """
    Saves the given data to the specified file.
    Provides options for appending or overwriting based on 'overwrite' flag.

    Args: 
        filename (str): The name of the file to save the data to.
        dataList (list): The data to be saved, either as a list of dictionaries (typeDict=True) or a list of lists (typeDict=False).
        typeDict (bool, optional): Indicates whether the data is a list of dictionaries (True) or a list of lists (False). Defaults to True.
        fileExt (str): The files extension.
        overwrite (bool, optional): If True, overwrites the existing file. If False, appends to the file. Defaults to False.
    """
    fileExt = fileExt
    try:
        if overwrite:
            file_rewrite(filename, fileExt, dataList, typeDict) # Overwrite existing data
        else:
            file_write(filename, fileExt, dataList, typeDict)  # Append to existing data

    except Exception as e:
        print(f"Error saving data to {filename}: {e}")

    return

# File writing
def file_write(filename:str, fileExt:str, dataframe:list, typeDict:bool=True):
    """
    Writes the given data to the specified file.
    does NOT wipe exisitng data.

    Args:
        filename (str): The name of the file to save the data to.
        dataList (list): The data to be written, either as a list of dictionaries (typeDict=True) or a list of lists (typeDict=False).
        typeDict (bool, optional): Indicates whether the data is a list of dictionaries (True) or a list of lists (False). Defaults to True.
    """
    bufferData = ''
    bufferList = []
    checkList = []


    if filename.endswith(fileExt):
        pass
    else:
        _, filename = is_fileType(filename, fileExt)
    
    pastVersion = file_read(filename, fileExt) # Pre Update File

    # Data of Pre Update File
    if file_read(filename, fileExt) == []:
        pass
    else:
        for i in file_read(filename, fileExt):
            checkList.append(i)

        checkList.pop(0) # rids of Header

   
    if typeDict:
        
        try:
            # Header Writing
            with open(filename, "a") as file:
                key = list(dataframe[0].keys())
                if file_read(filename, fileExt) == []:
                    bufferData = ",".join(key)
                    file.write(bufferData + '\n')
                    bufferData = ''
                    
                else:
                    print("Headers Exist.")
                    bufferData = '' # Clear out the buffer
                    pass

                # Content Writing
                tempList = []
                bufferList = []
                for i in range(len(dataframe)):
                    for k in range(len(key)):
                        tempList.append(str([item[key[k]] for item in dataframe][i]))

                bufferList = [tempList[i:i+len(key)] for i in range(0, len(tempList), len(key))] # Only Values from dict

                for i in bufferList:
                    bufferData = ','.join(i)

                counter = 0
                decision = None
                for i in bufferList:
                    if i in checkList:
                        while counter+1 <= len(bufferList):
                            if decision == 'Y':
                                bufferData = ','.join(bufferList[counter])
                                file.write(bufferData + '\n')
                                decision = None
                                counter += 1

                            elif decision == "N":
                                decision = None
                                counter += 1

                            else:
                                decision = str(input(f'Duplicate data located {bufferList[counter]}: Proceed?[Y/N] ')).upper()
                    else:
                        bufferData = ','.join(i)
                        file.write(bufferData + '\n')
        
        except:
            print("Error occured at writing file. Refer: file_write(filename:str, fileExt:str ,data:list, typeDict=True)")      
         
        
    else:
        try:
            with open(filename, "a") as file:
                bufferList = []
                tempList = []
                bufferData = ''
                key = dataframe[0]
                
                if file_read(filename, fileExt) == []:
                    for i in dataframe[0]:
                        bufferList.append(i)
                    bufferData = ','.join(bufferList)

                    file.write(bufferData + '\n')
                else:
                    print("Header Exists.")
                    pass
                
                bufferList = [] # Resets bufferList
                
                for i in dataframe:
                    for n in i:
                        tempList.append(str(n))

                bufferList = [tempList[i:i+len(key)] for i in range(0, len(tempList), len(key))]
                bufferList.pop(0) # Remove Hearders from list
                counter = 0
                decision = None
                for i in bufferList:
                    if i in checkList:
                        while counter+1 <= len(bufferList):
                            if decision == 'Y':
                                bufferData = ','.join(bufferList[counter])
                                file.write(bufferData + '\n')
                                decision = None
                                counter += 1

                            elif decision == "N":
                                decision = None
                                counter += 1

                            else:
                                decision = str(input(f'Duplicate data located {bufferList[counter]}: Proceed?[Y/N] ')).upper()
                    else:
                        bufferData = ','.join(i)
                        file.write(bufferData + '\n')
        except:
            print("Error occured at writing file. Refer: file_write(filename:str, fileExt:str ,data:list, typeDict=False)")

    newVersion = file_read(filename, fileExt)

    if pastVersion != newVersion:
        print("Data Writing Success!")
    else:
        print("Data Writing Failed")              
               
        
    return

# File rewriting
def file_rewrite(filename:str, fileExt:str, dataframe:list, typeDict:bool=True):
    """
    Writes the given data to the specified file.
    WILL wipe existing data.

    Args:
        filename (str): The name of the file to save the data to.
        dataList (list): The data to be saved, either as a list of dictionaries (typeDict=True) or a list of lists (typeDict=False).
        typeDict (bool, optional): Indicates whether the data is a list of dictionaries (True) or a list of lists (False). Defaults to True.
    """

    if filename.endswith(fileExt):
        pass
    else:
        _, filename = is_fileType(filename, fileExt)

    pastVersion = file_read(filename, fileExt)
    tempList = []

    if typeDict:
        try:
            # Header Writing
            with open(filename, "w") as file:
                key = list(dataframe[0].keys())
                bufferData = ",".join(key)
                file.write(bufferData + '\n')
                bufferData = ''

                # Content Writing
                tempList = []
                bufferList = []
                for i in range(len(dataframe)):
                    for k in range(len(key)):
                        tempList.append(str([item[key[k]] for item in dataframe][i]))

                bufferList = [tempList[i:i+len(key)] for i in range(0, len(tempList), len(key))] # Only Values from dict

                for i in bufferList:
                    bufferData = ','.join(i)
                    file.write(bufferData + '\n') 

        except:
            print("Error occured at rewriting file. Refer: file_rewrite(filename:str, fileExt:str ,data:list, typeDict=True)")

    else:
        try:
            with open(filename, "w") as file:
                key = dataframe[0]
                bufferList = []
                bufferData = ''

                for i in dataframe[0]:
                    bufferList.append(i)
                bufferData = ','.join(bufferList)
                file.write(bufferData + '\n')
                
                bufferList = [] # Resets bufferList

                for i in dataframe:
                    for n in i:
                        tempList.append(str(n))

                bufferList = [tempList[i:i+len(key)] for i in range(0, len(tempList), len(key))]
                bufferList.pop(0) # Remove Hearders from list

                for i in bufferList:
                    bufferData = ','.join(i)
                    file.write(bufferData + '\n') 

        except:
            print("Error occured at rewriting file. Refer: file_rewrite(filename:str, fileExt:str ,data:list, typeDict=False)")


    newVersion = file_read(filename, fileExt)

    if pastVersion != newVersion:
        print("Data Writing Success!")
    else:
        print("Data Writing Failed")              

    return

# File checker
def view_files(fileExt):
    """
    Views all existing files with given extension files in same folder.
    """

    current_dir = os.getcwd()
    files = [f for f in os.listdir(current_dir) if f.endswith(fileExt)]

    for i in files:
        print(i)

# For Testing Purposes
if __name__ == '__main__':
    #print(dataframe(file_read('test.csv')))
    view_files()
    #file = open("", "a")
    #file.close()
    #file_write("test",[{"yes":"foo","no":"bar","to":6},{"yes":7,"no":8,"to":"ton"}], True)
    #file_write("test",[["yes", "no", "to"], ["fOO",3, "dog"], ["bar",7,"foo"]], False)
    #is_fileType("test")
    #print(file_read("test"))
    #file = open("payment_log.csv", "a")
    #file.close()
    #file_create()
