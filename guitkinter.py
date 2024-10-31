
# from tkinter import *
# from tkinter import messagebox,ttk
# import tempfile,os,smtplib,subprocess,time,sqlite3
# import tkinter as tk
# # from escpos.printer import Usb




import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import tempfile, os, smtplib, subprocess, time, sqlite3

#Fuctionality part\

def connectandcreatetable():
# Connect to SQLite database
    conn = sqlite3.connect('medicspharmacy.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_name TEXT NOT NULL,
        expiry DATE NOT NULL,
        batch_no TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    );
    ''')
    conn.close()
connectandcreatetable()



def open_inventory_window():
    inventory_window = tk.Toplevel()
    inventory_window.title("Inventory Management")
    inventory_window.geometry("600x450")

    headingLabel = tk.Label(inventory_window, text="Inventory Management", font=('times new roman', 30, 'bold'), background='gray20', foreground='gold', bd=12, relief=tk.GROOVE)
    headingLabel.pack(fill=tk.X, pady=5)

    # Project Details
    treeviewFrame = tk.Frame(inventory_window, background='gray20', bd=8, relief=tk.GROOVE)
    treeviewFrame.pack(fill=tk.X, pady=5)

    columns = ('#1', '#2', '#3', '#4', '#5', '#6')
    tree = ttk.Treeview(treeviewFrame, columns=columns, show='headings')
    tree.heading('#1', text='Sr')
    tree.heading('#2', text='Medicine Name')
    tree.heading('#3', text='Expiry')
    tree.heading('#4', text='Batch Number')
    tree.heading('#5', text='Quantity')
    tree.heading('#6', text='Price')

    # Setting column widths
    tree.column('#1', width=30)
    tree.column('#2', width=150)
    tree.column('#3', width=100)
    tree.column('#4', width=100)
    tree.column('#5', width=70)
    tree.column('#6', width=70)

    # Adding Vertical Scrollbar
    vsb = ttk.Scrollbar(treeviewFrame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    # Adding Horizontal Scrollbar
    hsb = ttk.Scrollbar(treeviewFrame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x')
    tree.configure(xscrollcommand=hsb.set)

    tree.pack(fill='both', expand=True)

    def clear_treeview():
        for item in tree.get_children():
            tree.delete(item)

    # Reading Data from DB and inserting into Treeview
    def readintotreeview():
        conn = sqlite3.connect('medicspharmacy.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory;")
        completeRow = cursor.fetchall()

        conn.close()

        clear_treeview()
        # projectsList.delete(0, tk.END)
        for record in completeRow:
            # projectsList.insert(tk.END, f'{record[0]}')
            tree.insert('', 'end', values=(record[0], record[1], record[2], record[3], record[4], record[5]))
    readintotreeview()
     
           

    # sample_data = [
    #     (1, "Paracetamol", "2025-12-01", "B12345", 50, 10.0),
    #     (2, "Ibuprofen", "2024-10-01", "B23456", 30, 12.5)
    # ]
    # for item in sample_data:
    #     tree.insert('', 'end', values=item)
        

    def open_new_entry_window():
        new_entry_window = tk.Toplevel(inventory_window)
        new_entry_window.title("New Entry")
        new_entry_window.geometry("550x450")

        headingLabel = tk.Label(new_entry_window, text="New Entry", font=('times new roman', 30, 'bold'), background='gray20', foreground='gold', bd=12, relief=tk.GROOVE)
        headingLabel.pack(fill=tk.X, pady=5)

        # Create form labels and entries
        newentryFrame = tk.Frame(new_entry_window, background='gray20', bd=8, relief=tk.GROOVE)
        newentryFrame.pack(fill=tk.X, pady=5)
        
        tk.Label(newentryFrame, text="Medicine Name",font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=0, column=0, padx=10, pady=5)
        medicine_name_entry = tk.Entry(newentryFrame,font=('arial',15),bd=7,width=18)
        medicine_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(newentryFrame, text="Expiry Date (YYYY-MM-DD)",font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=1, column=0, padx=10, pady=5)
        expiry_entry = tk.Entry(newentryFrame,font=('arial',15),bd=7,width=18)
        expiry_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(newentryFrame, text="Batch No",font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=2, column=0, padx=10, pady=5)
        batch_no_entry = tk.Entry(newentryFrame,font=('arial',15),bd=7,width=18)
        batch_no_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(newentryFrame, text="Quantity",font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=3, column=0, padx=10, pady=5)
        quantity_entry = tk.Entry(newentryFrame,font=('arial',15),bd=7,width=18)
        quantity_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(newentryFrame, text="Price",font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=4, column=0, padx=10, pady=5)
        price_entry = tk.Entry(newentryFrame,font=('arial',15),bd=7,width=18)
        price_entry.grid(row=4, column=1, padx=10, pady=5)

        # Function to insert data into database
        def add_entry():
            conn = sqlite3.connect('medicspharmacy.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO inventory (medicine_name, expiry, batch_no, quantity, price)
                VALUES (?, ?, ?, ?, ?)
            ''', (medicine_name_entry.get(), expiry_entry.get(), batch_no_entry.get(), quantity_entry.get(), price_entry.get()))
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            # Insert new data into Treeview 
            # tree.insert('', 'end', values=(new_id, medicine_name_entry.get(), expiry_entry.get(), batch_no_entry.get(), quantity_entry.get(), price_entry.get()))
            readintotreeview() 
            readitems()
            new_entry_window.destroy()

        # Add submit button
        submit_button = tk.Button(newentryFrame, text="Submit", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10,command=add_entry)
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Add edit, delete, update buttons
    def edit_item():
        pass  # Add your logic here

    # def delete_item():
    #     pass  # Add your logic here
    def delete_item():
        selected_item = tree.selection()[0]  # Get selected item
        item_values = tree.item(selected_item, 'values')  # Get values of the selected item
        item_id = item_values[0]  # Assuming 'id' is the first value in the tuple

        conn = sqlite3.connect('medicspharmacy.db')
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM inventory WHERE id = ?
        ''', (item_id,))
        conn.commit()
        conn.close()

        # tree.delete(selected_item)  # Remove the item from Treeview
        readintotreeview()
        readitems()


    # def update_item():
    #     pass  # Add your logic here

    def update_item():
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, 'values')

        update_window = tk.Toplevel(inventory_window)
        update_window.title("Update Entry")
        update_window.geometry("450x420")

        headingLabel = tk.Label(update_window, text="Edit", font=('times new roman', 30, 'bold'), background='gray20', foreground='gold', bd=12, relief=tk.GROOVE)
        headingLabel.pack(fill=tk.X, pady=5)

        # Create form labels and entries
        editentryFrame = tk.Frame(update_window, background='gray20', bd=8, relief=tk.GROOVE)
        editentryFrame.pack(fill=tk.X, pady=5)

        tk.Label(editentryFrame, text="Medicine Name", font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=0, column=0, padx=10, pady=5)
        med_name_entry = tk.Entry(editentryFrame,font=('arial',15),bd=7,width=18)
        med_name_entry.grid(row=0, column=1, padx=10, pady=5)
        med_name_entry.insert(0, values[1])

        tk.Label(editentryFrame, text="Expiry", font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=1, column=0, padx=10, pady=5)
        expiry_entry = tk.Entry(editentryFrame,font=('arial',15),bd=7,width=18)
        expiry_entry.grid(row=1, column=1, padx=10, pady=5)
        expiry_entry.insert(0, values[2])

        tk.Label(editentryFrame, text="Batch No", font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=2, column=0, padx=10, pady=5)
        batch_no_entry = tk.Entry(editentryFrame,font=('arial',15),bd=7,width=18)
        batch_no_entry.grid(row=2, column=1, padx=10, pady=5)
        batch_no_entry.insert(0, values[3])

        tk.Label(editentryFrame, text="Quantity", font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=3, column=0, padx=10, pady=5)
        quantity_entry = tk.Entry(editentryFrame,font=('arial',15),bd=7,width=18)
        quantity_entry.grid(row=3, column=1, padx=10, pady=5)
        quantity_entry.insert(0, values[4])

        tk.Label(editentryFrame, text="Price", font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=4, column=0, padx=10, pady=5)
        price_entry = tk.Entry(editentryFrame,font=('arial',15),bd=7,width=18)
        price_entry.grid(row=4, column=1, padx=10, pady=5)
        price_entry.insert(0, values[5])

        def save_changes():
            conn = sqlite3.connect('medicspharmacy.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE inventory
                SET medicine_name=?, expiry=?, batch_no=?, quantity=?, price=?
                WHERE id=?
            ''', (med_name_entry.get(), expiry_entry.get(), batch_no_entry.get(), quantity_entry.get(), price_entry.get(), values[0]))
            conn.commit()
            conn.close()

            # Update Treeview
            # tree.item(selected_item, values=(values[0], med_name_entry.get(), expiry_entry.get(), batch_no_entry.get(), quantity_entry.get(), price_entry.get()))
            readintotreeview()
            readitems()
            update_window.destroy()

        tk.Button(editentryFrame, text="Save", font=('arial', 12, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10,command=save_changes).grid(row=5, column=0, columnspan=2, pady=10)






    inventorybuttonFrame = tk.Frame(inventory_window, background='gray20', bd=8, relief=tk.GROOVE)
    inventorybuttonFrame.pack(fill=tk.X, pady=5)

    # Buttons
    add_button = tk.Button(inventorybuttonFrame, text="New Entry", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10, command=open_new_entry_window)
    add_button.pack(side='left')

    edit_button = tk.Button(inventorybuttonFrame, text="Edit", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10, command=edit_item)
    edit_button.pack(side='left')

    delete_button = tk.Button(inventorybuttonFrame, text="Delete", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10, command=delete_item)
    delete_button.pack(side='left')

    update_button = tk.Button(inventorybuttonFrame, text="Update", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10, command=update_item)
    update_button.pack(side='left')

    print_button = tk.Button(inventorybuttonFrame, text="Print", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10, command=update_item)
    print_button.pack(side='left')




# def open_inventory_window():
    
#     inventory_window = Toplevel()
#     inventory_window.title("Inventory Management")
#     inventory_window.geometry("600x450")

#     headingLabel= Label(inventory_window,text="Inventory Managment",font=('times new roman',30,'bold'),background='gray20',foreground='gold',bd=12,relief=GROOVE)
#     headingLabel.pack(fill=X,pady=5)

#     #Project Details
#     treeviewFrame = Frame(inventory_window,background='gray20',bd=8,relief=GROOVE)
#     treeviewFrame.pack(fill= X,pady=5)



#     columns = ('#1', '#2', '#3', '#4', '#5', '#6')
#     tree = ttk.Treeview(treeviewFrame, columns=columns, show='headings')
#     tree.heading('#1', text='Sr')
#     tree.heading('#2', text='Medicine Name')
#     tree.heading('#3', text='Expiry')
#     tree.heading('#4', text='Batch Number')
#     tree.heading('#5', text='Quantity')
#     tree.heading('#6', text='Price')

#     # Setting column widths 
#     tree.column('#1', width=30) 
#     tree.column('#2', width=150) 
#     tree.column('#3', width=100) 
#     tree.column('#4', width=100) 
#     tree.column('#5', width=70) 
#     tree.column('#6', width=70)

    


#     # Adding Vertical Scrollbar 
#     vsb = ttk.Scrollbar(treeviewFrame, orient="vertical", command=tree.yview) 
#     vsb.pack(side='right', fill='y') 
#     tree.configure(yscrollcommand=vsb.set) 
#     # Adding Horizontal Scrollbar 
#     hsb = ttk.Scrollbar(treeviewFrame, orient="horizontal", command=tree.xview) 
#     hsb.pack(side='bottom', fill='x') 
#     tree.configure(xscrollcommand=hsb.set)



#     tree.pack(fill='both', expand=True)

#     # Add sample data
#     sample_data = [(1, "Paracetamol", "2025-12-01", "B12345", 50, 10.0),
#                    (2, "Ibuprofen", "2024-10-01", "B23456", 30, 12.5)]
#     for item in sample_data:
#         tree.insert('', 'end', values=item)

#     def open_new_entry_window(): 
#         new_entry_window = Toplevel(inventory_window) 
#         new_entry_window.title("New Entry") 
#         new_entry_window.geometry("400x300") 

#         # Create form labels and entries 
#         Label(new_entry_window, text="Medicine Name").grid(row=0, column=0, padx=10, pady=5) 
#         medicine_name_entry = Entry(new_entry_window) 
#         medicine_name_entry.grid(row=0, column=1, padx=10, pady=5) 

#         Label(new_entry_window, text="Expiry Date (YYYY-MM-DD)").grid(row=1, column=0, padx=10, pady=5) 
#         expiry_entry = Entry(new_entry_window) 
#         expiry_entry.grid(row=1, column=1, padx=10, pady=5) 

#         Label(new_entry_window, text="Batch No").grid(row=2, column=0, padx=10, pady=5) 
#         batch_no_entry =Entry(new_entry_window) 
#         batch_no_entry.grid(row=2, column=1, padx=10, pady=5) 

#         Label(new_entry_window, text="Quantity").grid(row=3, column=0, padx=10, pady=5) 
#         quantity_entry = Entry(new_entry_window) 
#         quantity_entry.grid(row=3, column=1, padx=10, pady=5) 

#         Label(new_entry_window, text="Price").grid(row=4, column=0, padx=10, pady=5) 
#         price_entry =Entry(new_entry_window) 
#         price_entry.grid(row=4, column=1, padx=10, pady=5)

#          # Function to insert data into database 
#         def add_entry():
#             conn = sqlite3.connect('pharmacy.db') 
#             cursor = conn.cursor() 
#             cursor.execute(''' 
#             INSERT INTO inventory (medicine_name, expiry, batch_no, quantity, price)
#             VALUES (?, ?, ?, ?, ?) 
#             ''', (medicine_name_entry.get(), expiry_entry.get(), batch_no_entry.get(), quantity_entry.get(), price_entry.get())) 
#         conn.commit() 
#         conn.close() 
#         new_entry_window.destroy() 
        
#         # Add submit button 
#         submit_button = tk.Button(new_entry_window, text="Submit", command=add_entry) 
#         submit_button.grid(row=5, column=0, columnspan=2, pady=10)

#     # Add edit, delete, update buttons
#     def edit_item():
#         pass  # Add your logic here

#     def delete_item():
#         pass  # Add your logic here

#     def update_item():
#         pass  # Add your logic here

#     inventorybuttonFrame = Frame(inventory_window,background='gray20',bd=8,relief=GROOVE)
#     inventorybuttonFrame.pack(fill= X,pady=5)

#     # Buttons
#     add_button = Button(inventorybuttonFrame, text="New Entry",font=('arial',16,'bold'),background="gray20", 
#                          foreground='white',bd=5,width=8,pady=10,command=open_new_entry_window)
#     add_button.pack(side='left')

#     edit_button = Button(inventorybuttonFrame, text="Edit",font=('arial',16,'bold'),background="gray20", 
#                          foreground='white',bd=5,width=8,pady=10,command=edit_item)
#     edit_button.pack(side='left')

#     delete_button = Button(inventorybuttonFrame, text="Delete", font=('arial',16,'bold'),background="gray20", 
#                          foreground='white',bd=5,width=8,pady=10,command=delete_item)
#     delete_button.pack(side='left')

#     update_button = Button(inventorybuttonFrame, text="Update", font=('arial',16,'bold'),background="gray20", 
#                          foreground='white',bd=5,width=8,pady=10,command=update_item)
#     update_button.pack(side='left')

#     print_button = Button(inventorybuttonFrame, text="Print", font=('arial',16,'bold'),background="gray20", 
#                          foreground='white',bd=5,width=8,pady=10,command=update_item)
#     print_button.pack(side='left')





# cursor.execute('''
# CREATE TABLE IF NOT EXISTS customers (
#     id INTEGER PRIMARY KEY,
#     name TEXT NOT NULL,
#     email TEXT
# )
# ''')

# Commit changes and close connection
# conn.commit()
# conn.close()

# print("Database and tables created successfully!")



# def on_closing():
#     stop_postgresql()
#     root.destroy()


# # Function for starting postgresql 
# def start_postgresql():
#     subprocess.call(['start_postgresql.bat'])
#     # Give PostgreSQL a moment to start up
#     time.sleep(5)

# # Function for stoping postgresql
# def stop_postgresql():
#     subprocess.call(['stop_postgresql.bat'])


# def print_receipt():

#     # Adjust the USB parameters according to your printer's specifications
#     p = Usb(0x04b8, 0x0202, 0)
#     p.text("Hello, World!\n")
#     p.cut()



# Function to update Listbox based on search
def update_listbox(event):
    search_term = search_entry.get()
    results = fetch_data(search_term)
    projectsList.delete(0, tk.END)
    for result in results:
        projectsList.insert(tk.END, result[0])

# Function to search and update Listbox
def fetch_data(search_term):

    conn = sqlite3.connect('medicspharmacy.db')
    cursor = conn.cursor()

    cursor.execute("SELECT medicine_name FROM inventory WHERE medicine_name LIKE ?", ('%' + search_term + '%',))

    results = cursor.fetchall()

    conn.close()

    return results

def send_email():
    def send_gmail():
        try:
            ob = smtplib.SMTP('smtp.gmail.com', 587)
            ob.starttls()
            ob.login(senderEntry.get(), passwordEntry.get())
            message = emailtextArea.get('1.0', tk.END)
            receiverAdress = receiverEntry.get()
            ob.sendmail(senderEntry.get(), receiverAdress, message)
            ob.quit()
            messagebox.showinfo('Successful', 'Email sent!',parent = root1)
            root1.destroy()
        except:
            messagebox.showinfo('Failed', 'Please try again!',parent =root1)



    if textArea.get(1.0,tk.END) == '\n':
        messagebox.showerror('Error','Nothing in Email')
    else:
        root1 = tk.Toplevel()
        root1.grab_set()
        root1.title("Send Email")
        root1.resizable(False, False)
        root1.configure(bg="grey20")

        senderFrame = tk.LabelFrame(root1,text = 'SENDER',font = ('arial',16,'bold'),background='grey20',foreground ='white')
        senderFrame.grid(row = 0, column = 0,padx = 40,pady = 20)

        senderLabel = tk.Label(senderFrame, text = "Sender's Email ID", font = ('arial',14,'bold'),background='grey20',foreground ='white')
        senderLabel.grid(row = 0, column = 0,padx = 10 ,pady = 8)
        senderEntry = tk.Entry(senderFrame,font = ('arial',14,'bold'),bd = 2,width = 23, relief = tk.RIDGE)
        senderEntry.grid(row = 0, column = 1,padx = 10 ,pady = 8)

        passwordLabel = tk.Label(senderFrame, text="Password", font=('arial', 14, 'bold'), background='grey20',
                            foreground='white')
        passwordLabel.grid(row=1, column=0, padx=10, pady=8)
        passwordEntry = tk.Entry(senderFrame, font=('arial', 14, 'bold'), bd=2, width=23, relief=tk.RIDGE,show='*')
        passwordEntry.grid(row=1, column=1, padx=10, pady=8)

        #Receiver Email Entry
        receiverFrame = tk.LabelFrame(root1, text='RECIPIENT', font=('arial', 16, 'bold'), background='grey20', foreground='white')
        receiverFrame.grid(row=1, column=0, padx=40, pady=20)

        receiverLabel = tk.Label(receiverFrame, text="Email Address", font=('arial', 14, 'bold'), background='grey20',
                              foreground='white')
        receiverLabel.grid(row=0, column=0, padx=10, pady=8)
        receiverEntry = tk.Entry(receiverFrame, font=('arial', 14, 'bold'), bd=2, width=23, relief=tk.RIDGE)
        receiverEntry.grid(row=0, column=1, padx=10, pady=8)

        #Message
        messageLabel = tk.Label(receiverFrame, text="Message", font=('arial', 14, 'bold'), background='grey20',
                              foreground='white')
        messageLabel.grid(row=1, column=0, padx=10, pady=8)

        emailtextArea = tk.Text(receiverFrame, font=('arial', 14, 'bold'), bd = 2, relief=tk.SUNKEN,width=42,height=11)
        emailtextArea.grid(row=2, column=0, padx=10, pady=8,columnspan =2)
        emailtextArea.delete('1.0',tk.END)
        emailtextArea.insert(tk.END,textArea.get('1.0', tk.END).replace('=','').replace('-','').replace('\t\t\t ','\t\t'))

        sendButton = tk.Button(root1,text='SEND',font=('arial', 16, 'bold'),width=15,command=send_gmail)
        sendButton.grid(row=2, column=0, padx=10, pady=8)


        root1.mainloop()



def print_bill():
    if textArea.get(1.0,tk.END) == '\n':
        messagebox.showerror('Error','Nothing to print')
    else:
        file= tempfile.mktemp('.txt')
        open(file, 'w').write(textArea.get(1.0,tk.END))
        os.startfile(file,'print')


def clearAll():
    global totalPrice
    totalPrice  = 0
    nameEntry.delete(0,tk.END)
    phoneEntry.delete(0, tk.END)
    billEntry.delete(0, tk.END)
    textArea.delete(1.0, tk.END)

    textArea.insert(1.0, '\t   ***Medical Store***\n\n')
    textArea.insert(tk.END,'\tContact # :0311-5552866\n\tEmail:mansoorpay@gmail.com\n')
    textArea.insert(tk.END,'========================================\n')
    textArea.insert(tk.END,' Item \t     Unit \t  Quantity\t   Total \n')
    textArea.insert(tk.END,' Name \t     Price \t\t         Price \n')
    textArea.insert(tk.END,'========================================\n')


def total():
    textArea.insert(tk.END, f'\n\nTotal Bill \t\t\t\t{totalPrice} Rs\n')
    textArea.insert(tk.END, '----------------------------------------\n\n')
    textArea.insert(tk.END, 'Developed by Django Softwate PVT\n')
    textArea.insert(tk.END, 'Contact:92-311-5552866  Email:mansoorpay@gmail.com\n')

# # Connecting to DB
# # start_postgresql()
# conn = psycopg2.connect(
#     dbname="postgres",
#     user="postgres",
#     password="Mansoor@9008",
#     host="localhost",
#     port="5432"
#     )
# cursor = conn.cursor()


# def submit():
#     #textArea.insert(0,nameEntry.get())
#     entered_name = nameEntry.get()
#     quantity_Entry = phoneEntry.get()
#     priceEntry = billEntry.get()
#     cursor.execute("INSERT INTO medicine(name, quantity, price) VALUES (?, ?, ?)", (entered_name, quantity_Entry, priceEntry))

#     conn.commit()
#     readitems()

def readitems():
    conn = sqlite3.connect('medicspharmacy.db')
    cursor = conn.cursor()

    cursor.execute("SELECT medicine_name FROM inventory;")
    # tree.insert('', 'end', values=(new_id, medicine_name_entry.get(), expiry_entry.get(), batch_no_entry.get(), quantity_entry.get(), price_entry.get())) 
           
    records = cursor.fetchall()

    conn.close()

    projectsList.delete(0, tk.END)
    for record in records:
        projectsList.insert(tk.END, f'{record[0]}')


def on_select(event):
    global totalPrice
    selectedIndex = projectsList.curselection()

    if selectedIndex:
        item = projectsList.get(selectedIndex)
        query = "SELECT price FROM inventory WHERE medicine_name = ?"

        conn = sqlite3.connect('medicspharmacy.db')
        cursor = conn.cursor()
        cursor.execute(query, (item,))

        priceofitem = cursor.fetchone()[0]

        conn.close()

        itemQuantity = simpledialog.askstring("Input", "Enter Quantity:", initialvalue="1")
        if itemQuantity:
        # Do something with the entered string 
            # print("Entered string:", itemQuantity)
            itemPrice = int(itemQuantity) * int(priceofitem)

        totalPrice = totalPrice + int(itemPrice)
        textArea.insert(tk.END, f' {item}\t\t{priceofitem}\t{itemQuantity}\t{itemPrice}\n')
        # print(f'Selected item is {item}')
    else:
        messagebox.INFO('Not Found','Unknown Error')

totalPrice = 0



# GUI Part
root = tk.Tk()
root.title("POS")


root.geometry('1270x800')
#root.iconbitmap("icon.ico")
headingLabel= tk.Label(root,text="Offline Software Managment",font=('times new roman',30,'bold'),background='gray20',foreground='gold',bd=12,relief=tk.GROOVE)
headingLabel.pack(fill=tk.X,pady=5)


# Customers Details Frame
costumer_details_frame = tk.LabelFrame(root,text="New Entry",font=('times new roman',15,'bold'),foreground='gold',bd=8,relief=tk.GROOVE,background='gray20')
costumer_details_frame.pack(fill=tk.X)

nameLabel=tk.Label(costumer_details_frame,text='Item Name',font=('times new roman',15,'bold'),background='gray20',foreground='white')
nameLabel.grid(row=0,column=0,padx=20)

nameEntry=tk.Entry(costumer_details_frame,font=('arial',15),bd=7,width=18)
nameEntry.grid(row=0,column=1,padx=8)

phoneLabel=tk.Label(costumer_details_frame,text='Quantity',font=('times new roman',15,'bold'),background='gray20',foreground='white')
phoneLabel.grid(row=0,column=2,padx=20,pady=2)

phoneEntry=tk.Entry(costumer_details_frame,font=('arial',15),bd=7,width=18)
phoneEntry.grid(row=0,column=3,padx=8)

billnumberLabel=tk.Label(costumer_details_frame,text='Price',font=('times new roman',15,'bold'),background='gray20',foreground='white')
billnumberLabel.grid(row=0,column=4,padx=20,pady=2)

billEntry=tk.Entry(costumer_details_frame,font=('arial',15),bd=7,width=18)
billEntry.grid(row=0,column=5,padx=8)

submitButton= tk.Button(costumer_details_frame,text="Inventory",font=('arial',12,'bold'),bd=7,width=10,command=open_inventory_window)
submitButton.grid(row=0,column=6,padx=20)

#Project Details
projectPanel = tk.Frame(root,background='gray20')
projectPanel.pack(fill= tk.X,pady=5)


items_details_frame = tk.LabelFrame(projectPanel,text="Items",font=('times new roman',15,'bold'),foreground='gold',bd=8,relief=tk.GROOVE,background='gray20')
items_details_frame.grid(row=0,column=0,padx=50)

#Listbox
search_entry = tk.Entry(items_details_frame,  width=40,font=('arial',15),bd=7)
search_entry.bind("<KeyRelease>", update_listbox)
search_entry.grid(row=0,column=0,padx=5)
projectsList = tk.Listbox(items_details_frame,bd=5,font=('arial',15,),height=15,width=40,relief=tk.GROOVE)
projectsList.bind('<Return>',on_select)
projectsList.grid(row=1,column=0,padx=5)

#Bill Area
billFrame=tk.Frame(projectPanel,bd=8,relief=tk.GROOVE)
billFrame.grid(row=0,column=2,padx=50,pady = 5)
bill_details_frame = tk.Label(billFrame,text="Bill",font=('times new roman',15,'bold'),bd=8,relief=tk.GROOVE)
bill_details_frame.pack(fill=tk.X)
scrollbar=tk.Scrollbar(billFrame,orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
textArea = tk.Text(billFrame,height=25,width=40,yscrollcommand=scrollbar.set)
textArea.pack()
scrollbar.config(command=textArea.yview)
textArea.insert(1.0,'\t   ***Medical Store***\n\n')
textArea.insert(tk.END,'\tContact # :0311-5552866\n\tEmail:mansoorpay@gmail.com\n')
textArea.insert(tk.END,'========================================\n')
textArea.insert(tk.END,' Item \t     Unit \t  Quantity\t   Total \n')
textArea.insert(tk.END,' Name \t     Price \t\t         Price \n')
textArea.insert(tk.END,'========================================\n')
readitems()



#Bill menu frame

billmenuframe = tk.LabelFrame(projectPanel,text="Buttons",font=('times new roman',15,'bold'),foreground='gold',bd=8,relief=tk.GROOVE,background='gray20')
billmenuframe.grid(row=0,column=1,padx=20)

totalbutton=tk.Button(billmenuframe,text="Total",font=('arial',16,'bold'),background="gray20",
                   foreground='white',bd=5,width=8,pady=10,command=total)
totalbutton.grid(row=0,column=0,pady=5,padx=10)

billbutton=tk.Button(billmenuframe,text="Bill",font=('arial',16,'bold'),background="gray20",foreground='white',bd=5,width=8,pady=10)
billbutton.grid(row=1,column=0,pady=5,padx=10)

emailbutton=tk.Button(billmenuframe,text="Email",font=('arial',16,'bold'),background="gray20",
                   foreground='white',bd=5,width=8,pady=10,command=send_email)
emailbutton.grid(row=2,column=0,pady=5,padx=10)

printbutton=tk.Button(billmenuframe,text="Print",font=('arial',16,'bold'),background="gray20",
                   foreground='white',bd=5,width=8,pady=10,command=print_bill)
printbutton.grid(row=3,column=0,pady=5,padx=10)

clearbutton=tk.Button(billmenuframe,text="Clear",font=('arial',16,'bold'),background="gray20",
                   foreground='white',bd=5,width=8,pady=10,command=clearAll)
clearbutton.grid(row=4,column=0,pady=5,padx=10)

# root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
