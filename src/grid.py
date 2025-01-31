import tkinter as tk
from PIL import Image, ImageTk
import random
from tkinter import messagebox

class Grid:
    def __init__(self, app, accept, deny):
        self.app = app
        self.accept = accept
        self.deny = deny

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
        self.entered_pass = ""

        # set up window
        self.createWidgets()

    def createWidgets(self):
        self.app.title("PassGrid")
        self.app.geometry("1400x800")

        # set up title frame
        title_frame = tk.Frame(self.app)
        title_frame.pack()

        # title
        title = tk.Label(title_frame, text="Enter Password:")
        title.pack(pady=20)

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
        
    def onClick(self, label):
        self.entered_pass += self.image_map[label]

        # auth password
        if len(self.entered_pass) == 12:

            print(self.entered_pass)
            messagebox.showerror("Error", "Invalid Password")
            self.entered_pass = ""

            # destroy widgets and switch to landing page
            
            #for widget in self.app.winfo_children():
                #widget.destroy()
            #self.deny()
