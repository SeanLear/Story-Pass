import sqlite3
import hashlib

def create_authentication_database():
    """
    Create a database to store account usernames and their passwords stored 
    as a sequence of six strings, each associated with an image.
    """
    connection = sqlite3.connect("authentication.db")
    cursor = connection.cursor()
    create_table = '''
    CREATE TABLE IF NOT EXISTS authentication(
        username TEXT,
        password TEXT,
        PRIMARY KEY (username)
    )
    '''
    cursor.execute(create_table)
    connection.commit()
    connection.close()

def check_username(username: str) -> int:
    """
    Check if the provided username exists in the authentication database.

    args:
        username: The username to check.
    returns:
        1: Username does not exist in the authentication database.
        -1: Username already exists in the authentication database.
    """
    connection = sqlite3.connect("authentication.db")
    cursor = connection.cursor()
    check_username = f'''
    SELECT username FROM authentication WHERE username = '{username}'
    '''
    result = cursor.execute(check_username)

    # Return 1 if username does not exist in the database, otherwise -1.
    if result.fetchone() is None:
        return 1
    else:
        return -1

def create_account(username: str, p_1: str, p_2: str, p_3: str, p_4: str, p_5: str, p_6: str) -> int:
    """
    Create an account entry in the database if an account with the provided username does not exist.

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
    # Only create an account if one does not already exist with supplied username
    if check_username(username) == 1:
        connection = sqlite3.connect("authentication.db")
        cursor = connection.cursor()
        # Hash the provided password sequence before insertion
        password_sequence_bytestring = (p_1 + p_2 + p_3 + p_4 + p_5 + p_6).encode("utf-8")
        hashed_password_sequence = hashlib.sha256(password_sequence_bytestring).hexdigest()
        insert_account = '''
        INSERT INTO authentication VALUES (?, ?)
        '''
        cursor.execute(insert_account, (username, hashed_password_sequence))
        connection.commit()
        connection.close()
        return 1
    else:
        return -1

def delete_account(username: str) -> int:
    """
    Remove an account entry from the authentication database if one exists with the provided username.

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
        DELETE FROM authentication WHERE username = '{username}'
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
        # Get hashed password stored in database
        get_password = f'''
        SELECT password FROM authentication WHERE
        username = '{username}'
        '''
        result = cursor.execute(get_password)
        stored_password = result.fetchone()[0] 

        # Hash provided password sequence
        password_sequence_bytestring = (p_1 + p_2 + p_3 + p_4 + p_5 + p_6).encode("utf-8")
        hashed_password_sequence = hashlib.sha256(password_sequence_bytestring).hexdigest()

        # Provided username and password sequence are a match
        if stored_password == hashed_password_sequence:
            return 1
        else:
            return -1
    else:
        # Account does not exist with provided username
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
        # Hash provided password sequence
        password_sequence_bytestring = (p_1 + p_2 + p_3 + p_4 + p_5 + p_6).encode("utf-8")
        hashed_password_sequence = hashlib.sha256(password_sequence_bytestring).hexdigest()
        # Update account's stored password in authentication database
        change_password = f'''
        UPDATE authentication SET password = '{hashed_password_sequence}' WHERE username = '{username}'
        '''
        cursor.execute(change_password)
        connection.commit()
        connection.close()
        return 1
    else:
        return -1
