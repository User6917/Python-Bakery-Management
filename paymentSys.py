from datetime import datetime  
import fileAP 
import fileUtils

"""
Payment System Module
This module provides functionality for initiating payments, storing transaction records,
and viewing transaction history. It uses both in-memory storage and CSV file logging
for maintaining transaction records.
"""

# Initialize variables
paymentRecords = fileAP.dataframe(fileAP.file_read("payment_log", ".csv"))  # In-memory list to store transaction records
filename = "payment_log"  # Filename for logging transactions to a CSV file

def initiate_payment(amount: float, payment_method: str) -> str:
    """
    Initiate a payment transaction.
    Args:
    amount (float): The amount to be paid.
    payment_method (str): The method used for payment (e.g., "Credit Card", "PayPal").
    Returns:
    str: A confirmation message indicating the status of the payment.
    """
    print(f"Initiating payment for RM{amount} via {payment_method}...")
    confirmation_message = "Payment successful" 
    print(confirmation_message)
    return confirmation_message

def store_payment_record(orderID, amount: float) -> list:
    """
    Store a payment transaction record in memory and CSV file.
    Args:
    amount (float): The amount paid in the transaction.
    payment_method (str): The method used for payment.
    Returns:
    list: Updated payment history list containing all transactions.
    """
    
    if len(paymentRecords) == None:
        paymentID = 0
    else:
        paymentID = len(paymentRecords) + 1

    transaction = {
        'PaymentID':f'Pay{paymentID:04}',
        'OrderID':orderID,
        'Amount':f'RM{amount}',
        'Payment_method': '-',
        'Payment_status': 'Unpaid',
        'Timestamp': '-',
    }
    paymentRecords.append(transaction)
    fileAP.file_save_data(filename, [transaction], ".csv", typeDict=True, overwrite=False)
    print("New Record Stored")

def update_payment_record(orderID, paymentMethod):
    timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for paymentRecord in paymentRecords:
        if paymentRecord["OrderID"] == orderID:
            paymentRecord.update({"Payment_method": paymentMethod,
                                 "Payment_status": 'Paid',
                                 "Timestamp": timeStamp})
    fileAP.file_save_data(filename, paymentRecords, ".csv", typeDict=True, overwrite=True)
    print("Record Changes Stored.")

def init_main(orderID) -> None:
    """
    Main function to demonstrate the payment system functionality.
    This function allows the user to choose a payment method, initiate a payment,
    store the transaction record, and view the transaction history.
    """
    for paymentRecord in paymentRecords:
        if paymentRecord['OrderID'] == orderID:
            amount = fileUtils.digit_split(paymentRecord['Amount'])

    payment_methods = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer", "Cash"]
    print("Available payment methods:")
    
    for i in range(len(payment_methods)):
        print(f"{i+1}. {payment_methods[i]}")
    choice = int(input("Choose a payment method (1-5): ")) - 1
    if 0 <= choice < len(payment_methods):
        payment_method = payment_methods[choice]

    else:
        print("Invalid choice. Using default payment method: Credit Card.")
    
    confirmation_message = initiate_payment(amount, payment_method)
    
    if confirmation_message == "Payment successful":
        update_payment_record(orderID, payment_method)

# For Testing         
if __name__ == '__main__':
    init_main('OID16161210582024')