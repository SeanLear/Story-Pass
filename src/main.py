import tkinter as tk
from landingPage import LandingPage
from grid import Grid
from signUp import SignUp
from authentication_database import create_authentication_database

class MainApp(tk.Tk):
    def __init__(self):
        # setting up window and starting login process
        super().__init__()
        self.title("PlaceHolder Name")
        self.geometry("1400x800")
        self.current_window = None
        
        self.start()

    def start(self):
        # this function starts the login process by bringing up the username
        #window

        # create auth database if doesn't exist already
        create_authentication_database()

        # pass until username window is pushed
        LandingPage(self, Grid, SignUp)

    def grid(self):
        # this funciton will start the grid window if the user passes the 
        # username check

        # pass until grid window has been set up
        pass

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()