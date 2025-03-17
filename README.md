# Story-Pass

Story-Pass is a local, encrypted password manager that utilizes a graphical, story-based
password scheme. Users create a story by selecting a sequence of six images that forms
the password to their encrypted password vault. By creating a story, users are better
able to recall their password when compared to a conventional textual password.

## Requirements

Story-Pass is officially supported on MacOS (x86) and requires the following:

1. Python3 (Developed on 3.13)
2. Python's virtual environment module venv
3. The Tcl/Tk Python GUI toolkit
    - If you installed Python via the binary installer provided by [python.org](https://www.python.org/),
    the Tcl/Tk GUI toolkit is included in your installation.
    - If you installed Python via [Homebrew](https://brew.sh/), you will need to run the following commands to
    ensure you have Tcl/Tk installed:
        - `brew update`
        - `brew install python-tk`
4. SQLCipher
    - To install SQLCipher, we recommend using [Homebrew](https://brew.sh/).
    - With Homebrew installed, run the following commands:
        - `brew update`
        - `brew install sqlcipher`

## Running the Program

To run Story-Pass:

1. [Download](https://github.com/SeanLear/CS433/archive/refs/heads/main.zip) Story-Pass's
zipped repo from github.
2. Unzip the downloaded repo.
3. Using your terminal, navigate to the repo's top level.
4. From the repo's top level, run the command:
    - `bash run.sh`
5. Wait as a virtual environment is created and all dependencies are installed, Story-Pass
will automatically run once completed.

NOTE: ARM based MacOS will almost certainly fail to run, as the wheels for ARM are NOT included in the sqlcipher3 package.

## Usage Instructions

### Creating a Story-Pass account

From the Story-Pass landing page:

1. Click the "Create Account" button.
2. Enter a username in the "Create Username" form.
3. Select a sequence of six images from the image grid presented below "Create Password"
    - While selecting six images, create your own story to aid in password recall.
    - For example, you might select the images (headphones, plane, taxi, hotel, wallet, keys)
    and think of the story "I listened to my headphones on the plane, then took a taxi
    to my hotel where I realized I forgot my wallet and keys".
    - If successful, the prompt "Please Re-enter password" will appear.
    - Click OK on the prompt.
4. When prompted, re-enter the password you created in step 3.
    - If successful, the prompt "Password Set, Submit to Create Account" will appear.
    - Click OK on the prompt.
5. Click the "Submit Account" button.
    - If successful, the prompt "Account Creation Successful, please Log In" will appear.
    - Click Ok on the prompt.

### Logging into your Story-Pass account

From the Story-Pass landing page:

1. Click the "Login" button.
2. Enter your username in the "Enter Username" form and click "Continue".
3. Select the sequence of six images you chose during your account creation.
    - To aid in recalling the images, think of the story you created.
    - If you click on the wrong image during selection, click on the "Reset Attempt"
    button to start again.
    - After selecting the sequence of six images:
        - If unsuccessful, the prompt "Invalid Password" will appear.
            - Click OK on the prompt.
            - Reattempt selecting your password sequence (You have 3 attempts before account lockout).
        - If successful, the prompt "Login Successful" will appear.
            - Click OK on the prompt.
4. After successfully logging in you will be presented with you password vault.

### Adding an account to your password vault

After successfully logging into your account, with your password vault open:

1. Click the "Add Account" button.
2. In the "Enter Account Name" form that appears, enter the name of the account to add.
3. In the "Enter Account Username" form that appears, enter the username of the account to add.
4. In the "Enter Account Password" form that appears, enter the password of the account to add.
5. If successful, the prompt "Account added successfully!" will appear.
    - Click OK on the prompt.
6. The new account will appear in your password vault.

### Removing an account from your password vault

After successfully logging into your account, with your password vault open:

1. Click the "Delete Account" button.
2. In the "Account for deletion" form that appears, enter the name of the account to delete.
    - If the account exists, the prompt "{account name} deleted successfully!".
        - Click OK on the prompt.
    - If the account does not exist, the prompt "{account name} doesn't exist".
        - Click OK on the prompt.
3. The deleted account will be removed from your password vault.

### Logging out of your Story-Pass account

After successfully logging into your account, with your password vault open:

1. Click the "Logout" button.
2. You will be returned to the Story-Pass landing page where you can log back in.

### Exiting Story-Pass

To exit Story-Pass at any point:

1. Click the red "x" button in the top left-hand corner of the application.
2. Alternatively, you can enter the command `ctrl+c` from your terminal.
