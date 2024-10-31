from tkinter import messagebox
import sqlite3
import tkinter as tk

# Connect to SQLite database
conn = sqlite3.connect('medicspharmacy.db')
cursor = conn.cursor()

# Create the accounts table
cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Function to handle signup
def signup():
    username = emailEntry.get()
    password = passwordEntry.get()

    if username and password:
        try:
            cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Signup successful!")
        except sqlite3.IntegrityError:
            conn.rollback()
            messagebox.showerror("Error", "Username already exists.")
    else:
        messagebox.showerror("Error", "Please fill out all fields.")


# Function to handle login
def login():
    username = emailEntry.get()
    password = passwordEntry.get()

    cursor.execute("SELECT * FROM accounts WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Error", "Invalid username or password.")


# Tkinter setup
root = tk.Tk()
root.title("Point of Sale")
root.geometry('500x250')
root.resizable(False, False)
#root.iconbitmap("icon.ico")
headingLabel= tk.Label(root,text="Login to Proceed",font=('times new roman',30,'bold'),background='gray20',foreground='gold',bd=12,relief=tk.GROOVE)
headingLabel.pack(fill=tk.X,pady=5)

registrationPanel = tk.Frame(root,background='gray20')
registrationPanel.pack(fill= tk.X,pady=5)

emailLabel=tk.Label(registrationPanel,text='Email',font=('times new roman',12,'bold'),background='gray20',foreground='white')
emailLabel.grid(row=0,column=0,padx=20)

emailEntry=tk.Entry(registrationPanel,font=('arial',15),bd=7,width=18)
emailEntry.grid(row=0,column=1,padx=8,pady=10)

passwordLabel=tk.Label(registrationPanel,text='Password',font=('times new roman',12,'bold'),background='gray20',foreground='white')
passwordLabel.grid(row=1,column=0,padx=20)

passwordEntry=tk.Entry(registrationPanel,font=('arial',15),bd=7,width=18)
passwordEntry.grid(row=1,column=1,padx=8)

# Label(root, text="Username").grid(row=0, column=0)
# Label(root, text="Password").grid(row=1, column=0)

# entry_username = Entry(root)
# entry_password = Entry(root, show="*")
#
# entry_username.grid(row=0, column=1)
# entry_password.grid(row=1, column=1)
#
tk.Button(registrationPanel, text="Signup",font=('times new roman',15), command=signup).grid(row=2, column=0,pady=10,columnspan=2)
tk.Button(registrationPanel, text="Login",font=('times new roman',15), command=login).grid(row=2, column=2,pady=10,columnspan=2)

root.mainloop()

# Close the database connection when done
cursor.close()
conn.close()