import os
import pandas as pd
import hashlib
import secrets
import smtplib
from email.message import EmailMessage
import re

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
    if cookie_username == '':
        input("You are not log in.\n\nEnter to continue...")
        return
    file_path = 'data.csv'
    df = pd.read_csv(file_path, encoding='utf-8')
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
    cls()
    logo()
    if cookie_username == '':
        input("You are not log in.\n\nEnter to continue...")
        return
    file_path = 'data.csv'
    df = pd.read_csv(file_path, encoding='utf-8')
    print("How do you want to sort the items ?\n1: By price\n2: By stock")
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

    else :
        cls()
        logo()
        print("Bad choice !")
        input("\n\nEnter to continue...")

def add():
    if cookie_username == '':
        input("You are not log in.\n\nEnter to continue...")
        return
    #Load the csv
    file_path = 'data.csv'
    df = pd.read_csv(file_path, encoding='utf-8')

    #Empty value for the user
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

    while stock == '':
        cls()
        logo()
        stock = input("Enter the stock of this product : ")
        if stock == "0":
            stock = "Out of stock !"

    cls()
    logo()
    print("Résumé (a traduire) :\n")
    print("Product name : ", product, "\nPrice : ", price, "$\nStock : ", stock)
    
    while True:
        entry = input("\nThis is correct ? (y/n/q) : ")
        if entry == "q":
            break

        elif entry == "y":
            file_path = 'data.csv'

            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except FileNotFoundError:
                df = pd.DataFrame(columns=['OBJECT', 'PRICE', 'STOCK'])

            new_row = pd.DataFrame([{
                'OBJECT': product,
                'PRICE': price,
                'STOCK': stock,
                'OWNER': cookie_username,
            }])

            df = pd.concat([df, new_row], ignore_index=True)

            df.to_csv(file_path, index=False, encoding='utf-8')
            cls()
            logo()
            print("Product saved successfully.")
            input("\n\nPress Enter to continue...")
            break

        elif entry == "n":
            main_menu()
        else:
            print("Type y for yes, n for no and modify, or q to return to user menu.")


    cls()
    with open('data.txt', 'r', encoding='utf-8') as f:
        lignes = f.readlines()

    print("Current entries:")
    for i, line in enumerate(lignes, start=1):
        print(f"{i}: {line.strip()}")
    print("q : Return to main menu.")

    try:
        line_number = int(input("Enter the number of the line to delete: "))
        if 1 <= line_number <= len(lignes):
            # Supprimer la ligne choisie
            lignes.pop(line_number - 1)

            # Réécrire le fichier sans ligne vide à la fin
            with open('data.txt', 'w', encoding='utf-8') as f:
                # Réécrire les lignes en s'assurant que le dernier élément n'a pas de saut de ligne supplémentaire
                f.write('\n'.join(line.strip() for line in lignes))

            print("Line deleted successfully.")
            print("-------------------------")
        elif line_number == str("q"):
            main_menu()
        else:
            print("Invalid line number.")
            print("-------------------------")
    except ValueError:
        print("Please enter a valid number.")
        print("-------------------------")


    with open('data.txt', encoding='utf-8') as f:
        data = f.read()
        datas = data.split('\n')
        cls()
        search = str(input("Enter object name : "))
        for produit in datas:
            infos = produit.split(',')
            produit = infos[0]
            prix = infos[1]
            description = infos[2]
            if search == produit :
                print("Nom :", produit)
                print("Prix :", prix, "euro")
                print("Stock :", description)
                print("-------------------------")
        input("Enter to continue...")
        cls()

def supr():
    if cookie_username == '':
        input("You are not log in.\n\nEnter to continue...")
        return
    file_path = 'data.csv'
    df = pd.read_csv(file_path, encoding='utf-8')
    df = df[df['OWNER'] == cookie_username]
    colonne = 'OBJECT'
    cls()
    logo()
    print("Aperçu des données :\n\n", df)
    x = int(input("\n\nEnter the number of the product you want to remove : "))
    df = pd.read_csv(file_path, encoding='utf-8')
    product = df.iloc[x][colonne]
    df = df.drop(index=x)
    df.to_csv(file_path, index=False, encoding='utf-8')
    cls()
    logo()
    print(product,"has been successfully deleted.")
    input("\n\nEnter to continue...")

def recherche():
    if cookie_username == '':
        input("You are not log in.\n\nEnter to continue...")
        return
    cls()
    logo()
    file_path = 'data.csv'
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except Exception as e:
        print("Erreur lors du chargement du fichier CSV :", e)
        input("\n\nEnter to continue...")
        return
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
        print("Press 1 to log in")
        print("Press 2 to register")
        print("Press 3 to view account details")
        print("Press 4 to modify account details")
        print("Press 5 to delete account")
        print("Press 6 to log out")
        if cookie_username == "Admin":
            print("Press 7 to check password leaks for all users")
        if cookie_username == "Admin":
            print("Press 8 to list all users")
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
        elif x == 3:
            account_det()
        elif x == 4:
            user_modif()
        elif x == 5:
            user_del()
        elif x == 6:
            logout()
        elif x == 7 and cookie_username == "Admin":
            leaks_to_email()
        elif x == 8 and cookie_username == "Admin":
            list_user()
        else:
            print("Invalid option. Please select a valid choice.")

def list_user():
    cls()
    logo()
    database = pd.read_csv('users.csv')
    print(database)
    input("\n\nEnter to continue...")

def register():
    #Load the csv
    file_path = 'users.csv'
    df = pd.read_csv(file_path, encoding='utf-8')

    #Empty value for the user
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
        for i in range(nb_rows):
            verif = leaks.iloc[i]['PASSWORD']
            if verif == password:
                rep = input("The password is present on web leaks. Choose a better password, more info here :\nhttps://www.cisa.gov/secure-our-world/use-strong-passwords .\n\nDo you want to force this password ? (y or else) : ")
                if rep == "y":
                    password = password
                else :
                    password = ''
            else:
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
    print("Résumé (a traduire) :\n")
    print("Username : ", username, "\nPassword : ", password, "\nDescription : ", description, "\nEmail : ", mail)
    
    while True:
        entry = input("\nThis is correct ? (y/n/q) : ")
        if entry == "q":
            break

        elif entry == "y":
            file_path = 'users.csv'

            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except FileNotFoundError:
                df = pd.DataFrame(columns=['USERNAME', 'PASSWORD','SALT', 'DESCRIPTION', 'MAIL'])

            new_row = pd.DataFrame([{
                'USERNAME': username,
                'PASSWORD': hashpassword,
                'SALT' : salt,
                'DESCRIPTION': description,
                'MAIL': mail
            }])

            df = pd.concat([df, new_row], ignore_index=True)

            df.to_csv(file_path, index=False, encoding='utf-8')
            cls()
            logo()
            print("Account saved successfully.")
            input("\n\nPress Enter to continue...")
            break

        elif entry == "n":
            register()
        else:
            print("Type y for yes, n for no and modify, or q to return to user menu.")

def login():
    global cookie_username
    cls()
    logo()
    file_path = 'users.csv'
    username = input("Enter your username: ")
    cls()
    logo()    

    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except FileNotFoundError:
        print("User database not found!")
        return

    user_found = df[df['USERNAME'] == username]

    if user_found.empty:
        print("Username not found!")
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
    file_path = 'users.csv'
    
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except FileNotFoundError:
        print("User database not found!")
        return

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
    file_path = 'users.csv'
    df = pd.read_csv(file_path, encoding='utf-8')
    df = df[df['USERNAME'] != cookie_username]
    df.to_csv(file_path, index=False, encoding='utf-8')
    cls()
    logo()
    print(f"User '{cookie_username}' has been successfully deleted.")
    input("\n\nEnter to continue...")

def user_modif():
    file_path = 'users.csv'
    df = pd.read_csv(file_path, encoding='utf-8')
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
            jsp = "USERNAME"
            phrase = "username : "
        elif x == 2:
            cls()
            logo()
            password = input("Enter your password : ")
            salt = secrets.token_hex(16)
            password_salted = salt+password
            hashpassword = hashlib.sha512(password_salted.encode()).hexdigest()
            df.loc[df['USERNAME'] == cookie_username, 'PASSWORD'] = hashpassword
            df.loc[df['USERNAME'] == cookie_username, 'SALT'] = salt
            df.to_csv(file_path, index=False, encoding='utf-8')
            cls()
            logo()
            print("Account updated successfully!")
            input("\n\nEnter to continue...")
            break

        elif x == 3:
            jsp = "DESCRIPTION"
            phrase = "description : "
        elif x == 4:
            jsp = "MAIL"
            phrase = "Email : "
        else:
            print("Invalid option. Please select a valid choice.")

        modif = ''
        while modif == '':
            modif = input("Enter the new " + phrase)
            df.loc[df['USERNAME'] == cookie_username, jsp] = modif

        df.to_csv(file_path, index=False, encoding='utf-8')
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
    for i in range(users_rows):
        for j in range(leaks_rows):
            verif = leaks.iloc[j]['PASSWORD']
            password = users.iloc[i]['PASSWORD']
            email = users.iloc[i]['MAIL']
            user = users.iloc[i]['USERNAME']
            salt = users.iloc[i]['SALT']
            verif = salt+verif
            verif = hashlib.sha512(verif.encode()).hexdigest()
            if verif == password:
                # Configuration
                admin_email = 'contact@zibraltar.fr'
                email_password = 'z3qlPzjkqWh9IPVLjh821w'
                to_email = email
                subject = 'Security Alert'
                body = f"Hello {user},\nYour password has leaked on the internet!\nYou need to change it now."

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
    cls()
    logo()
    input("Password check finish, enter to continue...")

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

cookie_username = ''
main_menu()