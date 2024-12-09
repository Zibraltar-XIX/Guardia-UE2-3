def main_menu():
    while True:
        print("Press 1 to view objects")
        print("Press 2 to view objects with filters")
        print("Press 3 to add objects")
        print("Press 4 to delete objects")
        print("Press 5 to quit")
        
        try:
            x = int(input("Enter your choice: "))
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
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid option. Please select a valid choice.")

def lect1():
    try:
        with open('data.txt', encoding='utf-8') as f:
            names = f.read()
        print("=================================")
        print(names)
        print("=================================")
    except FileNotFoundError:
        print("Error: File 'names.txt' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def lect():
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

def tri():
    with open('data.txt', encoding='utf-8') as f:
        lines = f.readlines()  # Lire toutes les lignes du fichier

    # Transformer les données en une liste d'objets
    objets = []
    for line in lines:
        infos = line.strip().split(',')  # Supprimer les espaces et couper par virgules
        name = infos[0]
        price = int(infos[1])
        stock = int(infos[2])
        objets.append([name, price, stock])  # Ajouter sous forme de liste [nom, prix, stock]

    # Demander le critère de tri
    print("How do you want to sort the items?")
    print("1: By price")
    print("2: By stock")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        # Trier manuellement par prix
        for i in range(len(objets)):
            for j in range(len(objets) - 1):
                if objets[j][1] > objets[j + 1][1]:  # Comparer les prix
                    objets[j], objets[j + 1] = objets[j + 1], objets[j]
    elif choice == "2":
        # Trier manuellement par stock
        for i in range(len(objets)):
            for j in range(len(objets) - 1):
                if objets[j][2] > objets[j + 1][2]:  # Comparer les stocks
                    objets[j], objets[j + 1] = objets[j + 1], objets[j]

    # Afficher les objets triés
    print("==========================")
    for item in objets:
        print(f"Name: {item[0]}")
        print(f"Price: {item[1]} euro")
        print(f"Stock: {item[2]}")
        print("--------------------------")

def add():
    with open('data.txt', 'a', encoding='utf-8') as f:
        name = input("Enter your new item name : ")
        price = int(input("Enter the price of the item : "))
        stock = int(input("Enter the number of items : "))
        f.write("\n" + name + ", " + str(price) + ", " + str(stock))
        print("-------------------------")

def supr():
    with open('data.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Afficher les lignes pour aider l'utilisateur à choisir
    print("Current entries:")
    for i, line in enumerate(lines, start=1):
        print(f"{i}: {line.strip()}")

    # Demander à l'utilisateur quelle ligne supprimer
    try:
        line_number = int(input("Enter the number of the line to delete: "))
        if 1 <= line_number <= len(lines):
            # Supprimer la ligne choisie
            lines.pop(line_number - 1)

            # Réécrire le fichier sans ligne vide à la fin
            with open('data.txt', 'w', encoding='utf-8') as f:
                # Réécrire les lignes en s'assurant que le dernier élément n'a pas de saut de ligne supplémentaire
                f.write('\n'.join(line.strip() for line in lines))

            print("Line deleted successfully.")
            print("-------------------------")
        else:
            print("Invalid line number.")
            print("-------------------------")
    except ValueError:
        print("Please enter a valid number.")
        print("-------------------------")

main_menu()