from tkinter import *
from tkinter import messagebox
import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Mansoor@9008",
    host="localhost",
    port="5432"
)
cur = conn.cursor()


# Function to handle signup
def signup():
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Signup successful!")
        except psycopg2.IntegrityError:
            conn.rollback()
            messagebox.showerror("Error", "Username already exists.")
    else:
        messagebox.showerror("Error", "Please fill out all fields.")


# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()

    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()

    if user:
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Error", "Invalid username or password.")


# Tkinter setup
root = Tk()
root.title("Point of Sale")
root.geometry('500x500')
#root.iconbitmap("icon.ico")
headingLabel= Label(root,text="Login to Proceed",font=('times new roman',30,'bold'),background='gray20',foreground='gold',bd=12,relief=GROOVE)
headingLabel.pack(fill=X,pady=5)

registrationPanel = Frame(root,background='gray20')
registrationPanel.pack(fill= X,pady=5)

emailLabel=Label(registrationPanel,text='Email',font=('times new roman',15,'bold'),background='gray20',foreground='white')
emailLabel.grid(row=0,column=0,padx=20)

emailEntry=Entry(registrationPanel,font=('arial',15),bd=7,width=18)
emailEntry.grid(row=0,column=1,padx=8)

passwordLabel=Label(registrationPanel,text='Password',font=('times new roman',15,'bold'),background='gray20',foreground='white')
passwordLabel.grid(row=1,column=0,padx=20)

passwordEntry=Entry(registrationPanel,font=('arial',15),bd=7,width=18)
passwordEntry.grid(row=1,column=1,padx=8)

# Label(root, text="Username").grid(row=0, column=0)
# Label(root, text="Password").grid(row=1, column=0)

# entry_username = Entry(root)
# entry_password = Entry(root, show="*")
#
# entry_username.grid(row=0, column=1)
# entry_password.grid(row=1, column=1)
#
# Button(root, text="Signup", command=signup).grid(row=2, column=0)
# Button(root, text="Login", command=login).grid(row=2, column=1)

root.mainloop()

# Close the database connection when done
cur.close()
conn.close()
