import hashlib
import secrets

from sqlcipher3 import dbapi2 as sqlite3
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def create_authentication_database():
    """
    Create a database to store account usernames, their hashed passwords, and the salt used
    to hash the password, the salt used to derive a PBKDF2 key used to encrypt an AES-256 key
    from the user's password, the encrypted AES 256 key to encrypt/decrypt the user's database,
    and the current nonce used in AES 256 key encryption/decryption.
    """
    connection = sqlite3.connect("authentication.db")
    cursor = connection.cursor()
    create_table = '''
    CREATE TABLE IF NOT EXISTS authentication(
        username TEXT PRIMARY KEY,
        hashed_password TEXT NOT NULL,
        password_salt TEXT NOT NULL,
        PBKDF2_salt TEXT NOT NULL,
        AES_key TEXT NOT NULL,
        nonce TEXT NOT NULL
    )
    '''
    cursor.execute(create_table)
    connection.commit()
    connection.close()

def check_username(username: str) -> int:
    """
    Check if an entry matching the provided username exists in the authentication
    database.

    args:
        username: The username to check.
    returns:
        1: Username does NOT exist in the authentication database.
        -1: Username ALREADY exists in the authentication database.
    """
    connection = sqlite3.connect("authentication.db")
    cursor = connection.cursor()
    check_username = f'''
    SELECT username
    FROM authentication
    WHERE username = '{username}'
    '''
    result = cursor.execute(check_username)

    # Return 1 if username does NOT exist in the database, otherwise -1.
    if result.fetchone() is None:
        return 1
    else:
        return -1

def create_account(username: str, p_1: str, p_2: str, p_3: str, p_4: str, p_5: str, p_6: str) -> int:
    """
    Create an account entry in the authentication database and a new user database for
    the user if an account with the provided username does not already exist.

    args:
        username: Account's username
        p_1: password sequence part 1
        p_2: password sequence part 2
        p_3: password sequence part 3
        p_4: password sequence part 4
        p_5: password sequence part 5
        p_6: password sequence part 6
    returns:
        1: Account was successfully added to the database.
        -1: Account could not be added to the database.
    """
    # Only create an account if one does not already exist with supplied username.
    if check_username(username) == 1:
        connection = sqlite3.connect("authentication.db")
        cursor = connection.cursor()

        # Create password
        password = (p_1 + p_2 + p_3 + p_4 + p_5 + p_6).encode("utf-8")
        #print(f"password: {password}")

        # Generate a salt for the password.
        password_salt = secrets.token_bytes(32)
        # Salt and hash the provided password sequence.
        hashed_password = (p_1 + p_2 + p_3 + p_4 + p_5 + p_6).encode("utf-8")
        hashed_password += password_salt
        hashed_password = hashlib.sha256(hashed_password).hexdigest()
        #print(f"hashed_password: {hashed_password}")

        # Generate AES-256 key to encrypt user's associated user database.
        inner_AES_256_key = AESGCM.generate_key(bit_length=256)
        #print(f"AES_256_key: {inner_AES_256_key}")

        # Generate a salt for the PBKDF2 key.
        PBKDF2_salt = secrets.token_bytes(32)
        # Generate a PBKDF2 key to encrypt the inner AES-256 key using the user's password.
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                          length=32, 
                          salt=PBKDF2_salt,
                          iterations=1_000_000)
        PBKDF2_key = kdf.derive(password)
        #print(f"PBKDF2_key: {PBKDF2_key}")

        # Encrypt the inner AES-256 key used to encrypt user's associated database using
        # the outer AES-256 key generated from their password (PBKDF2)
        nonce = secrets.token_bytes(32)
        outer_AES_256_key = AESGCM(PBKDF2_key)
        encrypted_AES_256_key = outer_AES_256_key.encrypt(nonce, inner_AES_256_key, None)
        #print(f"encrypted_AES_256_key: {encrypted_AES_256_key}")
        decrypted_AES_256_key = outer_AES_256_key.decrypt(nonce, encrypted_AES_256_key, None)
        #print(f"decrypted_AES_256_key: {decrypted_AES_256_key}")

        #if inner_AES_256_key == decrypted_AES_256_key:
            #print("AES_256 key successfully encrypted and decrypted.")

        # Byte -> hex conversion prior to insert
        password_salt = password_salt.hex()
        PBKDF2_salt = PBKDF2_salt.hex()
        encrypted_AES_256_key = encrypted_AES_256_key.hex()
        nonce = nonce.hex()

        # Insert the username, salted and hashed password, and the salt used to the database.
        insert_account = '''
        INSERT INTO authentication VALUES (?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(insert_account, (username,
                                        hashed_password,
                                        password_salt,
                                        PBKDF2_salt,
                                        encrypted_AES_256_key,
                                        nonce))
        connection.commit()
        connection.close()

        # Create encrypted database for user's account data
        connection = sqlite3.connect(f"{username}.db")
        cursor = connection.cursor()
        encrypt_database = f'''
        PRAGMA key = "X'{decrypted_AES_256_key.hex()}'"
        '''
        cursor.execute(encrypt_database)

        # Create accounts table in user's database
        create_table = '''
        CREATE TABLE IF NOT EXISTS accounts(
            account_name TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        '''
        cursor.execute(create_table)
        connection.commit()
        connection.close()
        return 1
    else:
        return -1

def delete_account(username: str) -> int:
    """
    Remove an account entry from the authentication database if one exists with the
    provided username.

    args:
        username: Username associated with account to be deleted.
    returns:
        1: Account successfully deleted.
        -1: Account could not be deleted (does not exist).
    """
    # Only delete an account if it already exists with supplied username
    if check_username(username) == -1:
        connection = sqlite3.connect("authentication.db")
        cursor = connection.cursor()
        delete_account = f'''
        DELETE FROM authentication
        WHERE username = '{username}'
        '''
        cursor.execute(delete_account)
        connection.commit()
        connection.close()
        return 1
    else:
        return -1

def check_account_password(username: str, p_1: str, p_2: str, p_3: str, p_4: str, p_5: str, p_6: str) -> int:
    """
    Check if the provided password sequence matches the hashed version stored in the authentication database.

    args:
        username: Account's username
        p_1: password sequence part 1
        p_2: password sequence part 2
        p_3: password sequence part 3
        p_4: password sequence part 4
        p_5: password sequence part 5
        p_6: password sequence part 6
    returns:
        1: Provided username and password are a correct match.
        -1: Provided username and password are not a correct match.
        -2: Account with provided username does not exist.
    """
    if check_username(username) == -1:
        connection = sqlite3.connect("authentication.db")
        cursor = connection.cursor()
        # Get hashed password and its salt stored in database.
        get_password = f'''
        SELECT hashed_password, password_salt
        FROM authentication
        WHERE username = '{username}'
        '''
        result = cursor.execute(get_password)
        result_tuple = result.fetchone() 
        stored_password = result_tuple[0]
        password_salt = result_tuple[1]

        # Hex -> bytes conversion
        password_salt = bytes.fromhex(password_salt)

        # Salt and Hash provided password sequence to compare with stored password.
        hashed_password = (p_1 + p_2 + p_3 + p_4 + p_5 + p_6).encode("utf-8")
        hashed_password += password_salt
        hashed_password = hashlib.sha256(hashed_password).hexdigest()

        # Check if provided username's password sequence is a match.
        if stored_password == hashed_password:
            return 1
        else:
            return -1
    else:
        # Account does not exist with provided username.
        return -2

def update_account_password(username: str, p_1: str, p_2: str, p_3: str, p_4: str, p_5: str, p_6: str) -> int:
    """
    Update password associated with username's entry in authentication database.

    args:
        username: Account's username
        p_1: password sequence part 1
        p_2: password sequence part 2
        p_3: password sequence part 3
        p_4: password sequence part 4
        p_5: password sequence part 5
        p_6: password sequence part 6
    returns:
        1: Password successfully updated in database.
        -1: Password could not be updated (account does not exist).
    """
    if check_username(username) == -1:
        connection = sqlite3.connect("authentication.db")
        cursor = connection.cursor()
        # Generate a salt for the password.
        password_salt = secrets.token_bytes(32)
        # Salt and hash the provided password sequence.
        hashed_password = (p_1 + p_2 + p_3 + p_4 + p_5 + p_6).encode("utf-8")
        hashed_password += password_salt
        hashed_password = hashlib.sha256(hashed_password).hexdigest()
        password_salt = password_salt.hex()
        # Update account's stored password in authentication database
        change_password = f'''
        UPDATE authentication
        SET hashed_password = '{hashed_password}', password_salt = '{password_salt}'
        WHERE username = '{username}'
        '''
        cursor.execute(change_password)
        connection.commit()
        connection.close()
        return 1
    else:
        return -1
