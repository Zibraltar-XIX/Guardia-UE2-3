import os
import pandas as pd
import hashlib
import secrets
import smtplib
from email.message import EmailMessage
import re
from pwned import pwned
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Treeview, Combobox
import json
from tkinter.font import Font
from tkinter import font

#Tools
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
    window.minsize(500, 400)

    df = pd.read_csv('data.csv', encoding='utf-8')
    column_names = ['OBJECT', 'PRICE', 'STOCK', 'OWNER']
    tree = Treeview(window, columns=column_names, show='headings')

    tri("Per stock", tree, df)

    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.pack(pady=10)

    frame = Frame(window, bg="white")
    frame.pack(expand=YES)
    add_btn = Button(frame, text="Add", command=add, font=police)
    add_btn.pack(fill=X, pady=5)
    del_btn = Button(frame, text="Delete", command=lambda: supr(tree), font=police)
    del_btn.pack(fill=X, pady=5)
    search_btn = Button(frame, text="Research", command=recherche, font=police)
    search_btn.pack(fill=X, pady=5)

    combobox = Combobox(frame, values=["Per price", "Per stock"], font=police) 
    combobox.set("Per price")
    combobox.pack(fill=X, pady=5)

    tri_btn = Button(frame, text="Tri", command=lambda: tri(combobox.get(), tree, df), font=police)
    tri_btn.pack(fill=X, pady=5)

    view_order_btn = Button(frame, text="View buyer order", command=view_order_menu, font=police)
    view_order_btn.pack(fill=X, pady=5)

    exit_btn = Button(frame, text="Exit", command=user_menu, font=police)
    exit_btn.pack(fill=X, pady=5)

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
        messagebox.showerror("error", "Product not found, sorry.")
        return
    product = object_found.iloc[0]['OBJECT']
    price = object_found.iloc[0]['PRICE']
    stock = object_found.iloc[0]['STOCK']
    owner = object_found.iloc[0]['OWNER']
    if owner != cookie_username:
        messagebox.showerror("error", "Product not found, sorry.")
        return
    messagebox.showinfo("search", f"Product name : {product}\nPrice : {price}\nStock : {stock}")

#View order
def tri_order(choice, tree, df):
    if choice == "Per in progress":
        df_sorted = df[df['Statut'] == 'in progress']
    elif choice == "Per completed":
        df_sorted = df[df['Statut'] == 'completed']
    else:
        df_sorted = df

    update_treeview_order(tree, df_sorted)

def update_treeview_order(tree, df):
    # Effacer les lignes existantes dans le Treeview
    for row in tree.get_children():
        tree.delete(row)
    # Insérer les nouvelles données dans le Treeview
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

def delivered(tree, df): 
    selected_items = tree.selection() 
    if not selected_items: 
        messagebox.showerror("Error", "You must select an object") 
        return 
    selected_item = selected_items[0] 
    selected_data = tree.item(selected_item, "values") 
    index = df.index[(df['Object'] == selected_data[0]) & (df['How many'] == selected_data[1]) & 
                     (df['Buyer'] == selected_data[2]) & (df['Statut'] == selected_data[3])].tolist()[0]
    # Modifier le statut à "delivered"
    df.at[index, 'Statut'] = 'delivered'
    # Mettre à jour le fichier JSON
    df.to_json('command.json', orient='records', indent=4)
    # Mettre à jour le Treeview
    update_treeview_order(tree, df)

def view_order_menu():
    clear()
    window.title("View order menu")
    window.config(background='white')
    window.minsize(500, 350)

    with open('command.json', 'r', encoding='utf-8') as file: 
        data = json.load(file)
    df = pd.DataFrame(data)

    column_names = ['Object', 'How many', 'Buyer', 'Statut']
    tree = Treeview(window, columns=column_names, show='headings')

    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    update_treeview_order(tree, df)

    tree.pack()

    frame = Frame(window, bg="white")
    frame.pack(expand=YES)
    
    delivered_btn = Button(frame, text="Delivered", command=lambda: delivered(tree, df), font=police)
    delivered_btn.pack(fill=X, pady=5)

    combobox = Combobox(frame, values=["Per in progress", "Per completed"], font=police) 
    combobox.set("Per in progress")
    combobox.pack(pady=5)

    tri_btn = Button(frame, text="Tri", command=lambda: tri_order(combobox.get(), tree, df), font=police)
    tri_btn.pack(fill=X, pady=5)

    exit_btn = Button(frame, text="Exit", command=main_menu, font=police)
    exit_btn.pack(fill=X, pady=5)

    window.mainloop()

#Buyer menu
def tri_buyer(choice, tree, df):
    if choice == "Per price":
        df_sorted = df.sort_values(by='PRICE', ascending=True)
    elif choice == "Per stock":
        df_sorted = df.sort_values(by='STOCK', ascending=True)
    elif choice == "Per seller":
        df_sorted = df.sort_values(by='OWNER', ascending=True)
    update_treeview_buyer(tree, df_sorted)

def update_treeview_buyer(tree, df):
    for row in tree.get_children():
        tree.delete(row)
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

def buyer_menu():
    clear()
    window.title("Seller menu")
    window.config(background='white')
    window.minsize(500, 350)

    df = pd.read_csv('data.csv', encoding='utf-8')
    column_names = ['OBJECT', 'PRICE', 'STOCK', 'OWNER']
    tree = Treeview(window, columns=column_names, show='headings')

    tri_buyer("Per stock", tree, df)

    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.pack()

    stock_select = list(range(1, 1000))
    frame = Frame(window, bg="white")
    frame.pack(expand=YES)
    combobox_stock = Combobox(frame, values=stock_select) 
    combobox_stock.set("1")
    combobox_stock.pack(fill=X, pady=5)
    command_btn = Button(frame, text="Add to cart", command=lambda: command(tree, combobox_stock.get()))
    command_btn.pack(fill=X, pady=5)
    add_btn = Button(frame, text="Validate cart", command=confirm_command)
    add_btn.pack(fill=X, pady=5)
    delete_btn = Button(frame, text="Clean cart", command=delete_buyer)
    delete_btn.pack(fill=X, pady=5)
    combobox = Combobox(frame, values=["Per price", "Per stock", "Per seller"]) 
    combobox.set("Per seller")
    combobox.pack(pady=5)
    tri_btn = Button(frame, text="Tri", command=lambda: tri_buyer(combobox.get(), tree, df))
    tri_btn.pack(fill=X, pady=5)
    exit_btn = Button(frame, text="Exit", command=user_menu)
    exit_btn.pack(fill=X, pady=5)

    window.mainloop()

def confirm_command():
    global cookie_username
    try:
        with open('command.json', "r") as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    for item in data:
        if item["Buyer"] == cookie_username and item["Statut"] == "in progress":
            item["Statut"] = "completed"

    with open('command.json', "w") as json_file:
        json.dump(data, json_file, indent=4)

def delete_buyer():
    with open('command.json', "r") as json_file:
        data = json.load(json_file)

    data = [item for item in data if item["Buyer"] != cookie_username]

    with open('command.json', "w") as json_file:
        json.dump(data, json_file, indent=4)

def command(tree, number_asked):
    def on_select(tree):
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "You must select an object")
            return None
        selected_item = selected_items[0]
        selected_data = tree.item(selected_item, "values")
        return selected_data[0]

    selected_line = on_select(tree)
    if not selected_line:
        return
    
    global cookie_username

    new_data = {
        "Object": selected_line,
        "How many": number_asked,
        "Buyer": cookie_username,
        "Statut": "in progress",
    }

    try:
        with open('command.json', "r") as json_file:
            if os.path.getsize('command.json') > 0:
                existing_data = json.load(json_file)
            else:
                existing_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    # Ajouter les nouvelles données
    existing_data.append(new_data)

    # Écrire les données mises à jour dans le fichier JSON
    with open('command.json', "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

    messagebox.showinfo("command", f"You have commanded {number_asked} * {selected_line}.")

def recherche_buyer():
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
        title = Label(window, text="User Menu", font=police_title, bg="white")
        title.pack(pady=5)
        frame = Frame(window, bg="white")
        frame.pack(expand=YES)

        if cookie_username == '':
            opt1 = Button(frame, text="Log in", command=login, font=police)
            opt1.pack(fill=X, pady=5)

            opt2 = Button(frame, text="Register", command=register, font=police)
            opt2.pack(fill=X, pady=5)

        elif cookie_username != '':

            opt8 = Button(frame, text="Buyer menu", command=buyer_menu, font=police)
            opt8.pack(fill=X, pady=5)

            opt7 = Button(frame, text="Seller menu", command=main_menu, font=police)
            opt7.pack(fill=X, pady=5)

            opt3 = Button(frame, text="Account details", command=account_det, font=police)
            opt3.pack(fill=X, pady=5)

            opt4 = Button(frame, text="Modify account", command=user_modif, font=police)
            opt4.pack(fill=X, pady=5)

            opt6 = Button(frame, text="Log out", command=logout, font=police)
            opt6.pack(fill=X, pady=5)
 
            opt5 = Button(frame, text="Delete account", command=user_del, font=police)
            opt5.pack(fill=X, pady=5)

        if cookie_username == "Admin":
 
            opt9 = Button(frame, text="Check password", command=leaks_to_email, font=police)
            opt9.pack(fill=X, pady=5)

        window.mainloop()       

def register():
    clear()

    #Config Tkinter
    window.title("Register")
    window.config(background='white')
    window.minsize(300, 150)

    #Tkinter object's
    username_label = Label(window, text="Username", bg="white")
    username_label.pack()
    username = StringVar()
    username_entry = Entry(window, textvariable=username)
    username_entry.pack()

    password_label = Label(window, text="Password", bg="white")
    password_label.pack()
    password = StringVar()
    password_entry = Entry(window, textvariable=password, show='*')
    password_entry.pack()

    description_label = Label(window, text="Description", bg="white")
    description_label.pack()
    description = StringVar()
    description_entry = Entry(window, textvariable=description)
    description_entry.pack()

    mail_label = Label(window, text="Mail", bg="white")
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
    username_label = Label(window, text="Username", bg="white")
    username_label.pack()
    username = StringVar()
    username_entry = Entry(window, textvariable=username)
    username_entry.pack()

    password_label = Label(window, text="Password", bg="white")
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

    messagebox.showinfo("Your account", f"Account : {account}\n\nPassword's hash : {psword}\n\nDescription : {desc}\n\nEmail : {mail}", bg="white")

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
            rep = simpledialog.askstring("Username", "Enter your new username :")
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
            password = simpledialog.askstring("Password", "Enter your new password :")
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
            confirm = messagebox.askquestion("Confirmation", f"Your new password will be : {password}")
            if confirm == "yes":
                df.loc[df['USERNAME'] == cookie_username, 'PASSWORD'] = hashpassword
                df.loc[df['USERNAME'] == cookie_username, 'SALT'] = salt
                df.to_csv('users.csv', index=False, encoding='utf-8')

        def descr_modif():
            df = pd.read_csv('users.csv', encoding='utf-8')
            rep = simpledialog.askstring("Description", "Enter your new description :")
            confirm = messagebox.askquestion("confirmation", f"Your new description will be : {rep}")
            if confirm == "yes":
                df.loc[df['USERNAME'] == cookie_username, 'DESCRIPTION'] = rep
                df.to_csv('users.csv', index=False, encoding='utf-8')

        def email_modif():
            df = pd.read_csv('users.csv', encoding='utf-8')
            rep = simpledialog.askstring("Email", "Enter your new email :")
            confirm = messagebox.askquestion("confirmation", f"Your new email will be : {rep}")
            if confirm == "yes":
                df.loc[df['USERNAME'] == cookie_username, 'MAIL'] = rep
                df.to_csv('users.csv', index=False, encoding='utf-8')

        #Tkinter object
        frame = Frame(window, bg="white")
        frame.pack(expand=YES)

        title = Label(frame, text="User modification", font=police_title, bg="white")
        title.pack(fill=X, pady=5)

        opt3 = Button(frame, text="Username", command=username_modif, font=police)
        opt3.pack(fill=X, pady=5)

        opt4 = Button(frame, text="Password", command=password_modif, font=police)
        opt4.pack(fill=X, pady=5)
 
        opt5 = Button(frame, text="Description", command=descr_modif, font=police)
        opt5.pack(fill=X, pady=5)

        opt6 = Button(frame, text="Email", command=email_modif, font=police)
        opt6.pack(fill=X, pady=5)

        opt7 = Button(frame, text="Exit", command=user_menu, font=police)
        opt7.pack(fill=X, pady=5)

        window.mainloop()

def logout():
    global cookie_username
    messagebox.showinfo("logout", f"You have been log out of {cookie_username}.")
    cookie_username = ''
    user_menu()

def leaks_to_email():
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
    messagebox.showinfo("check", "Password check finish")

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
cookie_username = ''

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

try:
    with open("command.json", "r") as log_file:
        pass
except FileNotFoundError:
    with open("command.json", "w") as log_file:
        log_file.write("")

window = Tk()
police = font.Font(family="Arial", size=10)
police_title = font.Font(family="Arial", size=20)
user_menu()