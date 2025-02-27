import tkinter as tk
from PIL import Image, ImageTk
import random
from tkinter import messagebox
from signUp import SignUp
from authentication_database import check_account_password

class Grid:
    def __init__(self, app, accept, deny, username):
        self.app = app
        self.accept = accept
        self.deny = deny
        self.attempts = 3
        self.username = username

        # create button list
        self.button_info = [["../imgs/apartment.webp", "apartment"], ["../imgs/apple.webp", "apple"], 
            ["../imgs/backpack.webp", "backpack"], ["../imgs/baseball.webp", "baseball"], ["../imgs/beach.webp", "beach"],
            ["../imgs/bear.webp", "bear"], ["../imgs/bicycle.webp", "bicycle"], ["../imgs/chicken.webp", "chicken"],
            ["../imgs/firetruck.webp", "firetruck"], ["../imgs/fish.webp", "fish"], ["../imgs/football.webp", "football"],
            ["../imgs/frog.webp", "frog"], ["../imgs/hamburger.webp", "hamburger"], ["../imgs/headphones.webp", "headphones"],
            ["../imgs/hotdog.webp", "hotdog"], ["../imgs/house.webp", "house"], ["../imgs/icecream.webp", "icecream"],
            ["../imgs/keys.webp", "keys"], ["../imgs/motorcycle.webp", "motorcycle"], ["../imgs/park.webp", "park"], 
            ["../imgs/phone.webp", "phone"], ["../imgs/plane.webp", "planes"], ["../imgs/rabbit.webp", "rabbit"], 
            ["../imgs/restaurant.webp", "restaurant"], ["../imgs/salad.webp", "salad"], ["../imgs/taxi.webp", "taxi"], 
            ["../imgs/tiger.webp", "tiger"], ["../imgs/tree.webp", "tree"], ["../imgs/truck.webp", "truck"], 
            ["../imgs/wallet.webp", "wallet"]]

        # create image ref to prevent early deletion
        self.image_refs = []

        # set up image correlation
        self.image_map = {"apartment" : "v%",
            "apple" : ".O",
            "backpack" : "94",
            "baseball" : "@#",
            "beach" : "L$",
            "bear" : "?b",
            "bicycle" : "4Q",
            "chicken" : "7e",
            "firetruck" : "M&",
            "fish" : "+U",
            "football" : "P9",
            "frog" : "x*",
            "hamburger" : "Kj",
            "headphones" : "8r",
            "hotdog" : "y#",
            "house" : "N0",
            "icecream" : "AG",
            "keys" : "!2",
            "motorcycle" : "^t",
            "park" : "Z(",
            "phone" : "}{",
            "planes" : "fw",
            "rabbit" : "i=",
            "restaurant" : "Hb",
            "salad" : "81",
            "taxi" : "s6",
            "tiger" : "D;",
            "tree" : ".-",
            "truck" : "c[",
            "wallet" : "^]",
        }

        # set pass hold
        self.entered_pass = []

        # button counter
       # self.bttn_counter = tk.IntVar()
       # self.bttn_counter.set(6)
        self.bttn_counter = 6

        # feedback string
        self.feedback = tk.StringVar()
        self.feedback.set("Remaining Choices: " + str(self.bttn_counter))

        # set up window
        self.createWidgets()

    def createWidgets(self):
        self.app.title("Story-Pass Password Grid")
        self.app.geometry("1150x800")

        # set up title frame
        title_frame = tk.Frame(self.app)
        title_frame.pack()

        # title
        title = tk.Label(title_frame, text="Enter Password:", font = ("TkDefaultFont", 25))
        title.pack(pady=10)

        show_pass = tk.Label(title_frame, textvariable=self.feedback, font = ("TkDefaultFont", 14))
        show_pass.pack(pady=10)

        # pack grid frame
        grid_frame = tk.Frame(self.app)
        grid_frame.pack()

        # randomize button list
        random.shuffle(self.button_info)

        # set up grid size
        cols = 6

        for index, (path, click) in enumerate(self.button_info):
            # calc index
            row, col = divmod(index, cols)

            # create image
            img = Image.open(path)
            img = img.resize((100, 100))
            photo = ImageTk.PhotoImage(img)

            # prevent deletion
            self.image_refs.append(photo)

            # create button
            btn = tk.Button(grid_frame, image=photo, command=lambda label=click: self.onClick(label))
            btn.grid(row=row, column=col, padx=10, pady=10)

        # grid
        
        # create frame for button
        bttn_frame = tk.Frame(self.app)
        bttn_frame.pack()

        # create cancel button
        cancel_button = tk.Button(bttn_frame, text="Cancel", font = ("TkDefaultFont", 18), command=lambda: self.leave())
        cancel_button.pack(side=tk.LEFT, padx = 10, pady = 10)

        # create reset button
        reset_button = tk.Button(bttn_frame, text="Reset Attempt", font = ("TkDefaultFont", 18), command=lambda: self.reset())
        reset_button.pack(side = tk.LEFT, padx = 10, pady = 10)
        
    def onClick(self, label):
        self.entered_pass.append(self.image_map[label])
        self.bttn_counter -= 1
        self.feedback.set("Remaining Choices: " + str(self.bttn_counter))

        # auth password
        if len(self.entered_pass) == 6:
            # hard code password
            if (check_account_password(self.username, self.entered_pass[0], self.entered_pass[1], self.entered_pass[2], self.entered_pass[3], self.entered_pass[4], self.entered_pass[5])) == 1:
                messagebox.showinfo("Success", "Login Successful")

                # delete widgets and switch to user info
                for widget in self.app.winfo_children():
                    widget.destroy()
                self.accept(self.app, self.username)
            
            else:
                # if not authenticated
                if self.attempts > 0:
                    messagebox.showerror("Error", "Invalid Password\n Attempts Remaining: " + str(self.attempts))
                    self.entered_pass = []
                    self.bttn_counter = 6
                    self.feedback.set("Remaining Choices: " + str(self.bttn_counter))
                    self.attempts -= 1
                else:
                    messagebox.showerror("Error", "Invalid Password\n 0 Attempts Remaining, Returing to Landing Page")

                    # destroy widgets and switch to landing page
                    for widget in self.app.winfo_children():
                        widget.destroy()
                    self.deny(self.app, Grid, SignUp)

    def reset(self):
        # this function resets the entered password

        print("reseting entered password")
        self.entered_pass = []
        self.bttn_counter = 6
        self.feedback.set("Remaining Choices: " + str(self.bttn_counter))


    def leave(self):
        # this function returns the user to the landing page
        for widget in self.app.winfo_children():
            widget.destroy()
        self.deny(self.app, Grid, SignUp)
