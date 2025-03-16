"""
Author: Jack Sedillos
Course: CS 433
Term: Winter 25
"""
import tkinter as tk
from tkinter import ttk
import user_database as ud
from tkinter import simpledialog
from tkinter import messagebox
from signUp import SignUp

# When add account button is pressed then databse function is called and
# adds that information to the database, when delete account button is pressed
# then databse function is called deleting account, logout pade send the
# user to the landing page, when a new account is added, this should be 
# displayed on a table of all added accounts

class UserInfo:
    def __init__(self, app, username: str, password: str, landing, grid_pass):
        self.app = app
        self.username = username
        self.password = ""
        self.landing = landing
        self.grid_pass = grid_pass
        if isinstance(password, list):
            for char in password:
                self.password += char  # Convert list to a single string if needed
        self.createWidgets()
    
    def add_info(self):
        user_data = ud.get_user_data(self.username, self.password)

        # Prompt for user input
        account_name = simpledialog.askstring("New Account", "Enter Account Name:")
        if not account_name:
            messagebox.showerror("Error", "Invalid Account Name")
            return

        account_username = simpledialog.askstring("New Account", "Enter Account Username:")
        if not account_username:
            messagebox.showerror("Error", "Invalid Account Username")
            return

        account_password = simpledialog.askstring("New Account", "Enter Account Password:")
        if not account_password:
            messagebox.showerror("Error", "Invalid Account Password")
            return

        if ud.add_user_data(self.username, self.password, account_name, account_username, account_password) == -1:
            messagebox.showerror("Error", "Account already exists in database")
            return

        # Insert into the Treeview UI
        self.tree.insert('', tk.END, values=(account_name, account_username, account_password))

        messagebox.showinfo("Success", "Account added successfully!")


    def del_info(self):
        user_data = ud.get_user_data(self.username, self.password)

        # Prompt user for input
        user_input = simpledialog.askstring("Input", "Account for deletion:")

        # Check if user provided input
        if user_input is None:
            messagebox.showinfo("Error", "Invalid input")
            return
        
        if ud.delete_user_data(self.username, self.password, user_input) == -1:
            messagebox.showinfo("Error", "Account doesn't exist")
            return

        # Delete from TreeView
        for item in self.tree.get_children():
            if self.tree.item(item, "values")[0] == user_input:
                self.tree.delete(item)
                break

        messagebox.showinfo("Success", f"{user_input} deleted successfully!")
    

    def leave_page(self):
        # return to landing page
        for widget in self.app.winfo_children():
            widget.destroy()
        #self.back(self.app, self.grid, SignUp)
        self.landing(self.app, self.grid_pass, SignUp)
        

    def createWidgets(self):
        # Create a frame for buttons
        button_frame = tk.Frame(self.app)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Buttons
        self.add_button = tk.Button(button_frame, text="Add Account", width=15, command=self.add_info)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = tk.Button(button_frame, text="Delete Account", width=15, command=self.del_info)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.logout_button = tk.Button(button_frame, text="Logout", width=15, command=self.leave_page)
        self.logout_button.pack(side=tk.RIGHT, padx=5)
        
        # Create a treeview for the table
        columns = ("Account", "Username", "Password")
        self.tree = ttk.Treeview(self.app, columns=columns, show='headings')

        # Define column headings and set column properties
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, width=200, anchor=tk.W)

        user_data = ud.get_user_data(self.username, self.password)
        for row in user_data:
            self.tree.insert('', tk.END, values=row)

        self.tree.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        
# Run the application
#if __name__ == "__main__":
 #   root = tk.Tk()
    #UserInfo(root)
  #  root.mainloop()
