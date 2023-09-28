from tkinter import *
from tkinter import messagebox
from random import shuffle
from secrets import choice, randbelow
import string
import os
import pyperclip


# Necessary for proper image path in Windows
absolute_path = os.path.dirname(__file__)
relative_path = "logo.png"
full_path = os.path.join(absolute_path, relative_path)


# Generate password
def generate_password():
    password_entry.delete(0, END)
    password_letters = [choice(string.ascii_letters) for _ in range(randbelow(3)+8)] 
    password_symbols = [choice(string.punctuation) for _ in range(randbelow(3)+1)]
    password_numbers = [choice(string.digits) for _ in range(randbelow(3)+1)]
    password_list = password_letters+password_numbers+password_symbols
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# Store password
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

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
            with open("data.txt", "a") as data_file:
                data_file.write(
                    f"-----------------------------------------------------------------------------------------\n"
                )
                data_file.write(f"Website: \t{website}\n")
                data_file.write(f"Username: \t{email}\n")
                data_file.write(f"Password: \t{password}\n")
                website_entry.delete(0, END)
                email_entry.delete(0, END)
                password_entry.delete(0, END)
        else:
            password_entry.delete(0, END)


#UI

window = Tk()
window.title("Password manager/Generator")
window.config(padx=30, pady=30, bg="#f7f5dd")

canvas = Canvas(width=200, height=200, bg="#f7f5dd", highlightthickness=0)
logo_img = PhotoImage(file=full_path)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:", bg="#f7f5dd")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:", bg="#f7f5dd")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:", bg="#f7f5dd")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=35)
# email_entry.insert(END, "someemail@somemail.com")
email_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=22)
password_entry.grid(row=3, column=1)

# Buttons
generate_password = Button(text="--Generate--", command=generate_password)
generate_password.grid(row=3, column=2)
add_button = Button(text="Add", width=21, command=save_password)
add_button.grid(row=4, column=1)


window.mainloop()

# Password image credit: Smashicons