import tkinter as tk
from PIL import Image, ImageTk
import random
from tkinter import messagebox
import platform
from landingPage import LandingPage
from authentication_database import create_account

class SignUp:
    def __init__(self, app, back, grid):
        self.app = app
        self.back = back
        self.grid = grid
        self.feedback = tk.StringVar()
        self.bttn_counter = 6
        self.feedback.set("Remaining Choices: " + str(self.bttn_counter))

        #self.curr_pass = tk.StringVar()
        #self.curr_pas.set("")

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
        #self.fade_image_refs = []

        # store image dictions for easy swap
        self.normal_images = {}
        self.faded_images = {}

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

        # set pass check
        self.second_pass = []

        # store button reference for disable
        self.buttons = {}

        # store disabled buttons for reset
        self.disabled = []

        # second attempt flag
        self.check = False

        # complete flag
        self.complete = False

        # set up window
        self.createWidgets()

    def update_scroll_region(self, event, canvas):
        #canvas.configure(scrollregion=canvas.bbox("all"))
        pass


    def createWidgets(self):
        self.app.title("Story-Pass Sign Up")
        self.app.geometry("950x900")

        # create canvas for scroll
        #canvas = tk.Canvas(self.app)
        #canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand=True)

        # scrollbar
        #scrollbar = tk.Scrollbar(self.app, orient=tk.VERTICAL, command=canvas.yview)
        #scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        #canvas.configure(yscrollcommand=scrollbar.set)

        # create scroll frame
        #scroll_frame = tk.Frame(canvas)
        #canvas.create_window((0, 0), window = scroll_frame, width = 1150, height = 1100)

        #scroll_frame.bind("<Configure>", lambda event: self.update_scroll_region(event, canvas))

        # create frame for username and title
        username_frame = tk.Frame(self.app)
        username_frame.pack()

        title = tk.Label(username_frame, text="Create Account", font = ("TkinterDefaultFont", 30, "bold"))
        title.pack(pady=(0, 10))

        username_title = tk.Label(username_frame, text="Create Username:", font = ("TkinterDefaultFont", 18))
        username_title.pack(pady=(10, 5))

        self.username = tk.Entry(username_frame, width = 50, bd = 2, relief = "solid")
        self.username.pack(pady=(5, 0))

        # bind username to typing for valid submit checking
       # self.username.bind("<KeyRelease>", lambda event: self.check_inputs())

        pass_title = tk.Label(username_frame, font = ("TkinterDefaultFont", 20), text="Create Password:")
        pass_title.pack(pady=(35, 5))

        pass_counter = tk.Label(username_frame, font = ("TkinterDefaultFont", 14), textvariable=self.feedback)
        pass_counter.pack(pady=5)


        # create Password Frame
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
            img = img.resize((75, 75))
            photo = ImageTk.PhotoImage(img)

            # store photo
            self.normal_images[click] = photo

            # prevent deletion
            self.image_refs.append(photo)

            # create faded image for disable
            faded_img = img.convert("RGBA")
            for x in range(faded_img.width):
                for y in range(faded_img.height):
                    r, g, b, a = faded_img.getpixel((x, y))
                    faded_img.putpixel((x, y), (r, g, b, int(a * 0.3)))

            faded_photo = ImageTk.PhotoImage(faded_img)
            self.faded_images[click] = faded_photo

            self.image_refs.append(faded_photo)


            # create button
            btn = tk.Button(grid_frame, image=photo, command=lambda label=click: self.onClick(label))
            btn.grid(row=row, column=col, padx=10, pady=10)

            self.buttons[click] = btn

        # create frame for buttons
        bttn_frame = tk.Frame(self.app)
        bttn_frame.pack()

        # create cancel button
        cancel_bttn = tk.Button(bttn_frame, text = "Cancel", font = ("TkDefaultFont", 18), command = lambda: self.leave())
        cancel_bttn.pack(side=tk.LEFT, padx = 10, pady = 20)
 
        # create reset button
        reset_bttn = tk.Button(bttn_frame, text = "Reset Attempt", font = ("TkDefaultFont", 18), command = lambda: self.reset())
        reset_bttn.pack(side=tk.LEFT, padx = 10, pady = 20)

        # create submit button
        self.submit_bttn = tk.Button(bttn_frame, text = "Submit Account", font = ("TkDefaultFont", 18), command = lambda: self.submit())
        self.submit_bttn.pack(side=tk.LEFT, padx = 10, pady = 20)

        # set up scroll
        #canvas.config(scrollregion=canvas.bbox("all"))

        # bind mousewheel
        #self.bind_mousewheel

    def onClick(self, label):
        if not self.check:
            self.entered_pass.append(self.image_map[label])
        else:
            self.second_pass.append(self.image_map[label])

        self.bttn_counter -= 1
        self.feedback.set("Remaining Choices: " + str(self.bttn_counter))
        # disable button
        self.buttons[label].config(image=self.faded_images[label], state=tk.DISABLED)
        self.disabled.append(label)

        # auth password
        if len(self.entered_pass) == 6 and len(self.second_pass) == 0:
                print(self.entered_pass)
                messagebox.showinfo("Success", "Please Re-enter password")
                #self.entered_pass = []
                self.bttn_counter = 6
                self.feedback.set("Remaining Choices: " + str(self.bttn_counter))
                # show entered pass and second pass in some way 

                # re enable buttons
                for name in self.disabled:
                    self.buttons[name].config(image=self.normal_images[name], state=tk.NORMAL)


                # set second attempt flag
                self.check = True
        elif len(self.second_pass) == 6:
            if self.second_pass == self.entered_pass:
                self.complete = True
                messagebox.showinfo("Success", "Password Set, Submit to Create Account")

                # disable all buttons
                for name, bttn in self.buttons.items():
                        bttn.config(image=self.faded_images[name], state=tk.DISABLED)
                
                # set done flag
                self.check_inputs()

            else:
                messagebox.showerror("Error", "Passwords do not match, Try Again")
                self.entered_pass = []
                self.second_pass = []
                self.bttn_counter = 6
                self.check = False

                self.feedback.set("Remaining Choices: " + str(self.bttn_counter))
                for name in self.disabled:
                    self.buttons[name].config(image=self.normal_images[name], state=tk.NORMAL)


    def reset(self):
        # this function resets the entered password for reset attempt button

        if not self.complete:

            print("reseting entred password")
            self.entered_pass = []
            self.bttn_counter = 6
            self.feedback.set("Remaining Choices: " + str(self.bttn_counter))

            # reset disabled buttons
            for name in self.disabled:
                    self.buttons[name].config(image=self.normal_images[name], state=tk.NORMAL)


    def submit(self):
        # this function will submit the account creation to database and bring user
        # back to the landing page
        if self.username.get().strip() and self.complete:
            if (create_account(self.username.get(), self.entered_pass[0], self.entered_pass[1], self.entered_pass[2], self.entered_pass[3], self.entered_pass[4], self.entered_pass[5]) == 1):
                messagebox.showinfo("Success", "Account Creation Successful, please Log In")
            else:
                messagebox.showerror("Error", "Account Creation Failed, Username Already Taken")
            
            for widget in self.app.winfo_children():
                widget.destroy()
            self.back(self.app, self.grid, SignUp)
        else:
            messagebox.showerror("Error", "Please enter Username and Password before Submitting")

    def leave(self):
        # this function returns the user to the landing page
        for widget in self.app.winfo_children():
            widget.destroy()
        self.back(self.app, self.grid, SignUp)
            

    def bind_mousewheel(self):
        # find out system and bind mousewheel accordingly
        system = platform.system()

        if system == "Darwin":
            self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_mac)
        elif system == "Windows":
            self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_windows)
        elif system == "Linux":
            self.canvas.bind_all("<Button-4>", self.on_mousewheel_linux_up)
            self.canvas.bind_all("<Button-5>", self.on_mousewheel_linux_down)
        else:
            print("Cant bind mousewheel")

    def on_mousewheel_mac(self, event):
        # scroll for macOS
        self.canvas.yview_scroll(int(-1 * event.delta), "units")

    def check_inputs(self):
        pass
        # allow for submit if user enters required info
        #if self.username.get().strip() and self.complete:
            #self.submit_bttn.config(state=tk.NORMAL)
        #else:
            #self.submit_bttn.config(state=tk.DISABLED)

        