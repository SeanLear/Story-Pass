import tkinter as tk
from tkinter import messagebox
from user_info import UserInfo
from authentication_database import check_username

class Username:
    def __init__(self, app, grid_window, back, create_window):
        self.app = app
        self.grid_window = grid_window
        self.back = back
        self.create_window = create_window
        self.createWidgets()

    def createWidgets(self):
        self.app.title("Story-Pass - Username")
        self.app.geometry("800x500")

        # title
        title = tk.Label(self.app, text="Enter Username:", font=("TkDefaultFont", 35))
        title.pack(pady=(100, 20))

        # username field
        self.username = tk.Entry(self.app, width = 50, bd = 2, relief = "solid")
        self.username.pack(pady=20)
        self.username.focus_set()

        # get buttons aligned 
        button_frame = tk.Frame(self.app)
        button_frame.pack()

        # create cancel button
        cancel_button = tk.Button(button_frame, text="Cancel", font = ("TkDefaultFont", 16), command=lambda: self.leave())
        cancel_button.pack(side=tk.LEFT, padx = 10, pady = 10)

        # create account button
        continue_bttn = tk.Button(button_frame, text = "Continue", font = ("TkDefaultFont", 16), command = self.cont)
        continue_bttn.pack(side = "left", padx = 10)

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

    def leave(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.back(self.app, self.grid_window, self.create_window)

    def cont(self):
        user = self.username.get()

        # open grid for password
        if (check_username(user)) == -1:
            # destroy widgets and switch to grid
            for widget in self.app.winfo_children():
                widget.destroy()
            self.grid_window(self.app, UserInfo, self.back, user)
        
        # throw an error
        # create custom alert later?
        # check number of attempts later
        elif (check_username(user)) == 1:
            self.username.delete(0, tk.END)
            messagebox.showerror("Error", "Invalid Username")