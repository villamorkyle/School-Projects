import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel, Entry, Button, Label, Frame, Scrollbar, StringVar, IntVar, Menu
import tkinter.messagebox as tkMessageBox
import sqlite3
from PIL import Image, ImageTk, ImageFilter

root = tk.Tk()
root.title("Computer Laboratory Inventory Manager")
root.state('zoomed')

bg_image = Image.open("cealogo.png")
bg_photo = ImageTk.PhotoImage(bg_image)

blurred = bg_image.filter(ImageFilter.BLUR)
bg_photo2 = ImageTk.PhotoImage(blurred)

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
    result = tkMessageBox.askquestion('Exit', message='Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

def Exit2():
    result = tkMessageBox.askquestion('Exit', message='Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        Home.destroy()
        exit()

def ShowLoginForm():
    global loginform
    loginform = Toplevel()
    loginform.title("Account Login")
    loginform.geometry("500x400+{}+{}".format(
    (loginform.winfo_screenwidth() - 500) // 2,  
    (loginform.winfo_screenheight() - 400) // 2 
))
    loginform.resizable(0, 0)
    LoginForm()
    
def LoginForm():
    global lbl_result
    TopLoginForm = Frame(loginform, width=600, height=100,)
    TopLoginForm.pack(side="top", pady=20)
    lbl_text = Label(TopLoginForm, text="Administrator Login", font=('Times New Roman', 25, 'bold'), width=300)
    lbl_text.pack(fill="x")
    MidLoginForm = Frame(loginform, width=300)
    MidLoginForm.pack(side="top", pady=50)
    lbl_username = Label(MidLoginForm, text="Username:", font=('Times New Roman', 15), bd=10)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="Password:", font=('Times New Roman', 15), bd=10)
    lbl_password.grid(row=1)
    lbl_result = Label(MidLoginForm, text="", font=('arial', 15))
    lbl_result.grid(row=3, columnspan=2)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 15), width=15)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 15), width=15, show="*")
    password.grid(row=1, column=1)
    btn_login = Button(MidLoginForm, text="Login", font=('arial', 15, 'bold'), width=20, command=Login)
    btn_login.grid(row=2, columnspan=2, pady=20)
    btn_login.bind('<Return>', Login)
    
def HomeWindow():
    global Home
    Home = Toplevel()
    Home.title("Home")
    Home.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    Home.resizable()
    Home.configure(bg='#E6E6E6')

    MainFrame = Frame(Home, bg="lightblue")
    MainFrame.pack(fill="both", expand=True)

    lbl_display = Label(
        MainFrame,
        text="ComLab Inventory Manager",
        font=('Times New Roman', 38, 'bold'),
        bg="lightblue",
        fg="black"
    )
    lbl_display.pack(pady=20)

    btn_add = Button(MainFrame, text="Add New Equipment", font=('Times New Roman', 18, 'bold'), width=30, command=ShowAddNew, bg="blue", fg="white")
    btn_add.pack(pady=20)

    btn_view = Button(MainFrame, text="View Equipment", font=('Times New Roman', 18, 'bold'), width=30, command=ShowView, bg="blue", fg="white")
    btn_view.pack(pady=20)

    menubar = Menu(Home)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Logout", command=Logout)
    filemenu.add_command(label="Exit", command=Exit2)
    menubar.add_cascade(label="Action", menu=filemenu)
    Home.config(menu=menubar)
    
addnewform = None    

def ShowAddNew():
    global addnewform
    
    if addnewform and addnewform.winfo_exists():
        if addnewform.state() == "iconic":
            addnewform.deiconify()
        else:
            addnewform.focus_set()
    else:
        addnewform = Toplevel()
        addnewform.title("ComLab Inventory Manager/Add new")
        addnewform.geometry("600x500+{}+{}".format(
            (addnewform.winfo_screenwidth() - 600) //2,
            (addnewform.winfo_screenheight() - 500) //2
        ))
        addnewform.resizable(0, 0)
        addnewform.configure(bg="gray")
        AddNewForm()

def AddNewForm():
    TopAddNew = Frame(addnewform, width=600, height=100,)
    TopAddNew.pack(side="top", pady=20)
    lbl_text = Label(TopAddNew, text="Add Equipment", font=('Times New Roman', 25, 'bold'), bg="gray", fg='white')
    lbl_text.pack(fill="x")
    MidAddNew = Frame(addnewform, width=600, bg="gray")
    MidAddNew.pack(side="top", pady=50)
    lbl_equipmentname = Label(MidAddNew, text="Name:", font=('Times New Roman', 25), bd=10, bg="gray", fg="white")
    lbl_equipmentname.grid(row=0, sticky="w")
    lbl_status = Label(MidAddNew, text="Status:", font=('Times New Roman', 25), bd=10, bg="gray", fg="white")
    lbl_status.grid(row=1, sticky="w")
    lbl_price = Label(MidAddNew, text="Quantity:", font=('Times New Roman', 25), bd=10, bg="gray", fg="white")
    lbl_price.grid(row=2, sticky="w")
    equipmentname = Entry(MidAddNew, textvariable=EQUIPMENT_NAME, font=('Times New Roman', 25), width=15)
    equipmentname.grid(row=0, column=1)
    equipmentstatus = Entry(MidAddNew, textvariable=EQUIPMENT_STATUS, font=('Times New Roman', 25), width=15)
    equipmentstatus.grid(row=1, column=1)
    equipmentquantity = Entry(MidAddNew, textvariable=EQUIPMENT_QUANTITY, font=('Times New Roman', 25), width=15)
    equipmentquantity.grid(row=2, column=1)
    btn_add = Button(MidAddNew, text="Add", font=('arial', 18, 'bold'), bg="blue", command=AddNew, fg="white")
    btn_add.grid(row=3, columnspan=2, pady=20)

def AddNew():
    Database()
    name = EQUIPMENT_NAME.get()
    status = EQUIPMENT_STATUS.get()
    quantity = EQUIPMENT_QUANTITY.get()

    if not name or not status or not quantity:
        tkMessageBox.showerror("Error", "Please fill in all fields.")
        return

    cursor.execute("INSERT INTO `equipment` (equipment_name, equipment_status, equipment_quantity) VALUES (?, ?, ?)", (str(name), str(status), int(quantity)))
    conn.commit()
    EQUIPMENT_NAME.set("")
    EQUIPMENT_STATUS.set("")
    EQUIPMENT_QUANTITY.set("")
    cursor.close()
    conn.close()
    tkMessageBox.showinfo("Success", "Equipment added successfully.")

def ViewForm():
    global tree
    TopViewForm = Frame(viewform, bd=1,)
    TopViewForm.pack(side="top", fill="x")

    search_frame = Frame(TopViewForm)
    search_frame.pack(side="left")

    search = Entry(search_frame, textvariable=SEARCH, font=('arial', 15), width=10)
    search.grid(row=0, column=0, padx=10)

    btn_search = Button(search_frame, text="Search", command=Search)
    btn_search.grid(row=0, column=1, padx=10, pady=10)

    buttons_frame = Frame(TopViewForm)
    buttons_frame.pack(side="right")

    btn_edit = Button(buttons_frame, text="Edit", command=Edit, bg='blue')
    btn_edit.grid(row=0, column=0, padx=10, pady=10)

    btn_reset = Button(buttons_frame, text="Reset", command=Reset)
    btn_reset.grid(row=0, column=1, padx=10, pady=10)

    btn_delete = Button(buttons_frame, text="Delete", command=Delete, bg='red')
    btn_delete.grid(row=0, column=2, padx=10, pady=10)

    MidViewForm = Frame(viewform, width=700)
    MidViewForm.pack(side="bottom",)

    scrollbarx = Scrollbar(MidViewForm, orient="horizontal")
    scrollbary = Scrollbar(MidViewForm, orient="vertical")
    tree = ttk.Treeview(MidViewForm, columns=("EquipmentID", "Equipment Name", "Equipment Status", "Equipment Quantity"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side="right", fill="y")
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side="bottom", fill="x")
    tree.heading('EquipmentID', text="EquipmentID", anchor="w")
    tree.heading('Equipment Name', text="Equipment Name", anchor="w")
    tree.heading('Equipment Status', text="Equipment Status", anchor="w")
    tree.heading('Equipment Quantity', text="Equipment Quantity", anchor="w")
    tree.column('#0', stretch="NO", minwidth=0, width=0)
    tree.column('#1', stretch="NO", minwidth=0, width=0)
    tree.column('#2', stretch="NO", minwidth=0, width=330)
    tree.column('#3', stretch="NO", minwidth=0, width=250)
    tree.column('#4', stretch="NO", minwidth=0, width=200)
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
       tkMessageBox.showerror("Error", "Please select an item to delete.")
    else:
        result = tkMessageBox.askquestion('Delete Equipment from Inventory', message='Are you sure you want to delete this record?',
                                          icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `equipment` WHERE `equipment_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
    
def Edit():
    selected_item = tree.selection()
    if not selected_item:
        tkMessageBox.showerror("Error", "Please select an item to edit.")
        return

    selected_item = tree.item(selected_item[0])  # Get the selected item
    item_data = selected_item['values']
    
    global editform
    editform = Toplevel()
    editform.title("Edit Equipment")
    editform.geometry("450x400+{}+{}".format(
        (editform.winfo_screenwidth() - 450) //2,
        (editform.winfo_screenheight() - 400) // 2
    ))

    fields = ["Name", "Status", "Quantity"]
    entry_values = []

    for i in range(len(fields)):
        label = Label(editform, text=fields[i] + ":", font=('arial', 25), bd=10) 
        label.grid(row=i, sticky="w")
        entry = Entry(editform, font=('arial', 25), width=15)  
        entry.insert(0, item_data[i + 1])
        entry.grid(row=i, column=1)
        entry_values.append(entry)

    save_button = Button(editform, text="Save Changes", font=('arial', 18), bg='red', command=lambda: SaveChanges(selected_item['values'][0], *[entry.get() for entry in entry_values]))
    save_button.grid(row=3, columnspan=2, pady=20, padx=(10, 10), )

def SaveChanges(item_id, new_name, new_status, new_quantity):
    Database()
    cursor.execute("UPDATE `equipment` SET equipment_name=?, equipment_status=?, equipment_quantity=? WHERE equipment_id=?", (new_name, new_status, new_quantity, item_id))
    conn.commit()
    cursor.close()
    conn.close()
    editform.destroy()
    Reset()
    tkMessageBox.showinfo("Success", "Equipment updated successfully.")
    
viewform = None

def ShowView():
    global viewform

    if viewform and viewform.winfo_exists():
        if viewform.state() == "iconic":
            viewform.deiconify()
        else:
            viewform.focus_set()
    else:
        viewform = Toplevel()
        viewform.title("View Equipments")
        viewform.geometry("800x600+{}+{}".format(
            (viewform.winfo_screenwidth() - 800) //2,
            (viewform.winfo_screenheight() - 600) // 2
        ))
        viewform.resizable(0, 0)
        ViewForm()

def Logout():
    result = tkMessageBox.askquestion('Logout', message='Are you sure you want to logout?', icon="warning")
    if result == 'yes': 
        root.deiconify()
        Home.withdraw()

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

def ShowHome():
    global admin_id
    if admin_id is not None:
        root.withdraw()
    HomeWindow()
    loginform.destroy() 
#==================================ROOT WINDOW COMPONENT==================================#
menubar = Menu(root)
filemenu = Menu(
    menubar,
    tearoff=0)
filemenu.add_command(label="Login", command=ShowLoginForm)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="Action", menu=filemenu)
root.config(menu=menubar)

Title = Frame(
    root, bd=1,
    relief="flat")
Title.pack()

lbl_display = Label(
    Title,
    text="Computer Laboratory Inventory Manager", 
    font=('Times New Roman', 40, 'bold'),
    image=bg_photo2,
    padx=300,
    pady=400,
    compound="center",
    fg="white"
)
lbl_display.pack()

def update_background_color():
    lbl_display.config(bg="gray")

update_background_color()

#===================================INITIALIZATION===================================#

root.mainloop()