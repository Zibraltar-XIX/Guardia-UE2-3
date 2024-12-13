import os
import pandas as pd

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def logo():
    print(" __________________________________________________\n|                                                  |\n|     /$$$$$$$$                  /$$               |\n|    |__  $$__/                 | $$               |\n|       | $$  /$$$$$$   /$$$$$$ | $$  /$$$$$$$     |\n|       | $$ /$$__  $$ /$$__  $$| $$ /$$_____/     |\n|       | $$| $$  \ $$| $$  \ $$| $$|  $$$$$$      |\n|       | $$| $$  | $$| $$  | $$| $$ \____  $$     |\n|       | $$|  $$$$$$/|  $$$$$$/| $$ /$$$$$$$/     |\n|       |__/ \______/  \______/ |__/|_______/      |\n|                                                  |\n'=================================================='\n\n")

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
            lect_csv()
        elif x == 2:
            tri()
        elif x == 3:
            add_csv()
        elif x == 4:
            supr_csv()
        elif x == 5:
            recherche_csv()
        elif x == 6:
            user_menu()
        else:
            print("Invalid option. Please select a valid choice.")

def lect_csv():
    cls()
    logo()
    file_path = 'data.csv'
    df = pd.read_csv(file_path, encoding='utf-8')
    print("Aperçu des données :\n\n", df.head())
    input("\n\nEnter to continue...")

def tri():
    cls()
    with open('data.txt', encoding='utf-8') as f:
        lignes = f.readlines()

    objets = []
    for line in lignes:
        infos = line.strip().split(',')  # Supprimer les espaces et couper par virgules
        name = infos[0]
        price = int(infos[1])
        stock = int(infos[2])
        objets.append([name, price, stock])

    print("How do you want to sort the items?")
    print("1: By price")
    print("2: By stock")
    choice = input("Enter your choice (1 or 2): ")

    # Trier manuellement par prix
    if choice == "1":
        for i in range(len(objets)):
            for j in range(len(objets) - 1):
                if objets[j][1] > objets[j + 1][1]:  # Comparer les prix
                    objets[j], objets[j + 1] = objets[j + 1], objets[j]
    
    # Trier manuellement par stock
    elif choice == "2":
        for i in range(len(objets)):
            for j in range(len(objets) - 1):
                if objets[j][2] > objets[j + 1][2]:  # Comparer les stocks
                    objets[j], objets[j + 1] = objets[j + 1], objets[j]

    print("==========================")
    for item in objets:
        print(f"Name: {item[0]}")
        print(f"Price: {item[1]} euro")
        print(f"Stock: {item[2]}")
        print("--------------------------")

def add_csv():
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

def supr_csv():
    file_path = 'data.csv'
    df = pd.read_csv(file_path, encoding='utf-8')
    colonne = 'OBJECT'
    cls()
    logo()
    print("Aperçu des données :\n\n", df)
    x = int(input("\n\nEnter the number of the product you want to remove : "))
    product = df.iloc[x][colonne]
    df = df.drop(index=x)
    df.to_csv(file_path, index=False, encoding='utf-8')
    cls()
    logo()
    print(product,"has been successfully deleted.")
    input("\n\nEnter to continue...")

def recherche_csv():
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
    print("Product name : ", product, "\nPrice : ", price, "$\nStock : ", stock)
    input("\n\nEnter to continue")

def user_menu():
    while True:
        cls()
        logo()
        print("Press 1 to log in")
        print("Press 2 to register")
        print("Press 3 to view account details")
        print("Press 4 to modify account details")
        print("Press 5 to delete account")
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
        elif x == 6: #the best hidden option lol
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
    phone = ''

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
        password = input("Enter your password : ")

    while description == '':
        cls()
        logo()
        description = input("Enter the description of this account : ")
        if description == '':
            description = "Nothing here !"
        else :
            break
    
    while phone == '':
        cls()
        logo()
        phone = input("Enter your phone number : ")
        if phone == '':
            phone = "Nothing here !"
        else :
            break

    cls()
    logo()
    print("Résumé (a traduire) :\n")
    print("Username : ", username, "\nPassword : ", password, "\nDescription : ", description, "\nPhone number : ", phone)
    
    while True:
        entry = input("\nThis is correct ? (y/n/q) : ")
        if entry == "q":
            break

        elif entry == "y":
            file_path = 'users.csv'

            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except FileNotFoundError:
                df = pd.DataFrame(columns=['USERNAME', 'PASSWORD', 'DESCRIPTION', 'PHONE'])

            new_row = pd.DataFrame([{
                'USERNAME': username,
                'PASSWORD': password,
                'DESCRIPTION': description,
                'PHONE': phone
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
    cls()
    logo()

    if user_found.iloc[0]['PASSWORD'] == password:
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
        print("No account information found for the logged-in user.")
        input("\n\nEnter to continue...")
        return

    account = user_found.iloc[0]['USERNAME']
    psword = user_found.iloc[0]['PASSWORD']
    desc = user_found.iloc[0]['DESCRIPTION']
    phone = user_found.iloc[0]['PHONE']

    cls()
    logo()
    print(f"Account : {account}\nPassword : {psword}\nDescription : {desc}\nPhone number : {phone}")
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
    while True:
        cls()
        logo()
        print("Press 1 to modify username")
        print("Press 2 to modify password")
        print("Press 3 to modify description")
        print("Press 4 to modify phone number")
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
            jsp = "PASSWORD"
            phrase = "password : "
        elif x == 3:
            jsp = "DESCRIPTION"
            phrase = "description : "
        elif x == 4:
            jsp = "PHONE"
            phrase = "phone number : "
        else:
            print("Invalid option. Please select a valid choice.")

        modif = ''
        while modif == '':
            modif = input("Enter the new " + phrase)
            df.loc[df['USERNAME'] == cookie_username, jsp] = modif

        df.to_csv(file_path, index=False, encoding='utf-8')
        print("Password updated successfully!")

main_menu()