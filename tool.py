import os

def main_menu():
    while True:
        print("Press 1 to view objects")
        print("Press 2 to add objects")
        print("Press 3 to delete objects")
        print("Press 4 to quit")
        
        try:
            x = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        if x == 1:
            os.system("start firefox")
        elif x == 2:
            os.system("start chrome")
        elif x == 3:
            os.system("start notepad")
        elif x == 4:
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid option. Please select a valid choice.")

def lect_donnee():
    try:
        with open('names.txt', encoding='utf-8') as f:
            names = f.read()
        print(names)
    except FileNotFoundError:
        print("Error: File 'names.txt' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

main_menu()
