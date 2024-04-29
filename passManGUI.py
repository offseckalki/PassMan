import tkinter as tk
from tkinter import messagebox
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

        c.execute('''SELECT userpass FROM users WHERE username = ?''', (username,))
        result = c.fetchone()
        if result is None:
            messagebox.showerror("Login Failed", "Username not found.")
            return

        stored_password = result[0]

        if hashed_password != stored_password:
            messagebox.showerror("Login Failed", "Incorrect password.")
        else:
            messagebox.showinfo("Login Successful", "Welcome!")
            login_window.destroy()

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

def main():
    root = tk.Tk()
    root.title("Password Manager")

    tk.Button(root, text="Sign Up", command=signup).pack(pady=20)
    tk.Button(root, text="Login", command=login).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
