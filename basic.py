import getpass
from cryptography.fernet import Fernet
import sqlite3
import hashlib

conn = sqlite3.connect('passwords.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                userpass TEXT NOT NULL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                serv TEXT NOT NULL,
                password TEXT ,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''')
conn.commit()

def signup():
    username=input("Enter Username to Continue\n")
    userpass = getpass.getpass(prompt="Enter Your Password Sir!\n") 
    userpass2 = getpass.getpass(prompt="Confirm Your Password Sir!\n") 
    if userpass != userpass2:
        print("Password MisMatch!\n Try again")
        signup()
    else:
        print("Welcome to THE PASSWORD MANAGER\n Now login as a User")
        hashed_password = hashlib.sha256(userpass.encode()).hexdigest()
        create_user(username, hashed_password)

def create_user(username, hashed_password):
    """Create a new user with a hashed password."""
    c.execute('''INSERT INTO users (username, userpass)
                 VALUES (?, ?)''', (username, hashed_password))
    conn.commit()

def login():
    username= input ("Enter Username to Continue\n")
    userpass = getpass.getpass(prompt="Enter Your Password Sir!\n")
    hashed_password = hashlib.sha256(userpass.encode()).hexdigest()

    c.execute('''SELECT userpass FROM users WHERE username = ?''', (username,))
    result = c.fetchone()
    if result is None:
        print("Username not found.")
        return False
    stored_password = result[0]

    if hashed_password != stored_password:
        print("wrong Password")
    else:
        print("Login Succsessful")
        return True

def store_password(serv, encrypted_password,user_id):
    
    
    # Store in SQLite database with associated service and hint
    c.execute('''INSERT INTO passwords (serv, password,user_id)
                 VALUES (?, ?, ?)''', (serv, encrypted_password,user_id))
    conn.commit()

key = Fernet.generate_key()
cipher_suite = Fernet(key)

def password():
    user_id = input("Enter Username for Service: ")
    pass1 = getpass.getpass("Enter Your Password Sir!\n")
    pass2 = getpass.getpass("Confirm Your Password Sir\n")
    
    if pass1 != pass2:
        print("Password Mismatch! Try again.")
        password()
    else:
        serv = input("Enter the name of Service (e.g., Gmail, Facebook): ")
        encrypted_password = cipher_suite.encrypt(pass1.encode())
        store_password(serv, encrypted_password, user_id)

def get_password():
    serv = input("Enter Service: ")
    c.execute('''SELECT password FROM passwords WHERE serv = ?''', (serv,))
    result = c.fetchone()
    
    if result is None:
        print("Service not found.")
        return 
    
    stored_password = result[0]
    try:
        decrypted_password = cipher_suite.decrypt(stored_password).decode()
        print("Password found successfully:", decrypted_password)
    except Exception as e:
        print("Error decrypting password:", e)

def main():
    while True:
        print("\nWelcome to Password Manager!")
        print("1. Sign-Up as New User!")
        print("2. Use Crediantials to login as Existing User!")
        print("3. Exit")
        choice = input("Enter your choice (1-2): ")
            
        if choice == '1':
            signup()

        elif choice == '2':
            if login():
                    while True:
                        print("\nWelcome to Password Manager!")
                        print("1. Save your password!")
                        print("2. View Your Password")
                        print("3. Exit")
                        
                        choice = input("Enter your choice (1-2): ")
                        
                        if choice == '1':
                            password()
                        elif choice == '2':
                            get_password()
                        elif choice == '3':
                            print("Thank you for using Password Manager. Goodbye!")
                            break
                        else:
                            print("Invalid choice. Please select a valid option.")

        

        elif choice == '3':
                print("Thank you for using Password Manager. Goodbye!")
                break
        else:
                print("Invalid choice. Please select a valid option.")
            

if __name__ == "__main__":
    main()