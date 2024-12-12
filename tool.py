import os
import pandas as pd
cookie_username = None

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
    with open('data.txt', encoding='utf-8') as f:
        data = f.read()
        datas = data.split('\n')
        print("==========================")
        for produit in datas:
            infos = produit.split(',')
            produit = infos[0]
            prix = infos[1]
            description = infos[2]
            print("Nom :", produit)
            print("Prix :", prix, "euro")
            print("Stock :", description)
            print("-------------------------")
        input("Enter to continue...")

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

def add():
    cls()
    with open('data.txt', 'a', encoding='utf-8') as f:
        name = input("Enter your new item name : ")
        price = int(input("Enter the price of the item : "))
        stock = int(input("Enter the number of items : "))
        f.write("\n" + name + ", " + str(price) + ", " + str(stock))
        print("-------------------------")

def supr():
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

def recherche():
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
            user_menu()
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
    cls()
    logo()
    username = input("Enter your username : ")
    cls()
    logo()
    password = input("Enter your password : ")
    cls()
    logo()
    description = input("Enter the description of this account : ")
    cls()
    logo()
    phone = input("Enter your phone number : ")
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
            print("Account saved successfully.")
            input("Press Enter to continue...")
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
        return

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
    print(f"User '{cookie_username}' has been successfully deleted.")
    input("Enter to continue...")

main_menu()