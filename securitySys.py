import random
import fileAP

"""
Password Encryption and OTP Management System

This module provides functionality for password encryption, decryption, and One-Time Password (OTP) management.
It includes custom encryption methods, password storage and validation, as well as OTP generation and validation.
"""
def encode_forbidden_chars(c, forbidden_characters:set):
    if c in forbidden_characters:
        return f'\\x{ord(c):02x}'  # Encodes forbidden characters as hex (e.g., '\x5c')
    return c


def custom_encrypt(password: str, salt: str, secret_key: str) -> str:
    """
    Encrypts the password using XOR operation with salt and secret key.

    Args:
    password (str): The password to encrypt.
    salt (str): A random string used to add complexity to the encryption.
    secret_key (str): A secret key used in the encryption process.

    Returns:
    str: The encrypted password.
    """
    forbidden_characters = {'n', ','}
    encrypted_password =  ''.join(chr(ord(password[i % len(password)]) ^ ord(secret_key[i % len(secret_key)]) ^ ord(salt[i % len(salt)])) for i in range(len(password)))
    return ''.join(encode_forbidden_chars(c, forbidden_characters) for c in encrypted_password)

def custom_decrypt(hex_encrypted_password: str, salt: str, secret_key: str) -> str:
    """
    Decrypts the encrypted password using the same XOR operation.

    Args:
    encrypted_password (str): The encrypted password to decrypt.
    salt (str): The salt used during encryption.
    secret_key (str): The secret key used during encryption.

    Returns:
    str: The decrypted password.
    """
    hex_decoded_password = []
    i = 0
    while i < len(hex_encrypted_password):
        if hex_encrypted_password[i:i+2] == '\\x':  # Check for the \x pattern
            hex_value = hex_encrypted_password[i+2:i+3]  # Get the two hex digits after \x
            hex_decoded_password.append(chr(int(hex_value, 16)))  # Convert hex to the original character
            i += 4  # Skip over the \x and the two hex digits
        else:
            hex_decoded_password.append(hex_encrypted_password[i])  # Append regular character
            i += 1
    encrypted_password = ''.join(hex_decoded_password)

    return ''.join(
        chr(ord(encrypted_password[i]) ^ ord(secret_key[i % len(secret_key)]) ^ ord(salt[i % len(salt)]))
        for i in range(len(encrypted_password))
    )

def create_salt(length: int = 5) -> str:
    """
    Generates a random salt of specified length using printable ASCII characters.

    Args:
    length (int): The length of the salt to generate. Defaults to 5.

    Returns:
    str: A random salt string.
    """
    return ''.join(chr(random.randint(33, 126)) for _ in range(length))

def store_password(password:str, secret_key:str) -> tuple[str, str]:
    """
    Encrypts the password and generates a salt, then stores them in a CSV file.

    Args:
    password (str): The password to store.
    secret_key (str): The secret key used for encryption.

    Returns:
    tuple: A tuple containing the encrypted password and the generated salt.
    """
    salt = create_salt()
    encrypted_password = custom_encrypt(password, salt, secret_key)
    password_record = {'encrypted_password': encrypted_password, 'salt': salt}
    
    fileAP.file_save_data("passwords", [password_record], ".csv", True, False)

    return encrypted_password, salt

def validate_password(stored_password:str, salt:str, input_password:str, secret_key:str) -> bool:
    """
    Validates an input password by encrypting it and comparing with stored encrypted password.

    Args:
    stored_password (str): The encrypted password stored in the system.
    salt (str): The salt used for encryption.
    input_password (str): The password input by the user for validation.
    secret_key (str): The secret key used for encryption.

    Returns:
    bool: True if the input password is valid, False otherwise.
    """
    encrypted_input = custom_encrypt(input_password, salt, secret_key)
    return stored_password == encrypted_input

def innit_security():
    secret_key = "my_secret_key"

    # Store a password
    password = input("Enter a password to store: ")
    encrypted_password, salt = store_password(password, secret_key)
    print(f"Stored encrypted password: {encrypted_password}, with salt: {salt}")

    # Validate the password
    input_password = input("Enter the password to validate: ")
    is_valid = validate_password(encrypted_password, salt, input_password, secret_key)
    print(f"Is the entered password valid? {is_valid}")

# For Testing         
if __name__ == '__main__':
    innit_security()