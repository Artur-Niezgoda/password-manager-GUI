from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json

BLACK = '#323131'
LABEL_FONT = ("Ariel", 11, "bold")
ENTRY_FONT = ("Ariel", 11)
LETTERS_LOWER = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()
LETTERS_UPPER = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
NUMBERS = '0 1 2 3 4 5 6 7 8 9'.split()
SYMBOLS = '! ? @ # : & * % $ ^'.split()

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def search_password():
    """Check if there is a password saved for a given website
    """

    website = web_entry.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="File not found", message="No Data File Found")
    else:
        if website.capitalize() in data:
            user_name = data[website.capitalize()]["email"]
            stored_pass = data[website.capitalize()]["password"]
            messagebox.showinfo(title=website, message=f"Username: {user_name} \n"
                                                       f"Password: {stored_pass} \n")
        else:
            messagebox.showinfo(title=website, message="No Details For The Website Exist")
    finally:
        web_entry.delete(0, END)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generate a random password using letters, numbers and symbols
    """

    password_list = [choice(LETTERS_LOWER + LETTERS_UPPER) for _ in range(randint(8, 10))] + \
                    [choice(SYMBOLS) for _ in range(randint(2, 4))] + \
                    [choice(NUMBERS) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_to_json(file_name: str, data_file: dict) -> None:
    """
    Open a json file in a write mode and save the data_file.

    :param file_name: name of the file with extension
    :param data_file: data saved as a dictionary
    """
    with open(f"{file_name}", "w") as file:
        # save data
        json.dump(data_file, file, indent=4)


def save_password() -> None:
    """
    Prepare dictionary containing the username and the password for a given website and save it to json file
    """

    website = web_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website.capitalize(): {
            "email": email.lower(),
            "password": password,
        }
    }
    if website == "" or email == "" or password == "":
        messagebox.showinfo(title="Empty Fields", message="One or more of the fields remain empty. Please fill all "
                                                          "the fields")
    else:
        try:
            with open("data.json", "r") as file:
                # load old data
                data = json.load(file)
        except FileNotFoundError:
            # save new data and create the file
            save_to_json("data.json", new_data)
        else:
            # update data with new data
            data.update(new_data)
            save_to_json("data.json", data)
        finally:
            web_entry.delete(0, END)
            email_entry.delete(0, END)
            email_entry.insert(0, "example@email.com")
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=20, padx=20, bg=BLACK)
window.minsize(width=500, height=450)

# Make a frame and having it fill the whole window using pack
mainframe = Frame(window,  bg=BLACK)
mainframe.pack(fill=BOTH, expand=1)

# Canvas with a logo
canvas = Canvas(mainframe, width=200, height=200, highlightthickness=0, bg=BLACK)
image_png = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image_png)
canvas.grid(row=0, column=1)

# Labels
web_label = Label(mainframe, text="Website:", font=LABEL_FONT, bg=BLACK, fg="white")
web_label.grid(row=1, column=0)
email_label = Label(mainframe, text="Email/Username:", font=LABEL_FONT, bg=BLACK, fg="white")
email_label.grid(row=2, column=0)
password_label = Label(mainframe, text="Password:", font=LABEL_FONT, bg=BLACK, fg="white")
password_label.grid(row=3, column=0)

# Entries
web_entry = Entry(mainframe, font=ENTRY_FONT)
web_entry.grid(row=1, column=1, sticky="EW", pady=(10, 10), padx=(0, 10))
web_entry.focus()
email_entry = Entry(mainframe, font=ENTRY_FONT)
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW", pady=(10, 10))
email_entry.insert(0, "example@email.com")
password_entry = Entry(mainframe, font=ENTRY_FONT)
password_entry.grid(row=3, column=1, sticky="EW", pady=(10, 10), padx=(0, 10))

# Buttons
button_gen_pass = Button(mainframe, text="Generate Password", command=generate_password)
button_gen_pass.grid(row=3, column=2, sticky="EW")
add_button = Button(mainframe, text="Add", width=35, command=save_password)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW", pady=(10, 10))
search_button = Button(mainframe, text="Search", command=search_password)
search_button.grid(row=1, column=2, sticky="EW")


# Add weights to the grid rows and columns
# Changing the weights will change the size of the rows/columns relative to each other
mainframe.grid_rowconfigure(0, weight=1)
mainframe.grid_rowconfigure(1, weight=1)
mainframe.grid_rowconfigure(2, weight=1)
mainframe.grid_rowconfigure(3, weight=1)
mainframe.grid_rowconfigure(4, weight=1)
mainframe.grid_columnconfigure(0, weight=1)
mainframe.grid_columnconfigure(1, weight=1)
mainframe.grid_columnconfigure(2, weight=1)

window.mainloop()
