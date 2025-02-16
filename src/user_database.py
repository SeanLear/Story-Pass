import hashlib
import secrets

from sqlcipher3 import dbapi2 as sqlite3
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import authentication_database as ad

def encrypt_user_database(username: str, password: str):
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
    print(result_tuple)
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
    print(f"PBKDF2_key: {PBKDF2_key}")
    outer_AES_256_key = AESGCM(PBKDF2_key)

    # Decrypt AES-256 key using PBKDF2 derived key and nonce.
    decrypted_AES_256_key = outer_AES_256_key.decrypt(nonce, encrypted_AES_256_key, None)
    print(f"decrypted_AES_256_key: {decrypted_AES_256_key}")

    # Encrypt user's database using decrypted AES-256 key.
    decrypted_AES_256_key_hex = decrypted_AES_256_key.hex()
    decrypt_command = f'''
    PRAGMA key = "X'{decrypted_AES_256_key}'"
    '''

    # Execute encryption command
    connection = sqlite3.connect(f"{username}.db")
    cursor = connection.cursor()
    cursor.execute(decrypt_command)
    connection.commit()
    connection.close()

    # Generate a new nonce and re-encrypt AES-256 key.
    new_nonce = secrets.token_bytes(32)
    encrypted_AES_256_key = outer_AES_256_key.encrypt(new_nonce, decrypted_AES_256_key, None).hex()
    new_nonce = new_nonce.hex()

    # Update authentication database
    connection = sqlite3.connect("authentication.db")
    cursor = connection.cursor()
    query = f'''
    UPDATE authentication
    SET AES_key = X'{encrypted_AES_256_key}', nonce = X'{new_nonce}'
    WHERE username='{username}'
    '''
    cursor.execute(query)
    connection.commit()
    connection.close()

def get_encryption_key(username: str, password: str):
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
    print(result_tuple)
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
    print(f"PBKDF2_key: {PBKDF2_key}")
    outer_AES_256_key = AESGCM(PBKDF2_key)

    # Decrypt AES-256 key using PBKDF2 derived key and nonce.
    decrypted_AES_256_key = outer_AES_256_key.decrypt(nonce, encrypted_AES_256_key, None)
    print(f"decrypted_AES_256_key: {decrypted_AES_256_key}")

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

def get_user_data(username: str, password: str):
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

def add_user_data(username: str, password: str, account_name: str, account_username: str, account_password: str):
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
    print(ad.create_account("new_test", "a", "b", "c", "d", "e", "f"))
    print(ad.check_account_password("new_test", "a", "b", "c", "d", "e", "f"))
    print(add_user_data("new_test", "abcdef", "USAA", "sean", "123"))
    print(get_user_data("new_test", "abcdef"))
    print(delete_user_data("new_test", "abcdef", "USAA"))
    print(get_user_data("new_test", "abcdef"))


if __name__ == "__main__":
    main()