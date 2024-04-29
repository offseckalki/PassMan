import tkinter as tk
from tkinter import messagebox, simpledialog
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
                password TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''')
conn.commit()

key = Fernet.generate_key()
cipher_suite = Fernet(key)

def signup():
    def register_user():
        username = username_entry.get()
        userpass = password_entry.get()
        userpass2 = confirm_entry.get()
        
        if userpass != userpass2:
            messagebox.showerror("Password Mismatch", "Passwords do not match. Please try again.")
            return
        
        hashed_password = hashlib.sha256(userpass.encode()).hexdigest()
        
        c.execute('''INSERT INTO users (username, userpass) VALUES (?, ?)''', (username, hashed_password))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully.")
        register_window.destroy()
    
    register_window = tk.Tk()
    register_window.title("Sign Up")

    tk.Label(register_window, text="Username:").pack()
    username_entry = tk.Entry(register_window)
    username_entry.pack()

    tk.Label(register_window, text="Password:").pack()
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack()

    tk.Label(register_window, text="Confirm Password:").pack()
    confirm_entry = tk.Entry(register_window, show="*")
    confirm_entry.pack()

    tk.Button(register_window, text="Register", command=register_user).pack()

    register_window.mainloop()

def login():
    def authenticate_user():
        username = username_entry.get()
        userpass = password_entry.get()
        hashed_password = hashlib.sha256(userpass.encode()).hexdigest()

        c.execute('''SELECT id, userpass FROM users WHERE username = ?''', (username,))
        result = c.fetchone()
        if result is None:
            messagebox.showerror("Login Failed", "Username not found.")
            return

        user_id, stored_password = result
        if hashed_password != stored_password:
            messagebox.showerror("Login Failed", "Incorrect password.")
        else:
            messagebox.showinfo("Login Successful", "Welcome!")
            login_window.destroy()
            open_password_manager(user_id)

    login_window = tk.Tk()
    login_window.title("Login")

    tk.Label(login_window, text="Username:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    tk.Button(login_window, text="Login", command=authenticate_user).pack()

    login_window.mainloop()

def open_password_manager(user_id):
    def save_password():
        service = simpledialog.askstring("Service Name", "Enter the service name (e.g., Gmail, Facebook):")
        password = simpledialog.askstring("Password", "Enter the password for this service:")
        encrypted_password = cipher_suite.encrypt(password.encode()).decode()
        
        c.execute('''INSERT INTO passwords (user_id, serv, password) VALUES (?, ?, ?)''', (user_id, service, encrypted_password))
        conn.commit()
        messagebox.showinfo("Success", "Password saved successfully.")

    def retrieve_password():
        service = simpledialog.askstring("Service Name", "Enter the service name to retrieve password:")
    
        c.execute('''SELECT password FROM passwords WHERE user_id = ? AND serv = ?''', (user_id, service))
        result = c.fetchone()
        if result:
            encrypted_password = result[0]
            try:
                decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
                messagebox.showinfo("Password", f"Password for {service}: {decrypted_password}")
            except Exception as e:
                messagebox.showerror("Error", f"Error decrypting password: {e}")
        else:
            messagebox.showerror("Error", f"No password found for {service}.")


    password_manager_window = tk.Tk()
    password_manager_window.title("Password Manager")

    tk.Button(password_manager_window, text="Save Password", command=save_password).pack(pady=20)
    tk.Button(password_manager_window, text="Retrieve Password", command=retrieve_password).pack(pady=20)

    password_manager_window.mainloop()

def main():
    root = tk.Tk()
    root.title("Password Manager")

    tk.Button(root, text="Sign Up", command=signup).pack(pady=20)
    tk.Button(root, text="Login", command=login).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
