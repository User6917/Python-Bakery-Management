# PwP Bakery Management System

A comprehensive bakery management system written in Python, designed to handle all aspects of bakery operations, including inventory, orders, production, payments, and user roles.

## Features

- **User Roles:** Supports Baker, Cashier, Customer, Manager, Superadmin, and Supplier, each with dedicated interfaces and permissions.
- **Account Management:** Secure login/signup with password encryption ([`securitySys`](securitySys.py)), and account management for users.
- **Product & Inventory Management:** Manage recipes, ingredients, hardware, and finished goods ([`Baker`](Baker.py), [`Manager`](Manager.py)).
- **Order System:** Customers can browse products, manage carts, place orders, and track order status ([`Customer`](Customer.py)).
- **Production Tracking:** Bakers can record production batches and update inventory.
- **Payment System:** Handles payment initiation, logging, and status updates ([`paymentSys`](paymentSys.py)).
- **Reporting:** Cashiers and managers can generate sales and transaction reports ([`Cashier`](Cashier.py)).
- **File Management:** All data is stored in CSV files for easy access and backup ([`fileAP`](fileAP.py), [`fileUtils`](fileUtils.py)).

## Getting Started

### Prerequisites

- Python 3.10 or higher

### Running the Application

1. Clone or download this repository.
2. Ensure all `.py` and `.csv` files are in the same directory.
3. Run the main script:

   ```sh
   python main.py
   ```

4. Follow the on-screen prompts to log in or sign up, and navigate the system based on your user role.
5. User credentials are as follows:
        Email               Password   Role
        admin@gmail.com:    admin      Admin
        baker@gmail.com:    baker123   Baker
        cashier@gmail.com:  cashier    Cashier
        user@gmail.com:     user       Customer
        supplier@gmail.com: supplier   Supplier
        manager@gmail.com:  manager    Manager


## File Structure

- `main.py` - Entry point and main menu logic.
- `Baker.py`, `Cashier.py`, `Customer.py`, `Manager.py`, `Superadmin.py`, `Supplier.py` - Role-specific modules.
- `fileAP.py`, `fileUtils.py` - File and data manipulation utilities.
- `securitySys.py` - Password encryption and security.
- `paymentSys.py` - Payment processing.
- CSV files (`Accounts.csv`, `Orders.csv`, etc.) - Data storage.

## Notes

- All data is stored in CSV files for simplicity and portability.
- Passwords are encrypted using a custom method for basic security.
- The system is designed for educational and demonstration purposes.

## Contributors

- [@User6917](https://github.com/User6917)
- [@nat322](https://github.com/nat322)
- [@PCV939](https://github.com/PCV939)
- [@ARUYIE](https://github.com/ARUYIE)

## License

This project is licensed under the MIT License.
