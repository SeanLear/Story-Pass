import secrets
from typing import List, Tuple

from sqlcipher3 import dbapi2 as sqlite3
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import authentication_database as ad

def get_encryption_key(username: str, password: str) -> bytes:
    """
    Derive the decrypted AES-256 encryption key used for encrypting/decrypting the
    user's database.

    args:
        username: The username for an account stored in the authentication database.
        password: User's authentication password associated with their account.
    returns:
        The decrypted AES-256 key used to encrypt/decrypt the user's database.
    """
    # Get encrypted AES-256 key, PBKDF2 salt, and nonce from authentication database.
    connection = sqlite3.connect("authentication.db")
    cursor = connection.cursor()
    query = f'''
    SELECT AES_key, PBKDF2_salt, nonce
    FROM authentication
    WHERE username = '{username}'
    '''
    result = cursor.execute(query)
    result_tuple = result.fetchone()
    #print(result_tuple)
    encrypted_AES_256_key = result_tuple[0]
    PBKDF2_salt = result_tuple[1]
    nonce = result_tuple[2]

    connection.close()

    # Hex -> bytes conversion
    encrypted_AES_256_key = bytes.fromhex(encrypted_AES_256_key)
    PBKDF2_salt = bytes.fromhex(PBKDF2_salt)
    nonce = bytes.fromhex(nonce)

    # Encode password into bytes
    password = password.encode("utf-8")

    # Generate PBKDF2 key to use to decrypt AES-256 key.
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                        length=32, 
                        salt=PBKDF2_salt,
                        iterations=1_000_000)
    PBKDF2_key = kdf.derive(password)
    #print(f"PBKDF2_key: {PBKDF2_key}")
    outer_AES_256_key = AESGCM(PBKDF2_key)

    # Decrypt AES-256 key using PBKDF2 derived key and nonce.
    decrypted_AES_256_key = outer_AES_256_key.decrypt(nonce, encrypted_AES_256_key, None)
    #print(f"decrypted_AES_256_key: {decrypted_AES_256_key}")

    # Generate a new nonce and re-encrypt AES-256 key.
    new_nonce = secrets.token_bytes(32)
    encrypted_AES_256_key = outer_AES_256_key.encrypt(new_nonce, decrypted_AES_256_key, None).hex()
    new_nonce = new_nonce.hex()

    # Update authentication database
    connection = sqlite3.connect("authentication.db")
    cursor = connection.cursor()
    query = f'''
    UPDATE authentication
    SET AES_key = '{encrypted_AES_256_key}', nonce = '{new_nonce}'
    WHERE username='{username}'
    '''
    cursor.execute(query)
    connection.commit()
    connection.close()

    return decrypted_AES_256_key

def get_user_data(username: str, password: str) -> List[Tuple]:
    """
    Get all of the data stored in the user's database as a list of tuples (one for each
    entry).

    args:
        username: The username for an account stored in the authentication database.
        password: User's authentication password associated with their account.
    returns:
        List of tuples, associated with each associated with a database entry.
    """
    # Get database encryption key.
    decrypted_AES_256_key = get_encryption_key(username, password)
    # Connect to user database.
    connection = sqlite3.connect(f"{username}.db")
    cursor = connection.cursor()
    # Decrypt database.
    decrypt_command = f'''
    PRAGMA key = "X'{decrypted_AES_256_key.hex()}'"
    '''
    # Get data contained in database.
    query = f'''
    SELECT *
    FROM accounts
    '''
    cursor.execute(decrypt_command)
    result = cursor.execute(query)
    result_tuple = result.fetchall()
    connection.close()

    return result_tuple

def check_account_name(account_name: str) -> int:
    """
    Check if an entry matching the provided account_name exists in the user's
    database.

    args:
        account_name: The account_name to check.
    returns:
        1: Account_name does NOT exist in the authentication database.
        -1: Account_name ALREADY exists in the authentication database.
    """
    connection = sqlite3.connect("authentication.db")
    cursor = connection.cursor()
    check_username = f'''
    SELECT account_name
    FROM accounts
    WHERE account_name = '{account_name}'
    '''
    result = cursor.execute(check_username)

    # Return 1 if username does NOT exist in the database, otherwise -1.
    if result.fetchone() is None:
        return 1
    else:
        return -1

def add_user_data(username: str, password: str, account_name: str, account_username: str, account_password: str) -> None:
    """
    Add an entry to the user's database.
    args:
        username: The username for an account stored in the authentication database.
        password: User's authentication password associated with their account.
        account_name: The name of the account to be added to the user's database
        account_username: The username of the account to be added to the user's database.
        account_password: The password of the account to be added to the user's database.
    """
    # Get database encryption key.
    decrypted_AES_256_key = get_encryption_key(username, password)
    # Connect to user database.
    connection = sqlite3.connect(f"{username}.db")
    cursor = connection.cursor()
    # Decrypt database.
    decrypt_command = f'''
    PRAGMA key = "X'{decrypted_AES_256_key.hex()}'"
    '''
    # Get data contained in database.
    query = f'''
    INSERT INTO accounts VALUES (?, ?, ?)
    '''
    cursor.execute(decrypt_command)
    cursor.execute(query, (account_name,
                           account_username,
                           account_password))
    connection.commit()
    connection.close()

def delete_user_data(username: str, password: str, account_name: str):
    """
    Delete an entry from the user's database.
    args:
        username: The username for an account stored in the authentication database.
        password: User's authentication password associated with their account.
        account_name: The name of the account to be deleted from the user's database
    """
    # Get database encryption key.
    decrypted_AES_256_key = get_encryption_key(username, password)
    # Connect to user database.
    connection = sqlite3.connect(f"{username}.db")
    cursor = connection.cursor()
    # Decrypt database.
    decrypt_command = f'''
    PRAGMA key = "X'{decrypted_AES_256_key.hex()}'"
    '''
    # Delete user database entry
    query = f'''
    DELETE FROM accounts
    WHERE account_name = '{account_name}'
    '''
    cursor.execute(decrypt_command)
    cursor.execute(query)
    connection.commit()
    connection.close()

def main():
    ad.create_authentication_database()

if __name__ == "__main__":
    main()