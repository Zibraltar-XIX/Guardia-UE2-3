import os
import pandas as pd
import hashlib
import secrets
import smtplib
from email.message import EmailMessage
import re
from pwned import pwned
from pwned import pwned_description
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from tkinter.ttk import Treeview, Combobox

#Tools
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def logo():
    print(" __________________________________________________\n|                                                  |\n|     /$$$$$$$$                  /$$               |\n|    |__  $$__/                 | $$               |\n|       | $$  /$$$$$$   /$$$$$$ | $$  /$$$$$$$     |\n|       | $$ /$$__  $$ /$$__  $$| $$ /$$_____/     |\n|       | $$| $$  \ $$| $$  \ $$| $$|  $$$$$$      |\n|       | $$| $$  | $$| $$  | $$| $$ \____  $$     |\n|       | $$|  $$$$$$/|  $$$$$$/| $$ /$$$$$$$/     |\n|       |__/ \______/  \______/ |__/|_______/      |\n|                                                  |\n'=================================================='\n\n")

def clear():
    for widget in window.winfo_children():
        widget.destroy()

#Seller menu
def tri(choice, tree, df):
    if choice == "Per price":
        df_filtered = df[df['OWNER'] == cookie_username]
        df_sorted = df_filtered.sort_values(by='PRICE', ascending=True)
    elif choice == "Per stock":
        df_filtered = df[df['OWNER'] == cookie_username]
        df_sorted = df_filtered.sort_values(by='STOCK', ascending=True)
    update_treeview(tree, df_sorted)

def update_treeview(tree, df):
    for row in tree.get_children():
        tree.delete(row)
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

def main_menu():
    clear()
    window.title("Seller menu")
    window.config(background='white')
    window.minsize(500, 350)

    df = pd.read_csv('data.csv', encoding='utf-8')
    column_names = ['OBJECT', 'PRICE', 'STOCK', 'OWNER']
    tree = Treeview(window, columns=column_names, show='headings')

    tri("Per stock", tree, df)

    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.pack()

    add_btn = Button(window, text="Add", command=add)
    add_btn.pack()
    del_btn = Button(window, text="Delete", command=lambda: supr(tree))
    del_btn.pack()
    search_btn = Button(window, text="Research", command=recherche)
    search_btn.pack()

    combobox = Combobox(window, values=["Per price", "Per stock"]) 
    combobox.set("Per price")
    combobox.pack(pady=20)

    tri_btn = Button(window, text="Tri", command=lambda: tri(combobox.get(), tree, df))
    tri_btn.pack()

    window.mainloop()

def add():
    clear()
    #Config Tkinter
    window.title("Register")
    window.config(background='white')
    window.minsize(300, 150)

    #Tkinter object's
    object_label = Label(window, text="Object")
    object_label.pack()
    object = StringVar()
    object_entry = Entry(window, textvariable=object)
    object_entry.pack()

    price_label = Label(window, text="Price")
    price_label.pack()
    price = StringVar()
    price_entry = Entry(window, textvariable=price)
    price_entry.pack()

    stock_label = Label(window, text="Stock")
    stock_label.pack()
    stock = StringVar()
    stock_entry = Entry(window, textvariable=stock)
    stock_entry.pack()


    def add_action():
        df = pd.read_csv('data.csv', encoding='utf-8')
        object = object_entry.get()
        price = price_entry.get()
        stock = stock_entry.get()
        new_row = pd.DataFrame([{
            'OBJECT': object,
            'PRICE': price,
            'STOCK' : stock,
            'OWNER': cookie_username,
        }])

        entry = messagebox.askquestion("validation", "Is this correct ?\n\n" f"Object name : {object}\n" f"Price : {price}\n" f"Stock : {stock}")
            
        if entry != "yes":
            return

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv('data.csv', index=False, encoding='utf-8')
        main_menu()
    
    add_btn = Button(window, text="Add", command=add_action)
    add_btn.pack()
    exit_btn = Button(window, text="Exit", command=main_menu)
    exit_btn.pack()



    """df = pd.read_csv('data.csv', encoding='utf-8')
    product = ''
    price = ''
    stock = ''

    while product == '':
        cls()
        logo()
        product = input("Enter your product's name : ")
        verif = df[df['OBJECT'] == product]
        if verif.empty:
            product = product
        else :
            input("Product already exist, sorry.\n\nEnter to try an other one...")
            product = ''

    while price == '':
        cls()
        logo()
        price = input("Enter product's price : ")
        if not price.isdigit():
            cls()
            logo()
            price = ''
            input("Enter a number please.\n\nEnter to continue...")

    while stock == '':
        cls()
        logo()
        stock = input("Enter the stock of this product : ")
        if not stock.isdigit():
            cls()
            logo()
            stock = ''
            input("Enter a number please.\n\nEnter to continue...")
        elif stock == "0":
            stock = "Out of stock !"

    cls()
    logo()
    print("Summary :\n")
    print("Product name : ", product, "\nPrice : ", price, "$\nStock : ", stock)
    
    while True:
        entry = input("\nThis is correct ? (y/n) : ")            

        if entry == "y":
            df = pd.read_csv('data.csv', encoding='utf-8')
            new_row = pd.DataFrame([{
                'OBJECT': product,
                'PRICE': price,
                'STOCK': stock,
                'OWNER': cookie_username,
            }])

            df = pd.concat([df, new_row], ignore_index=True)

            df.to_csv('data.csv', index=False, encoding='utf-8')
            cls()
            logo()
            print("Product saved successfully.")
            input("\n\nPress Enter to continue...")
            break

        elif entry == "n":
            break
        else:
            print("Type y for yes, n for no and modify, or q to return to user menu.")"""

def supr(tree):
    def on_select(tree):
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "You must select an object")
            return None
        selected_item = selected_items[0]
        selected_data = tree.item(selected_item, "values")
        return selected_data

    selected_line = on_select(tree)
    if not selected_line:
        return

    df = pd.read_csv('data.csv', encoding='utf-8')
    object_found = df[df['OBJECT'] == selected_line[0]]
    if object_found.empty:
        messagebox.showerror("Error", "Object not found")
        return

    owner = object_found.iloc[0]['OWNER']
    if owner != cookie_username:
        messagebox.showinfo("Error", "You are not the owner of this product")
        return

    x = object_found.index[0]
    df = df.drop(index=x)
    df.to_csv('data.csv', index=False, encoding='utf-8')
    main_menu()

def recherche():
    df = pd.read_csv('data.csv', encoding='utf-8')
    search = simpledialog.askstring("search", "Enter the product name : ")
    object_found = df[df['OBJECT'] == search]
    if object_found.empty:
        messagebox.showerror("Product not found, sorry.")
        return
    product = object_found.iloc[0]['OBJECT']
    price = object_found.iloc[0]['PRICE']
    stock = object_found.iloc[0]['STOCK']
    owner = object_found.iloc[0]['OWNER']
    if owner != cookie_username:
        messagebox.showerror("Product not found, sorry.")
        return
    messagebox.showinfo("search", f"Product name : {product}\nPrice : {price}\nStock : {stock}")

#User menu
def user_menu():
    while True:
        clear()
        #Config Tkinter
        window.title("User Menu")
        window.config(background='white')
        window.minsize(300, 150)

        #Tkinter object
        title = Label(window, text="User Menu", font=("Courrier", 15), bg="white")
        title.pack()

        if cookie_username == '':
            opt1 = Button(window, text="Log in", command=login)
            opt1.pack()

            opt2 = Button(window, text="Register", command=register)
            opt2.pack()

        elif cookie_username != '':

            opt3 = Button(window, text="Account details", command=account_det)
            opt3.pack()

            opt4 = Button(window, text="Modify account", command=user_modif)
            opt4.pack()
 
            opt5 = Button(window, text="Delete account", command=user_del)
            opt5.pack()

            opt6 = Button(window, text="log out", command=logout)
            opt6.pack()

            opt7 = Button(window, text="Seller menu", command=main_menu)
            opt7.pack()

        if cookie_username == "Admin":
 
            opt8 = Button(window, text="Check password", command=leaks_to_email)
            opt8.pack()

            opt9 = Button(window, text="List users", command=list_user)
            opt9.pack() 

        window.mainloop()       

def list_user():
    cls()
    logo()
    database = pd.read_csv('users.csv')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(database)
    input("\n\nEnter to continue...")

def register():
    clear()

    #Config Tkinter
    window.title("Register")
    window.config(background='white')
    window.minsize(300, 150)

    #Tkinter object's
    username_label = Label(window, text="Username")
    username_label.pack()
    username = StringVar()
    username_entry = Entry(window, textvariable=username)
    username_entry.pack()

    password_label = Label(window, text="Password")
    password_label.pack()
    password = StringVar()
    password_entry = Entry(window, textvariable=password, show='*')
    password_entry.pack()

    description_label = Label(window, text="Description")
    description_label.pack()
    description = StringVar()
    description_entry = Entry(window, textvariable=description)
    description_entry.pack()

    mail_label = Label(window, text="Mail")
    mail_label.pack()
    mail = StringVar()
    mail_entry = Entry(window, textvariable=mail)
    mail_entry.pack()


    def register_action():
        df = pd.read_csv('users.csv', encoding='utf-8')
        username = username_entry.get()
        password = password_entry.get()
        description = description_entry.get()
        mail = mail_entry.get()
        verif = df[df['USERNAME'] == username]
        leaks = pd.read_csv('leaks.csv', encoding='utf-8')
        nb_rows = len(leaks)
        check = "ok"
        salt = secrets.token_hex(16)
        password_salted = salt+password
        hashpassword = hashlib.sha512(password_salted.encode()).hexdigest()
        new_row = pd.DataFrame([{
            'USERNAME': username,
            'PASSWORD': hashpassword,
            'SALT' : salt,
            'DESCRIPTION': description,
            'MAIL': mail
        }])
        rep = ""

        #Username
        if username == '':
            messagebox.showerror("fail", "Username cannot be empty")
            return
        
        if not verif.empty:
            messagebox.showerror("fail", "Username already exist, sorry.")
            return

        #Password
        if password == "" or len(password) < 8 :
            messagebox.showerror("fail", "Password must have 8 characters or more")
            return

        for i in range(nb_rows):
            verif = leaks.iloc[i]['PASSWORD']
            if verif == password:
                check = "leak"
                break

        if check == "leak" or pwned(password):
            rep = messagebox.askquestion("Leak", "The password is present on web leaks. Choose a better password, more info here :\nhttps://www.cisa.gov/secure-our-world/use-strong-passwords .\n\nDo you want to force this password ?")
            if rep != "yes":
                return

        #Description
        if description == '':
            description = "Nothing here !"
        
        #Mail
        if mail == '' or not is_valid_email(mail):
            messagebox.showerror("fail","You need enter a valid email.")
            return

        entry = messagebox.askquestion("validation", "Is this correct ?\n\n" f"Username : {username}\n" f"Password : {password}\n" f"Description : {description}\n" f"Email : {mail}" )
            
        if entry != "yes":
            return

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv('users.csv', index=False, encoding='utf-8')
        if rep == "yes":
            messagebox.showinfo("email send","Register can take few minute")
            email_send(mail, username)

        messagebox.showinfo("success","Your account have been created.")
        global cookie_username
        cookie_username = username
        user_menu()
    
    register_btn = Button(window, text="Register", command=register_action)
    register_btn.pack()
    exit_btn = Button(window, text="Exit", command=user_menu)
    exit_btn.pack()
    
def login():
    global cookie_username
    clear()

    #Config Tkinter
    window.title("Login")
    window.config(background='white')
    window.minsize(300, 150)

    #Tkinter object's
    username_label = Label(window, text="Username")
    username_label.pack()
    username = StringVar()
    username_entry = Entry(window, textvariable=username)
    username_entry.pack()

    password_label = Label(window, text="Password")
    password_label.pack()
    password = StringVar()
    password_entry = Entry(window, textvariable=password, show='*')
    password_entry.pack()
     
    def login_action():
        global cookie_username

        df = pd.read_csv('users.csv', encoding='utf-8')
        user_found = df[df['USERNAME'] == username_entry.get()]

        if user_found.empty:
            messagebox.showerror("Error", "Username not found!")
            return

        salt = user_found.iloc[0]['SALT']
        password_salted = salt+password_entry.get()
        hashpassword = hashlib.sha512(password_salted.encode()).hexdigest()

        if user_found.iloc[0]['PASSWORD'] == hashpassword:
            cookie_username = username_entry.get()
            user_menu()

        else:
            messagebox.showerror("Error", "Password incorrect !")
            return
    
    login_btn = Button(window, text="Log in", command=login_action)
    login_btn.pack()
    return
    
def account_det():
    df = pd.read_csv('users.csv', encoding='utf-8')
    user_found = df[df['USERNAME'] == cookie_username]

    account = user_found.iloc[0]['USERNAME']
    psword = user_found.iloc[0]['PASSWORD']
    desc = user_found.iloc[0]['DESCRIPTION']
    mail = user_found.iloc[0]['MAIL']

    messagebox.showinfo("your account", f"Account : {account}\nPassword's hash : {psword}\nDescription : {desc}\nEmail : {mail}")

def user_del():
    df = pd.read_csv('users.csv', encoding='utf-8')
    df = df[df['USERNAME'] != cookie_username]
    df.to_csv('users.csv', index=False, encoding='utf-8')
    rep = messagebox.askquestion("delete", "Are you sure to delete your account ?")
    if rep == "yes":
        cookie_username = ''
        messagebox.showinfo(f"User '{cookie_username}' has been successfully deleted.")

def user_modif():
    while True:
        clear()
        #Tkinter window
        window.title("User Modification")
        window.config(background='white')
        window.minsize(300, 150)

        def username_modif():
            global cookie_username
            df = pd.read_csv('users.csv', encoding='utf-8')
            rep = simpledialog.askstring("username", "Enter your new username :")
            confirm = messagebox.askquestion("confirmation", f"Your new username will be : {rep}")
            if confirm == "yes":
                df.loc[df['USERNAME'] == cookie_username, 'USERNAME'] = rep
                df.to_csv('users.csv', index=False, encoding='utf-8')
                cookie_username = rep
                
        def password_modif():
            df = pd.read_csv('users.csv', encoding='utf-8')
            leaks = pd.read_csv('leaks.csv', encoding='utf-8')
            nb_rows = len(leaks)
            check = ""
            password = simpledialog.askstring("password", "Enter your new password :")
            for i in range(nb_rows):
                verif = leaks.iloc[i]['PASSWORD']
                if verif == password:
                    check = "leak"
                    break

            if check == "leak" or pwned(password):
                rep = messagebox.askquestion("\nThe password is present on web leaks. Choose a better password, more info here :\nhttps://www.cisa.gov/secure-our-world/use-strong-passwords .\n\nDo you want to force this password ? (y or else) : ")
                if rep != "yes":
                    return

            salt = secrets.token_hex(16)
            password_salted = salt+password
            hashpassword = hashlib.sha512(password_salted.encode()).hexdigest()
            confirm = messagebox.askquestion("confirmation", f"Your new password will be : {password}")
            if confirm == "yes":
                df.loc[df['USERNAME'] == cookie_username, 'PASSWORD'] = hashpassword
                df.loc[df['USERNAME'] == cookie_username, 'SALT'] = salt
                df.to_csv('users.csv', index=False, encoding='utf-8')

        def descr_modif():
            df = pd.read_csv('users.csv', encoding='utf-8')
            rep = simpledialog.askstring("description", "Enter your new description :")
            confirm = messagebox.askquestion("confirmation", f"Your new description will be : {rep}")
            if confirm == "yes":
                df.loc[df['USERNAME'] == cookie_username, 'DESCRIPTION'] = rep
                df.to_csv('users.csv', index=False, encoding='utf-8')

        def email_modif():
            df = pd.read_csv('users.csv', encoding='utf-8')
            rep = simpledialog.askstring("email", "Enter your new email :")
            confirm = messagebox.askquestion("confirmation", f"Your new email will be : {rep}")
            if confirm == "yes":
                df.loc[df['USERNAME'] == cookie_username, 'MAIL'] = rep
                df.to_csv('users.csv', index=False, encoding='utf-8')

    #Tkinter object
        title = Label(window, text="User modification", font=("Courrier", 15), bg="white")
        title.pack()

        opt3 = Button(window, text="Username", command=username_modif)
        opt3.pack()

        opt4 = Button(window, text="Password", command=password_modif)
        opt4.pack()
 
        opt5 = Button(window, text="Description", command=descr_modif)
        opt5.pack()

        opt6 = Button(window, text="Email", command=email_modif)
        opt6.pack()

        opt7 = Button(window, text="Exit", command=user_menu)
        opt7.pack()

        window.mainloop()

def logout():
    global cookie_username
    messagebox.showinfo("logout", f"You have been log out of {cookie_username}.")
    cookie_username = ''
    user_menu()

def leaks_to_email():
    cls()
    logo()
    print("Password check loading...")
    leaks = pd.read_csv('leaks.csv', encoding='utf-8')
    users = pd.read_csv('users.csv', encoding='utf-8')
    leaks_rows = len(leaks)
    users_rows = len(users)
    check = "ok"
    for i in range(users_rows):
        for j in range(leaks_rows):
            verif = leaks.iloc[j]['PASSWORD']
            password = users.iloc[i]['PASSWORD']
            email = users.iloc[i]['MAIL']
            user = users.iloc[i]['USERNAME']
            salt = users.iloc[i]['SALT']
            verif = salt+verif
            verif = hashlib.sha512(verif.encode()).hexdigest()
            if verif == password and check == "ok":
                check = "fail"
        
        password = users.iloc[i]['PASSWORD']
        if check == "fail" or pwned(password):
            email_send(email, user)
    cls()
    logo()
    input("Password check finish, enter to continue...")

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def email_send(email, user):
    # Configuration
    admin_email = 'contact@zibraltar.fr'
    email_password = 'z3qlPzjkqWh9IPVLjh821w'
    to_email = email
    subject = 'Security Alert'
    body = f"Hello {user},\nYour password has leaked on the internet!\nYou need to change it now if you want to have a better security for your account.\nYou can visit this web site to see how to create a good password : https://www.cisa.gov/secure-our-world/use-strong-passwords\nThank you for using our tool\nHave a good day !"

    # Création du message
    msg = EmailMessage()
    msg['From'] = admin_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.set_content(body)

    # Envoi de l'email
    server = smtplib.SMTP('127.0.0.1', 1025)
    server.starttls()
    server.login(admin_email, email_password)
    server.send_message(msg)
    server.quit()

global cookie_username
cookie_username = 'Admin'

try:
    df = pd.read_csv('data.csv', encoding='utf-8')
except FileNotFoundError:
    df = pd.DataFrame(columns=['OBJECT', 'PRICE', 'STOCK', 'OWNER'])
    df.to_csv('data.csv', index=False, encoding='utf-8')

try:
    df = pd.read_csv('users.csv', encoding='utf-8')
except FileNotFoundError:
    df = pd.DataFrame(columns=['USERNAME', 'PASSWORD', 'SALT', 'DESCRIPTION', 'MAIL'])
    df.to_csv('users.csv', index=False, encoding='utf-8')

try:
    with open("pwned.log", "r") as log_file:
        pass
except FileNotFoundError:
    with open("pwned.log", "w") as log_file:
        log_file.write("")

window = Tk()
user_menu()