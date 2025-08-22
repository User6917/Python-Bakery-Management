"""
Recipe Management: Create, update, and delete digital recipes.
Inventory Check: Verify the availability of required ingredients. (Built into Production)
Production Record Keeping: Record production quantities, batch numbers, and expiration dates.
"""
import fileAP
import fileUtils
import os

def recipe_management(currentUser:str, fileExt:str):
    functionName = "Recipe Management"
    tableName = 'Recipes'
    csvBool, filename = fileAP.is_fileType("Recipe", fileExt)
    if csvBool:
        fileUtils.init_dbtools(currentUser, functionName, tableName, filename, fileExt)

    elif csvBool is False:
        filename = fileAP.file_create(filename, fileExt)
        recipe_management(currentUser, fileExt)

    else:
        print("Error at recipe_management(currentUser, fileExt)")

def inventory_request(requestItems:list, fileExt:str):
    requests = fileAP.dataframe(fileAP.file_read("Ingredient_request", fileExt), False)

    if requests == None:
        requestID = 0
    else:
        requestID = len(requests[1:])

    requestFormat = {
        "RequestID":f'Req{requestID+1:04}',
        "RequestItems":"; ".join(requestItems),
        "RequestStatus":"Not fulfilled"
    }
    fileAP.file_write("Ingredient_request", fileExt, [requestFormat])

def production(currentUser:str, fileExt:str):
    while True:
        recipeList = fileAP.dataframe(fileAP.file_read("Recipe", fileExt))
        inventoryList1 = fileAP.dataframe(fileAP.file_read('Ingredient_supply', fileExt))
        goods = fileAP.dataframe(fileAP.file_read('Goods_information', fileExt))
        cost = 0
        processItems = []
        requestItems = []
        bufferItems = []
        defaultOutput = 0

        tableName = 'Ingredients'
        fileUtils.tableFormat("Recipes", recipeList)
        fileUtils.tableFormat(tableName, inventoryList1)
        
        userInput = str(input(f'1 - Production\nE - Exit\n{currentUser} - '))
        try:
            if userInput == '1':
                requirementInput = str(input("Enter Recipe id: ")).upper()
                quantityInput = str(input("Enter production quantity in grams: "))
                quantityInput = fileUtils.digit_split(quantityInput)

                for r in recipeList:
                    if requirementInput == r['RecipeID']:
                        defaultOutput = r['Output Quantity(g)']
                        goodsName = r['Name']
                        ingredientNameList = [i.split(" ")[0] for i in r["Ingredients"].split("; ")]
                        ingredientList = [i.split(" ")[1] for i in r["Ingredients"].split("; ")]
                ratio = int(quantityInput) // int(defaultOutput)

                for i in range(len(ingredientNameList)):
                # Calculate required amount of each ingredient
                    required_amount = fileUtils.digit_split(ingredientList[i]) * ratio  # Update the ingredient amount
                    item_found = False  # Flag to track if the ingredient is found
                    sufficeState = 'Sufficient'

                # Check against inventory
                    for n in inventoryList1:
                        if ingredientNameList[i] == n['Name']: 
                            item_found = True
                            inventory_amount = fileUtils.digit_split(n['In-stock'])  # Get inventory amount
                            price, unit = n['Price(RM)'].split('/')
                            if inventory_amount > required_amount:
                                processItems.append(f'{ingredientNameList[i]} {str(required_amount)}')
                                cost += required_amount / 1000*int(price) if unit == 'Kg' or unit == 'L' else 12*int(price)
                                
                            else:
                                sufficeState = 'Insufficient'  
                        

                    if item_found == False:  # If the item was not found in the inventory
                        print(f'{ingredientNameList[i]} is not in Ingredient Supply. Currently requires {required_amount}')
                        requestItems.append([ingredientNameList[i], str(required_amount)])

                    elif sufficeState == 'Insufficient':
                        print(f'{n['UUID']}. {n['Name']}: {sufficeState}')  # Print sufficiency state
                        requestItems.append([ingredientNameList[i], str(required_amount)])

                if len(requestItems) == 0:
                    pass
                else:
                    for i in requestItems:
                        bufferItems.append(" ".join(i))
                    inventory_request(bufferItems, fileExt)
                    pause = input("=======[Enter to Continue]=======")

                for i in processItems:
                    itemName, itemQuantity = i.split(' ')
                    for e in inventoryList1:
                        if e['Name'] == itemName:
                            e.update({'In-stock': f'{fileUtils.digit_split(e['In-stock'])-int(itemQuantity)}{fileUtils.word_split(e['In-stock'])}'})
                
                for g in goods:
                    if g['Name'] in [r['Name'] for r in recipeList if r['RecipeID'] == requirementInput]:
                        for r in recipeList:
                            if r['Name'] == g['Name']:
                                storageQuantity = g['Quantity']
                                outputQuantity = r['Output Quantity(g)']
                        g.update({'Quantity': f'{quantityInput//int(outputQuantity)+int(storageQuantity)}'})

                fileUtils.tableFormat("Test Update", goods)
                #pause = input("=======[Enter to Continue]=======") # Use this for testing
                fileAP.file_rewrite("Goods_information", fileExt, goods)
                fileAP.file_rewrite("Ingredient_supply", fileExt, inventoryList1)

                records = fileAP.file_read("Production_record", ".csv")[1:]
                if len(records) == 0:
                    productionID = 1
                else:
                    productionID = fileUtils.digit_split(records[-1][0]) + 1

                productionRecord = {
                'ProductionID': f'PrID{productionID:04}',
                'ProducedItem': goodsName,
                'Quantity(g)': quantityInput,
                'IngredientsUsed': '; '.join(processItems),
                'TotalCost': f'RM{str(round(cost, 2))}'
                }
                
                fileAP.file_write("Production_record", fileExt, [productionRecord])
                pause = input("=====[Enter to Continue]=====")

            elif userInput.upper() == 'E':
                break

            else:
                print("Invalid Input") 
        except:
            print("Ivalid Input")  

def production_record_management(currentUser:str, fileExt:str):
    functionName = "Production Record Management"
    tableName = 'Production Records'
    csvBool, filename = fileAP.is_fileType("Production_record", fileExt)
    if csvBool:
        fileUtils.init_dbtools(currentUser, functionName, tableName, filename, fileExt)

    elif csvBool is False:
        filename = fileAP.file_create(filename, fileExt)
        production_record_management(currentUser, fileExt)
    
    else:
        print("Error at production_record_management(currentUser, fileExt)")
       
def goods_production_management(currentUser:str, fileExt:str):
    functionName = "Goods Production Management"
    tableName = 'Goods Records'
    csvBool, filename = fileAP.is_fileType("Goods_information", fileExt)
    if csvBool:
        fileUtils.init_dbtools(currentUser, functionName, tableName, filename, fileExt)

    elif csvBool is False:
        filename = fileAP.file_create(filename, fileExt)
        goods_production_management(currentUser, fileExt)
    
    else:
        print("Error at goods_production_management(currentUser:str, fileExt:str)")

def init_baker(currentUser:str):
    os.system('cls')
    bakerNames = ["Manage Recipe", "Production", "Production Record Management", "Goods Production Management"]
    fileExt = '.csv'
    while True:
        for i in range(len(bakerNames)):
                print(f'{i+1} - {bakerNames[i]}')
        print('E - Exit')
        action = str(input(f'{currentUser} - ')).upper()

        if action == '1': 
            recipe_management(currentUser, fileExt)

        elif action == '2':
            production(currentUser, fileExt)

        elif action == '3':
            production_record_management(currentUser, fileExt)
            
        elif action == '4':
            goods_production_management(currentUser, fileExt)

        elif action == 'E':
            print("Exiting Bakers Page.")
            break

        else:
            print('Invalid Input')

# For Testing         
if __name__ == '__main__':
    init_baker('Test')
