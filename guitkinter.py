from optparse import Values
from tkinter import *
from tkinter import messagebox
import psycopg2,tempfile,os,smtplib

#Fuctionality part\

# Function to update Listbox based on search
def update_listbox(event):
    search_term = search_entry.get()
    results = fetch_data(search_term)
    projectsList.delete(0, END)
    for result in results:
        projectsList.insert(END, result[0])

# Function to search and update Listbox
def fetch_data(search_term):

    cursor.execute("SELECT name FROM Projects WHERE name LIKE %s", ('%' + search_term + '%',))
    results = cursor.fetchall()
    return results

def send_email():
    def send_gmail():
        try:
            ob = smtplib.SMTP('smtp.gmail.com', 587)
            ob.starttls()
            ob.login(senderEntry.get(), passwordEntry.get())
            message = emailtextArea.get('1.0', END)
            receiverAdress = receiverEntry.get()
            ob.sendmail(senderEntry.get(), receiverAdress, message)
            ob.quit()
            messagebox.showinfo('Successful', 'Email sent!',parent = root1)
            root1.destroy()
        except:
            messagebox.showinfo('Failed', 'Please try again!',parent =root1)



    if textArea.get(1.0,END) == '\n':
        messagebox.showerror('Error','Nothing in Email')
    else:
        root1 = Toplevel()
        root1.grab_set()
        root1.title("Send Email")
        root1.resizable(False, False)
        root1.configure(bg="grey20")

        senderFrame = LabelFrame(root1,text = 'SENDER',font = ('arial',16,'bold'),background='grey20',foreground ='white')
        senderFrame.grid(row = 0, column = 0,padx = 40,pady = 20)

        senderLabel = Label(senderFrame, text = "Sender's Email ID", font = ('arial',14,'bold'),background='grey20',foreground ='white')
        senderLabel.grid(row = 0, column = 0,padx = 10 ,pady = 8)
        senderEntry = Entry(senderFrame,font = ('arial',14,'bold'),bd = 2,width = 23, relief = RIDGE)
        senderEntry.grid(row = 0, column = 1,padx = 10 ,pady = 8)

        passwordLabel = Label(senderFrame, text="Password", font=('arial', 14, 'bold'), background='grey20',
                            foreground='white')
        passwordLabel.grid(row=1, column=0, padx=10, pady=8)
        passwordEntry = Entry(senderFrame, font=('arial', 14, 'bold'), bd=2, width=23, relief=RIDGE,show='*')
        passwordEntry.grid(row=1, column=1, padx=10, pady=8)

        #Receiver Email Entry
        receiverFrame = LabelFrame(root1, text='RECIPIENT', font=('arial', 16, 'bold'), background='grey20', foreground='white')
        receiverFrame.grid(row=1, column=0, padx=40, pady=20)

        receiverLabel = Label(receiverFrame, text="Email Address", font=('arial', 14, 'bold'), background='grey20',
                              foreground='white')
        receiverLabel.grid(row=0, column=0, padx=10, pady=8)
        receiverEntry = Entry(receiverFrame, font=('arial', 14, 'bold'), bd=2, width=23, relief=RIDGE)
        receiverEntry.grid(row=0, column=1, padx=10, pady=8)

        #Message
        messageLabel = Label(receiverFrame, text="Message", font=('arial', 14, 'bold'), background='grey20',
                              foreground='white')
        messageLabel.grid(row=1, column=0, padx=10, pady=8)

        emailtextArea = Text(receiverFrame, font=('arial', 14, 'bold'), bd = 2, relief=SUNKEN,width=42,height=11)
        emailtextArea.grid(row=2, column=0, padx=10, pady=8,columnspan =2)
        emailtextArea.delete('1.0',END)
        emailtextArea.insert(END,textArea.get('1.0', END).replace('=','').replace('-','').replace('\t\t\t ','\t\t'))

        sendButton = Button(root1,text='SEND',font=('arial', 16, 'bold'),width=15,command=send_gmail)
        sendButton.grid(row=2, column=0, padx=10, pady=8)


        root1.mainloop()



def print_bill():
    if textArea.get(1.0,END) == '\n':
        messagebox.showerror('Error','Nothing to print')
    else:
        file= tempfile.mktemp('.txt')
        open(file, 'w').write(textArea.get(1.0,END))
        os.startfile(file,'print')


def clearAll():
    global totalPrice
    totalPrice  = 0
    nameEntry.delete(0,END)
    phoneEntry.delete(0, END)
    billEntry.delete(0, END)
    textArea.delete(1.0, END)

    textArea.insert(1.0, '\t   ***Medical Store***\n\n')
    textArea.insert(END, '\tContact Number:0311-5552866\n\tEmail:mansoorpay@gmail.com\n')
    textArea.insert(END, '========================================\n')
    textArea.insert(END, '  Item\t\tQuantity\t\tPrice\n')
    textArea.insert(END, '========================================\n')


def total():
    textArea.insert(END, f'\n\nTotal Bill \t\t\t\t{totalPrice} Rs\n')
    textArea.insert(END, '----------------------------------------\n\n')
    textArea.insert(END, 'Developed by Django Softwate PVT\n')
    textArea.insert(END, 'Contact:92-311-5552866  Email:mansoorpay@gmail.com\n')

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Mansoor@9008",
    host="localhost",
    port="5432"
    )
cursor = conn.cursor()


def submit():
    #textArea.insert(0,nameEntry.get())
    entered_name = nameEntry.get()
    quantity_Entry = phoneEntry.get()
    priceEntry = billEntry.get()
    cursor.execute("INSERT INTO Projects(name, mquntity,mprice, mname, number) VALUES (%s, %s,  %s,  %s,  %s)" ,(entered_name, quantity_Entry, priceEntry,'try','0'))
    conn.commit()
    readitems()

def readitems():
    cursor.execute("SELECT name FROM Projects;")
    records = cursor.fetchall()
    projectsList.delete(0, END)
    for record in records:
        projectsList.insert(END, f'{record[0]}')


def on_select(event):
    global totalPrice
    selectedIndex = projectsList.curselection()

    if selectedIndex:
        item = projectsList.get(selectedIndex)
        query = "SELECT mprice FROM Projects WHERE name = %s"
        cursor.execute(query, (item,))
        price = cursor.fetchone()[0]
        totalPrice = totalPrice + int(price)
        textArea.insert(END, f'  {item}\t\t1\t\t{price}\n')
        # print(f'Selected item is {item}')
    else:
        messagebox.INFO('Not Found','Unknown Error')

totalPrice = 0



# GUI Part
root = Tk()
root.title("POS")


root.geometry('1270x800')
#root.iconbitmap("icon.ico")
headingLabel= Label(root,text="Offline Software Managment",font=('times new roman',30,'bold'),background='gray20',foreground='gold',bd=12,relief=GROOVE)
headingLabel.pack(fill=X,pady=5)


# Customers Details Frame
costumer_details_frame = LabelFrame(root,text="New Entry",font=('times new roman',15,'bold'),foreground='gold',bd=8,relief=GROOVE,background='gray20')
costumer_details_frame.pack(fill=X)

nameLabel=Label(costumer_details_frame,text='Item Name',font=('times new roman',15,'bold'),background='gray20',foreground='white')
nameLabel.grid(row=0,column=0,padx=20)

nameEntry=Entry(costumer_details_frame,font=('arial',15),bd=7,width=18)
nameEntry.grid(row=0,column=1,padx=8)

phoneLabel=Label(costumer_details_frame,text='Quantity',font=('times new roman',15,'bold'),background='gray20',foreground='white')
phoneLabel.grid(row=0,column=2,padx=20,pady=2)

phoneEntry=Entry(costumer_details_frame,font=('arial',15),bd=7,width=18)
phoneEntry.grid(row=0,column=3,padx=8)

billnumberLabel=Label(costumer_details_frame,text='Price',font=('times new roman',15,'bold'),background='gray20',foreground='white')
billnumberLabel.grid(row=0,column=4,padx=20,pady=2)

billEntry=Entry(costumer_details_frame,font=('arial',15),bd=7,width=18)
billEntry.grid(row=0,column=5,padx=8)

submitButton= Button(costumer_details_frame,text="Submit",font=('arial',12,'bold'),bd=7,width=10,command=submit)
submitButton.grid(row=0,column=6,padx=20)

#Project Details
projectPanel = Frame(root,background='gray20')
projectPanel.pack(fill= X,pady=5)


items_details_frame = LabelFrame(projectPanel,text="Items",font=('times new roman',15,'bold'),foreground='gold',bd=8,relief=GROOVE,background='gray20')
items_details_frame.grid(row=0,column=0,padx=50)

#Listbox
search_entry = Entry(items_details_frame,  width=40,font=('arial',15),bd=7)
search_entry.bind("<KeyRelease>", update_listbox)
search_entry.grid(row=0,column=0,padx=5)
projectsList = Listbox(items_details_frame,bd=5,font=('arial',15,),height=15,width=40,relief=GROOVE)
projectsList.bind('<Return>',on_select)
projectsList.grid(row=1,column=0,padx=5)

#Bill Area
billFrame=Frame(projectPanel,bd=8,relief=GROOVE)
billFrame.grid(row=0,column=2,padx=50,pady = 5)
bill_details_frame = Label(billFrame,text="Bill",font=('times new roman',15,'bold'),bd=8,relief=GROOVE)
bill_details_frame.pack(fill=X)
scrollbar=Scrollbar(billFrame,orient=VERTICAL)
scrollbar.pack(side=RIGHT,fill=Y)
textArea = Text(billFrame,height=25,width=40,yscrollcommand=scrollbar.set)
textArea.pack()
scrollbar.config(command=textArea.yview)
textArea.insert(1.0,'\t   ***Medical Store***\n\n')
textArea.insert(END,'\tContact Number:0311-5552866\n\tEmail:mansoorpay@gmail.com\n')
textArea.insert(END,'========================================\n')
textArea.insert(END,'  Item\t\tQuantity\t\tPrice\n')
textArea.insert(END,'========================================\n')
readitems()



#Bill menu frame

billmenuframe = LabelFrame(projectPanel,text="Buttons",font=('times new roman',15,'bold'),foreground='gold',bd=8,relief=GROOVE,background='gray20')
billmenuframe.grid(row=0,column=1,padx=20)

totalbutton=Button(billmenuframe,text="Total",font=('arial',16,'bold'),background="gray20",
                   foreground='white',bd=5,width=8,pady=10,command=total)
totalbutton.grid(row=0,column=0,pady=5,padx=10)

billbutton=Button(billmenuframe,text="Bill",font=('arial',16,'bold'),background="gray20",foreground='white',bd=5,width=8,pady=10)
billbutton.grid(row=1,column=0,pady=5,padx=10)

emailbutton=Button(billmenuframe,text="Email",font=('arial',16,'bold'),background="gray20",
                   foreground='white',bd=5,width=8,pady=10,command=send_email)
emailbutton.grid(row=2,column=0,pady=5,padx=10)

printbutton=Button(billmenuframe,text="Print",font=('arial',16,'bold'),background="gray20",
                   foreground='white',bd=5,width=8,pady=10,command=print_bill)
printbutton.grid(row=3,column=0,pady=5,padx=10)

clearbutton=Button(billmenuframe,text="Clear",font=('arial',16,'bold'),background="gray20",
                   foreground='white',bd=5,width=8,pady=10,command=clearAll)
clearbutton.grid(row=4,column=0,pady=5,padx=10)


root.mainloop()
