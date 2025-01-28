import tkinter as tk
from tkinter import messagebox

# revert main before pushing to not mess things up


class LandingPage:
    def __init__(self, app, grid_window, create_window):
        self.app = app
        self.change_window = grid_window
        self.create_window = create_window
        self.createWidgets()

    def createWidgets(self):
        #landingPage = tk.Toplevel(app)

        # create the landing page
        self.app.title("Landing Page")
        self.app.geometry("1400x800")

        # title
        title = tk.Label(self.app, text="Title Here")
        title.pack(pady=20)

        # username field
        self.username = tk.Entry(self.app, width = 50)
        self.username.pack(pady=20)

        # get buttons aligned 
        button_frame = tk.Frame(self.app)
        button_frame.pack()

        # create account button
        create_account = tk.Button(button_frame, text = "Create Account", command = self.create_window)
        create_account.pack(side = "left", padx = 10)

        # login button
        login = tk.Button(button_frame, text = "login", command= self.authUser)
        login.pack(side = "left", padx = 20)

  
    # auth func
    def authUser(self):
        user = self.username.get()

        # open grid for password
        if user == "admin":
            self.change_window()
        
        # throw an error
        # create custom alert later?
        # check number of attempts later
        else:
            self.username.delete(0, tk.END)
            messagebox.showerror("Error", "Invalid Username")
