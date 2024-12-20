import os
import pandas as pd
import hashlib
import secrets
import smtplib
from email.message import EmailMessage
import re
from pwned import pwned
from pwned import pwned_description

#Tools
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def logo():
    print(" __________________________________________________\n|                                                  |\n|     /$$$$$$$$                  /$$               |\n|    |__  $$__/                 | $$               |\n|       | $$  /$$$$$$   /$$$$$$ | $$  /$$$$$$$     |\n|       | $$ /$$__  $$ /$$__  $$| $$ /$$_____/     |\n|       | $$| $$  \ $$| $$  \ $$| $$|  $$$$$$      |\n|       | $$| $$  | $$| $$  | $$| $$ \____  $$     |\n|       | $$|  $$$$$$/|  $$$$$$/| $$ /$$$$$$$/     |\n|       |__/ \______/  \______/ |__/|_______/      |\n|                                                  |\n'=================================================='\n\n")

#Main menu
def main_menu():
    while True:
        cls()
        logo()
        print("Press 1 to view objects")
        print("Press 2 to view objects with filters")
        print("Press 3 to add objects")
        print("Press 4 to delete objects")
        print("Press 5 to find objects")
        print("Press 6 to access user's menu")
        print("Press q to quit")

        x = input("\nEnter your choice: ")

        if x == "q":
            print("Exiting the menu. Goodbye!")
            break
        try:
            x = int(x)
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        if x == 1:
            lect()
        elif x == 2:
            tri()
        elif x == 3:
            add()
        elif x == 4:
            supr()
        elif x == 5:
            recherche()
        elif x == 6:
            user_menu()
        else:
            print("Invalid option. Please select a valid choice.")

def lect(): 
    cls()
    logo()
    df = pd.read_csv('data.csv', encoding='utf-8')
    data_len = len(df)
    for i in range(data_len):
        if df.iloc[i]['OWNER'] == cookie_username:
            product = df.iloc[i]['OBJECT']
            price = df.iloc[i]['PRICE']
            stock = df.iloc[i]['STOCK']
            print(f"\nProduct : {product}\nPrice : {price}\nStock : {stock}")
            print("\n=======================================")

    input("\n\nEnter to continue...")

def tri():
    while choice == "":
        cls()
        logo()
        df = pd.read_csv('data.csv', encoding='utf-8')
        print("How do you want to sort the items ?\n1: By price\n2: By stock\nExit : q")
        choice = input("\n\nEnter your choice (1 or 2): ")

        if choice == "1":
            df = df[df['OWNER'] == cookie_username]
            df = df.sort_values(by='PRICE', ascending=True)
            cls()
            logo()
            print("Données triées par prix :\n\n", df)
            input("\n\nEnter to continue...")

        elif choice == "2":
            df = df[df['OWNER'] == cookie_username]
            df = df.sort_values(by='STOCK', ascending=True)
            cls()
            logo()
            print("Données triées par prix :\n\n", df)
            input("\n\nEnter to continue...")
    
        elif choice == "q":
            break

        else :
            cls()
            logo()
            print("Bad choice !")
            input("\n\nEnter to continue...")
            choice == ""

def add():
    df = pd.read_csv('data.csv', encoding='utf-8')
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
            print("Type y for yes, n for no and modify, or q to return to user menu.")

def supr():
    df = pd.read_csv('data.csv', encoding='utf-8')
    df = df[df['OWNER'] == cookie_username]
    colonne = 'OBJECT'
    cls()
    logo()
    print("Aperçu des données :\n\n", df)
    x = int(input("\n\nEnter the number of the product you want to remove : "))
    df = pd.read_csv('data.csv', encoding='utf-8')
    product = df.iloc[x][colonne]
    df = df.drop(index=x)
    df.to_csv('data.csv', index=False, encoding='utf-8')
    cls()
    logo()
    print(product,"has been successfully deleted.")
    input("\n\nEnter to continue...")

def recherche():
    cls()
    logo()
    df = pd.read_csv('data.csv', encoding='utf-8')
    search = input("Enter the product name : ")
    object_found = df[df['OBJECT'] == search]
    if object_found.empty:
        cls()
        logo()
        input("Product not found, sorry.\n\nEnter to continue...")
        return
    cls()
    logo()
    product = object_found.iloc[0]['OBJECT']
    price = object_found.iloc[0]['PRICE']
    stock = object_found.iloc[0]['STOCK']
    owner = object_found.iloc[0]['OWNER']
    if owner != cookie_username:
        input("Product not found, sorry.\n\nEnter to continue...")
        return
    print("Product name : ", product, "\nPrice : ", price, "$\nStock : ", stock)
    input("\n\nEnter to continue")

#User menu
def user_menu():
    while True:
        cls()
        logo()
        if cookie_username == '':
            print("Press 1 to log in")
            print("Press 2 to register")
        elif cookie_username != '':
            print("Press 3 to view account details")
            print("Press 4 to modify account details")
            print("Press 5 to delete account")
            print("Press 6 to log out")
            print("Press 7 to go to costumer menu")
        if cookie_username == "Admin":
            print("Press 8 to check password leaks for all users")
            print("Press 9 to list all users")
        print("Press q to quit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "q":
            cls()
            print("Exiting the menu...")
            break
        
        try:
            x = int(choice)
        except ValueError:
            print("Invalid input! Please enter a number or 'q' to quit.")
            continue

        if x == 1:
            login()
        elif x == 2:
            register()
        elif x == 3 and cookie_username != '':
            account_det()
        elif x == 4 and cookie_username != '':
            user_modif()
        elif x == 5 and cookie_username != '':
            user_del()
        elif x == 6 and cookie_username != '':
            logout()
        elif x == 7 and cookie_username != '':
            main_menu()
        elif x == 8 and cookie_username == "Admin":
            leaks_to_email()
        elif x == 9 and cookie_username == "Admin":
            list_user()
        else:
            print("Invalid option. Please select a valid choice.")

def list_user():
    cls()
    logo()
    database = pd.read_csv('users.csv')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(database)
    input("\n\nEnter to continue...")

def register():
    df = pd.read_csv('users.csv', encoding='utf-8')
    username = ''
    password = ''
    description = ''
    mail = ''

    while username == '':
        cls()
        logo()
        username = input("Enter your username : ")
        verif = df[df['USERNAME'] == username]
        if verif.empty:
            username = username
        else :
            input("Username already exist, sorry.\n\nEnter to try an other one...")
            username = ''

    while password == '':
        cls()
        logo()
        leaks = pd.read_csv('leaks.csv', encoding='utf-8')
        nb_rows = len(leaks)
        password = input("Enter your password : ")
        check = "ok"

        for i in range(nb_rows):
            verif = leaks.iloc[i]['PASSWORD']
            if verif == password:
                check = "leak"

        if check == "leak" or pwned(password):
            pwned_description(password) 
            rep = input("\nThe password is present on web leaks. Choose a better password, more info here :\nhttps://www.cisa.gov/secure-our-world/use-strong-passwords .\n\nDo you want to force this password ? (y or else) : ")
            if rep == "y":
                password = password
            else :
                password = ''
        if password != '':
            salt = secrets.token_hex(16)
            password_salted = salt+password
            hashpassword = hashlib.sha512(password_salted.encode()).hexdigest()

    while description == '':
        cls()
        logo()
        description = input("Enter the description of this account : ")
        if description == '':
            description = "Nothing here !"
        else :
            break
    
    while mail == '':
        cls()
        logo()
        mail = input("Enter your email : ").strip()
        if mail == '':
            cls()
            logo()
            input("You need enter a valid email.\n\nEnter to try again...")
        if not is_valid_email(mail):
            cls()
            logo()
            mail = ''
            input("You need to enter a valid email.\n\nPress Enter to try again...")

    cls()
    logo()
    print("Summary :\n")
    print("Username : ", username, "\nPassword : ", password, "\nDescription : ", description, "\nEmail : ", mail)
    
    while True:
        entry = input("\nThis is correct ? (y/n/q) : ")
        if entry == "q":
            break

        elif entry == "y":
            df = pd.read_csv('users.csv', encoding='utf-8')
            new_row = pd.DataFrame([{
                'USERNAME': username,
                'PASSWORD': hashpassword,
                'SALT' : salt,
                'DESCRIPTION': description,
                'MAIL': mail
            }])

            df = pd.concat([df, new_row], ignore_index=True)

            df.to_csv('users.csv', index=False, encoding='utf-8')
            cls()
            logo()
            print("Account saved successfully.")
            input("\n\nPress Enter to continue...")
            if rep == "y":
                cls()
                logo()
                print("Please, wait a few seconde.")
                email_send(mail, username)
            break

        elif entry == "n":
            register()
        else:
            print("Type y for yes, n for no and modify, or q to return to user menu.")

def login():
    global cookie_username
    cls()
    logo()
    username = input("Enter your username: ")
    cls()
    logo()    
    df = pd.read_csv('users.csv', encoding='utf-8')
    user_found = df[df['USERNAME'] == username]

    if user_found.empty:
        input("Username not found!\n\nEnter to continue...")
        return

    password = input("Enter your password: ")
    salt = user_found.iloc[0]['SALT']
    password_salted = salt+password
    hashpassword = hashlib.sha512(password_salted.encode()).hexdigest()
    cls()
    logo()

    if user_found.iloc[0]['PASSWORD'] == hashpassword:
        cookie_username = username
        print("Login successful!")
        input("\n\nPress Enter to continue...")
    else:
        print("Incorrect password!")
        input("Enter to continue...")

def account_det():    
    df = pd.read_csv('users.csv', encoding='utf-8')
    user_found = df[df['USERNAME'] == cookie_username]

    if user_found.empty:
        cls()
        logo()
        print("You are not log in.")
        input("\n\nEnter to continue...")
        return

    account = user_found.iloc[0]['USERNAME']
    psword = user_found.iloc[0]['PASSWORD']
    desc = user_found.iloc[0]['DESCRIPTION']
    mail = user_found.iloc[0]['MAIL']

    cls()
    logo()
    print(f"Account : {account}\nPassword's hash : {psword}\nDescription : {desc}\nEmail : {mail}")
    input("\n\nPress Enter to continue...")

def user_del():
    df = pd.read_csv('users.csv', encoding='utf-8')
    df = df[df['USERNAME'] != cookie_username]
    df.to_csv('users.csv', index=False, encoding='utf-8')
    cls()
    logo()
    print(f"User '{cookie_username}' has been successfully deleted.")
    cookie_username = ''
    input("\n\nEnter to continue...")

def user_modif():
    df = pd.read_csv('users.csv', encoding='utf-8')
    if cookie_username == '':
        cls()
        logo()
        print("You are not log in.")
        input("\n\nEnter to continue...")
        return
    
    while True:
        cls()
        logo()
        print("Press 1 to modify username")
        print("Press 2 to modify password")
        print("Press 3 to modify description")
        print("Press 4 to modify email")
        print("Press q to quit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "q":
            break
        
        try:
            x = int(choice)
        except ValueError:
            print("Invalid input! Please enter a number or 'q' to quit.")
            continue

        if x == 1:
            select = "USERNAME"
            phrase = "username : "
        elif x == 2:
            cls()
            logo()
            password = ''
            while password == '':
                cls()
                logo()
                leaks = pd.read_csv('leaks.csv', encoding='utf-8')
                nb_rows = len(leaks)
                password = input("Enter your password : ")
                check = "ok"

                for i in range(nb_rows):
                    verif = leaks.iloc[i]['PASSWORD']
                    if verif == password:
                        check = "leak"

                if check == "leak" or pwned(password):
                    pwned_description(password) 
                    rep = input("\nThe password is present on web leaks. Choose a better password, more info here :\nhttps://www.cisa.gov/secure-our-world/use-strong-passwords .\n\nDo you want to force this password ? (y or else) : ")
                    if rep == "y":
                        password = password
                    else :
                        password = ''
                if password != '':
                    salt = secrets.token_hex(16)
                    password_salted = salt+password
                    hashpassword = hashlib.sha512(password_salted.encode()).hexdigest()

            salt = secrets.token_hex(16)
            password_salted = salt+password
            hashpassword = hashlib.sha512(password_salted.encode()).hexdigest()
            df.loc[df['USERNAME'] == cookie_username, 'PASSWORD'] = hashpassword
            df.loc[df['USERNAME'] == cookie_username, 'SALT'] = salt
            df.to_csv('users.csv', index=False, encoding='utf-8')
            cls()
            logo()
            print("Account updated successfully!")
            input("\n\nEnter to continue...")
            break

        elif x == 3:
            select = "DESCRIPTION"
            phrase = "description : "
        elif x == 4:
            select = "MAIL"
            phrase = "Email : "
        else:
            print("Invalid option. Please select a valid choice.")

        modif = ''
        while modif == '':
            modif = input("Enter the new " + phrase)
            df.loc[df['USERNAME'] == cookie_username, select] = modif

        df.to_csv('users.csv', index=False, encoding='utf-8')
        print("Account updated successfully!")

def logout():
    cls()
    logo()
    global cookie_username
    input(f"You have been log out of {cookie_username}.\n\nEnter to continue...")
    cookie_username = ''

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


user_menu()