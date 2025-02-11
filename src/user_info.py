import tkinter as tk
from tkinter import ttk

class UserInfo:
    def __init__(self, app):
        self.app = app
        self.app.title("User Database")
        self.app.geometry("1400x800")
        
        # Create a frame for buttons
        button_frame = tk.Frame(self.app)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Buttons
        self.add_button = tk.Button(button_frame, text="Add Account", width=15)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = tk.Button(button_frame, text="Delete Account", width=15)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.logout_button = tk.Button(button_frame, text="Logout", width=15, command=self.app.quit)
        self.logout_button.pack(side=tk.RIGHT, padx=5)
        
        # Create a treeview for the table
        columns = ("Account", "Username", "Password")
        self.tree = ttk.Treeview(self.app, columns=columns, show='headings')
        
        # Define column headings
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, width=200, anchor=tk.W)
        
        # Insert sample data
        accounts = [
            ("Checking Account", "JaneDoe", "QrF1@:A:rhyMVs"),
            ("Health Insurance", "JaneDoe", "X8e)S**xe&s)Jb"),
            ("Primary Care", "JaneDoe", "q29+q*H1Wq9aa#"),
            ("Pharmacy", "JaneDoe", "ncVs():!Qd4w&c"),
            ("Retirement Account", "JaneDoe", "&$2Egt9uZaz?Er"),
            ("AARP", "JaneDoe", "rfUD(snzvj#[d3"),
            ("Medicare", "JaneDoe", "c+:a4A8xH:sNx["),
        ]
        
        for acc in accounts:
            self.tree.insert('', tk.END, values=acc)
        
        self.tree.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    UserInfo(root)
    root.mainloop()
