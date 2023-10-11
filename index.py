from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import tkinter.ttk as ttk
from PIL import Image, ImageTk  # Import PIL modules for handling images

root = Tk()
root.title("CEA Inventory System")

# Load the background image
bg_image = Image.open("cealogo.png")
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to display the background image
bg_label = Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)


width = 1080
height = 740
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable()
# root.config(bg="#6666ff")

#========================================VARIABLES========================================
USERNAME = StringVar()
PASSWORD = StringVar()
EQUIPMENT_NAME = StringVar()
EQUIPMENT_STATUS = StringVar()
EQUIPMENT_QUANTITY = IntVar()
SEARCH = StringVar()

#========================================METHODS==========================================

def Database():
    global conn, cursor
    conn = sqlite3.connect("inventoryTable.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `equipment` (equipment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, equipment_name TEXT, equipment_status TEXT, equipment_quantity TEXT)")
    cursor.execute("SELECT * FROM `admin` WHERE `username` = 'comlab_admin' AND `password` = 'ce@c0mlab'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `admin` (username, password) VALUES('comlab_admin', 'ce@c0mlab')")
        conn.commit()

def Exit():
    result = tkMessageBox.askquestion(message='Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

def Exit2():
    result = tkMessageBox.askquestion(message='Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        Home.destroy()
        exit()

def ShowLoginForm():
    global loginform
    loginform = Toplevel()
    loginform.title("Account Login")
    width = 500
    height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    loginform.resizable(0, 0)
    loginform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    LoginForm()
    
def LoginForm():
    global lbl_result
    TopLoginForm = Frame(loginform, width=600, height=100, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopLoginForm, text="Administrator Login", font=('arial', 18), width=300)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(loginform, width=300)
    MidLoginForm.pack(side=TOP, pady=50)
    lbl_username = Label(MidLoginForm, text="Username:", font=('arial', 15), bd=10)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="Password:", font=('arial', 15), bd=10)
    lbl_password.grid(row=1)
    lbl_result = Label(MidLoginForm, text="", font=('arial', 15))
    lbl_result.grid(row=3, columnspan=2)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 15), width=15)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 15), width=15, show="*")
    password.grid(row=1, column=1)
    btn_login = Button(MidLoginForm, text="Login", font=('arial', 15), width=20, command=Login)
    btn_login.grid(row=2, columnspan=2, pady=20)
    btn_login.bind('<Return>', Login)
    
def Home():
    global Home
    Home = Tk()
    Home.title("Home")
    width = 1080
    height = 740
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/4) - (width/4)
    y = (screen_height/4) - (height/4)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    Home.resizable()
    Title = Frame(Home, bd=1, relief=FLAT)
    Title.pack(pady=10)
    lbl_display = Label(Title, text="ComLab Inventory Management System", font=('arial', 30))
    lbl_display.pack(anchor="center")
    menubar = Menu(Home)
    filemenu = Menu(menubar, tearoff=0)
    filemenu2 = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Logout", command=Logout)
    filemenu.add_command(label="Exit", command=Exit2)
    filemenu2.add_command(label="Add new", command=ShowAddNew)
    filemenu2.add_command(label="View", command=ShowView)
    menubar.add_cascade(label="Action", menu=filemenu)
    menubar.add_cascade(label="Inventory", menu=filemenu2)
    Home.config(menu=menubar)
    Home.config(bg="#32a852")

def ShowAddNew():
    global addnewform
    addnewform = Toplevel()
    addnewform.title("ComLab Inventory Management System/Add new")
    width = 600
    height = 500
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    addnewform.resizable(0, 0)
    AddNewForm()

def AddNewForm():
    TopAddNew = Frame(addnewform, width=600, height=100, bd=1, relief=SOLID)
    TopAddNew.pack(side=TOP, pady=20)
    lbl_text = Label(TopAddNew, text="Add Equipment", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidAddNew = Frame(addnewform, width=600)
    MidAddNew.pack(side=TOP, pady=50)
    lbl_equipmentname = Label(MidAddNew, text="Name:", font=('arial', 25), bd=10)
    lbl_equipmentname.grid(row=0, sticky=W)
    lbl_status = Label(MidAddNew, text="Status:", font=('arial', 25), bd=10)
    lbl_status.grid(row=1, sticky=W)
    lbl_price = Label(MidAddNew, text="Quantity:", font=('arial', 25), bd=10)
    lbl_price.grid(row=2, sticky=W)
    equipmentname = Entry(MidAddNew, textvariable=EQUIPMENT_NAME, font=('arial', 25), width=15)
    equipmentname.grid(row=0, column=1)
    equipmentstatus = Entry(MidAddNew, textvariable=EQUIPMENT_STATUS, font=('arial', 25), width=15)
    equipmentstatus.grid(row=1, column=1)
    equipmentquantity = Entry(MidAddNew, textvariable=EQUIPMENT_QUANTITY, font=('arial', 25), width=15)
    equipmentquantity.grid(row=2, column=1)
    btn_add = Button(MidAddNew, text="Save", font=('arial', 18), width=30, bg="#009ACD", command=AddNew)
    btn_add.grid(row=3, columnspan=2, pady=20)



def AddNew():
    Database()
    cursor.execute("INSERT INTO `equipment` (equipment_name, equipment_status, equipment_quantity) VALUES(?, ?, ?)", (str(EQUIPMENT_NAME.get()), str(EQUIPMENT_STATUS.get()), int(EQUIPMENT_QUANTITY.get())))
    conn.commit()
    EQUIPMENT_NAME.set("")
    EQUIPMENT_STATUS.set("")
    EQUIPMENT_QUANTITY.set("")
    cursor.close()
    conn.close()

def ViewForm():
    global tree
    TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=600)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=600)
    MidViewForm.pack(side=RIGHT)
    lbl_text = Label(TopViewForm, text="View Equipments", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftViewForm, text="Search", font=('arial', 15))
    lbl_txtsearch.pack(side=TOP, anchor=W)
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('arial', 15), width=10)
    search.pack(side=TOP,  padx=10, fill=X)
    btn_search = Button(LeftViewForm, text="Search", command=Search)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_reset = Button(LeftViewForm, text="Reset", command=Reset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_delete = Button(LeftViewForm, text="Delete", command=Delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=("EquipmentID", "Equipment Name", "Equipment Status", "Equipment Quantity"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('EquipmentID', text="EquipmentID",anchor=W)
    tree.heading('Equipment Name', text="Equipment Name",anchor=W)
    tree.heading('Equipment Status', text="Equipment Status",anchor=W)
    tree.heading('Equipment Quantity', text="Equipment Quantity",anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=0)
    tree.column('#2', stretch=NO, minwidth=0, width=200)
    tree.column('#3', stretch=NO, minwidth=0, width=120)
    tree.column('#4', stretch=NO, minwidth=0, width=120)
    tree.pack()
    DisplayData()

def DisplayData():
    Database()
    cursor.execute("SELECT * FROM `equipment`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database()
        cursor.execute("SELECT * FROM `equipment` WHERE `equipment_name` LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def Reset():
    tree.delete(*tree.get_children())
    DisplayData()
    SEARCH.set("")

def Delete():
    if not tree.selection():
       print("ERROR")
    else:
        result = tkMessageBox.askquestion('Are you sure you want to delete this record?',
                                          icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `product` WHERE `equipment_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
    

def ShowView():
    global viewform
    viewform = Toplevel()
    viewform.title("View Product")
    width = 600
    height = 400
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    viewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    viewform.resizable(0, 0)
    ViewForm()

def Logout():
    result = tkMessageBox.askquestion(message='Are you sure you want to logout?',
                                      icon="warning")
    if result == 'yes': 
        admin_id = ""
        root.deiconify()
        Home.destroy()
  
def Login(event=None):
    global admin_id
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
            data = cursor.fetchone()
            admin_id = data[0]
            USERNAME.set("")
            PASSWORD.set("")
            lbl_result.config(text="")
            ShowHome()
        else:
            lbl_result.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close() 

def ShowHome():
    root.withdraw()
    Home()
    loginform.destroy()


#========================================MENUBAR WIDGETS==================================
menubar = Menu(root)
filemenu = Menu(
    menubar,
    tearoff=0)
filemenu.add_command(label="Login", command=ShowLoginForm)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="Action", menu=filemenu)
root.config(menu=menubar)

#========================================FRAME============================================
Title = Frame(
    root, bd=1,
    relief=FLAT)
Title.pack()

#========================================LABEL WIDGET=====================================
lbl_display = Label(
    Title, 
    text="Computer Laboratory Inventory Management System", 
    font=('arial', 30),
)
lbl_display.pack()


#========================================INITIALIZATION===================================
if __name__ == '__main__':
    root.mainloop()