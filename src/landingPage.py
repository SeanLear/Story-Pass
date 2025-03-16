"""
Author: Will Marceau
Course: CS 433
Term: Winter 25
"""
import tkinter as tk
from tkinter import messagebox
from user_info import UserInfo
from authentication_database import check_username
from PIL import Image, ImageTk
from username import Username


class LandingPage:
    def __init__(self, app, grid_window, create_window):
        self.app = app
        self.grid_window = grid_window
        self.create_window = create_window
        self.createWidgets()

    def createWidgets(self):
        # create icon 
        png = Image.open("../imgs/StoryPass_Logo.webp")
        png.save("../imgs/StoryPass_Logo.png")
        icon = ImageTk.PhotoImage(file="../imgs/StoryPass_Logo.png")
        self.app.wm_iconphoto(True, icon)

        #landingPage = tk.Toplevel(app)

        # create the landing page
        self.app.title("Story-Pass - Landing Page")
        self.app.geometry("800x500")

        # title
        title = tk.Label(self.app, text="Story-Pass", font=("TkDefaultFont", 55, "bold"))
        title.pack(pady=(100, 20))


        # username field
        #self.username = tk.Entry(self.app, width = 50, bd = 2, relief = "solid")
        #self.username.pack(pady=20)
        #self.username.focus_set()

        # get buttons aligned 
        button_frame = tk.Frame(self.app)
        button_frame.pack()

        # create account button
        create_account = tk.Button(button_frame, text = "Create Account", font = ("TkDefaultFont", 27), command = self.accountCreation)
        create_account.pack(side = "left", padx = 10)

        # login button
        login = tk.Button(button_frame, text = "Login", font = ("TkDefaultFont", 27), command= self.login)
        login.pack(side = "left", padx = 20)

  
    # auth func
    """
    def authUser(self):
        user = self.username.get()

        # open grid for password
        if (check_username(user)) == -1:
            # destroy widgets and switch to grid
            for widget in self.app.winfo_children():
                widget.destroy()
            self.grid_window(self.app, UserInfo, LandingPage, user)
        
        # throw an error
        # create custom alert later?
        # check number of attempts later
        elif (check_username(user)) == 1:
            self.username.delete(0, tk.END)
            messagebox.showerror("Error", "Invalid Username")
    """

    def login(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        Username(self.app, self.grid_window, LandingPage, self.create_window)


    def accountCreation(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.create_window(self.app, LandingPage, self.grid_window)