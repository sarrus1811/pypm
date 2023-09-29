from tkinter import *
from tkinter import messagebox
from random import shuffle
from secrets import choice, randbelow
from json import dump, load
import string
import os
import pyperclip

# Necessary for proper image path in Windows
path = os.path.join(os.path.dirname(__file__), "logo.png")

# Generate password
def generate_password():
    password_entry.delete(0, END)
    password_letters = [choice(string.ascii_letters) for _ in range(randbelow(3) + 8)]
    password_symbols = [choice(string.punctuation) for _ in range(randbelow(3) + 1)]
    password_numbers = [choice(string.digits) for _ in range(randbelow(3) + 1)]
    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# Store password
def save_password():
    website = website_entry.get().lower()
    email = email_entry.get()
    password = password_entry.get()

    new_account = {website: {"email": email, "password": password}}

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(
            title="Empty field", message="Ensure all fields are filled!"
        )
    else:
        password_OK = messagebox.askokcancel(
            title=website,
            message=f"The entered login:\nWebsite:\t\t{website}\nEmail:\t\t{email}\nPassword:\t{password}\nSave the details?",
        )

        if password_OK:
            
            try:
                with open("data.json", "r") as data_file:
                    data = load(data_file)
                     
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    dump(new_account, data_file, indent=4) 
            
            else:
                data.update(new_account)
                with open("data.json", "w") as data_file:
                    dump(data, data_file, indent=4)
            
            finally:
                website_entry.delete(0, END)
                email_entry.delete(0, END)
                password_entry.delete(0, END)
                
        else:
            password_entry.delete(0, END)

#Find password
def find_password():
    website = website_entry.get().lower()
    if len(website) == 0:
        messagebox.showinfo(
            title="Empty field", message="Website name needed!"
        )
    else:
        try:
            with open("data.json", 'r') as data_file:
                data = load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No password file found!")
        else:
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title="Login found", message=f"{website.capitalize()}\nEmail: {email}\nPassword: {password}\nPassword copied to clipboard.")
                pyperclip.copy(password)
            else:
                messagebox.showinfo(title="Error", message=f"No logins found for {website}")

# UI
window = Tk()
window.title("Password Manager")
window.config(padx=30, pady=30, bg="#f7f5dd")

canvas = Canvas(width=200, height=200, bg="#f7f5dd", highlightthickness=0)
logo_img = PhotoImage(file=path)
canvas.create_image(108, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:", bg="#f7f5dd")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:", bg="#f7f5dd")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:", bg="#f7f5dd")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=25)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=25)
email_entry.grid(row=2, column=1)
password_entry = Entry(width=25)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search",width=16, command=find_password)
search_button.grid(row=1, column=2)
generate_button = Button(text="Generate password", width=16, command=generate_password)
generate_button.grid(row=3, column=2)
add_button = Button(text="Add", width=21, command=save_password)
add_button.grid(row=4, column=1)

window.mainloop()

# Image credit: Smashicons
