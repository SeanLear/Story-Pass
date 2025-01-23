import tkinter as tk

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

        # pass until username window is pushed
        pass

    def grid(self):
        # this funciton will start the grid window if the user passes the 
        # username check

        # pass until grid window has been set up
        pass

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()