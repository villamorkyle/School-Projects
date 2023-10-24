import tkinter as tk
from tkinter import Toplevel, Entry, Button, Label, Frame, Scrollbar, Treeview, StringVar
import tkinter.messagebox as tkMessageBox
import sqlite3

root = tk.Tk()
root.title("Computer Laboratory Inventory Manager")

# Define global variables and initialize them
USERNAME = StringVar()
PASSWORD = StringVar()
EQUIPMENT_NAME = StringVar()
EQUIPMENT_STATUS = StringVar()
EQUIPMENT_QUANTITY = StringVar()
SEARCH = StringVar()
admin_id = None  # Initialize admin_id to None

# Database function to connect to SQLite database
def Database():
    conn = sqlite3.connect("inventoryTable.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `equipment` (equipment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, equipment_name TEXT, equipment_status TEXT, equipment_quantity TEXT)")
    cursor.execute("SELECT * FROM `admin` WHERE `username` = 'comlab_admin' AND `password` = 'ce@c0mlab'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `admin` (username, password) VALUES('comlab_admin', 'ce@c0mlab')")
        conn.commit()
    conn.close()

# Define a function to create the Home window
def HomeWindow():
    home = Toplevel(root)
    home.title("Home")
    home.geometry("1080x740")

    Title = Frame(home, bd=1, relief="flat",)
    Title.pack(pady=10)
    lbl_display = Label(Title, text="ComLab Inventory Manager", font=('arial', 30),)
    lbl_display.pack()

    btn_add = Button(home, text="Add New Equipment", font=('arial', 18), width=30, command=ShowAddNew)
    btn_add.pack(pady=20)
    btn_view = Button(home, text="View Equipment", font=('arial', 18), width=30, command=ShowView)
    btn_view.pack(pady=20)

    menubar = Menu(home)
    filemenu = Menu(menubar, tearoff=0)
    filemenu2 = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Logout", command=Logout)
    filemenu.add_command(label="Exit", command=Exit2)
    menubar.add_cascade(label="Action", menu=filemenu)
    
    Home.config(menu=menubar)
    Home.config(bg='#C0C0C0')

# Define a function to show the login form
def ShowLoginForm():
    loginform = Toplevel(root)
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

# Define a function to handle login
def Login():
    global admin_id, root
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
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

# Define a function to log out
def Logout():
    result = tkMessageBox.askquestion('Logout', message='Are you sure you want to logout?', icon="warning")
    if result == 'yes': 
        admin_id = ""
        root.deiconify()
        Home.withdraw()

# Define a function to show the add new equipment form
def ShowAddNew():
    addnewform = Toplevel(root)
    addnewform.title("Add New Equipment")
    width = 600
    height = 500
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    addnewform.resizable(0, 0)
    AddNewForm()

# Define a function to handle adding new equipment
def AddNew():
    Database()
    cursor.execute("INSERT INTO `equipment` (equipment_name, equipment_status, equipment_quantity) VALUES(?, ?, ?)", (str(EQUIPMENT_NAME.get()), str(EQUIPMENT_STATUS.get()), int(EQUIPMENT_QUANTITY.get())))
    conn.commit()
    EQUIPMENT_NAME.set("")
    EQUIPMENT_STATUS.set("")
    EQUIPMENT_QUANTITY.set("")
    cursor.close()
    conn.close()

# Define a function to show the view equipment form
def ShowView():
    viewform = Toplevel(root)
    viewform.title("View Equipment")
    width = 600
    height = 400
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    viewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    viewform.resizable(0, 0)
    ViewForm()

# Define a function to display equipment data in the Treeview
def DisplayData():
    Database()
    cursor.execute("SELECT * FROM `equipment`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

# Call the Database function to initialize the database
Database()

# Set up the main window and menu
root.geometry("1080x740")
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create menu items for login, exit, and other actions
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Login", command=ShowLoginForm)
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Action", menu=filemenu)

# Create the Home button (you can create other buttons similarly)
btn_home = Button(root, text="Home", command=HomeWindow)
btn_home.pack()

# Start the main loop
root.mainloop()
