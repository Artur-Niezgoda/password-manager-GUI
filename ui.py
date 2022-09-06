from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
from cryptography.fernet import Fernet
import bcrypt
import pyperclip
import json
import base64


BLACK = '#323131'
LABEL_FONT = ("Ariel", 11, "bold")
ENTRY_FONT = ("Ariel", 11)
LETTERS_LOWER = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()
LETTERS_UPPER = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
NUMBERS = '0 1 2 3 4 5 6 7 8 9'.split()
SYMBOLS = '! ? @ # : & * % $ ^'.split()
ENCRYPTION_REQUEST_TEXT = "Please set up an encryption key to protect your passwords. Please enter exactly " \
                          "32 alphanumeric characters and simple symbols. The key should be easy to remember, " \
                          "for example, use a sequence of random words." \



class ManagerInterface(Tk):

    def __init__(self):

        super().__init__()
        self.authorization_key = ""
        self.title("Password Manager")
        self.config(pady=20, padx=20, bg=BLACK)
        self.minsize(width=500, height=450)

        # Make a frame and having it fill the whole window using pack
        self.mainframe = Frame(self,  bg=BLACK)
        self.mainframe.pack(fill=BOTH, expand=1)

        # Canvas with a logo
        self.canvas = Canvas(self.mainframe, width=200, height=200, highlightthickness=0, bg=BLACK)
        image_png = PhotoImage(file="logo.png")
        self.canvas.create_image(100, 100, image=image_png)
        self.canvas.grid(row=0, column=1)

        # Labels
        self.web_label = Label(self.mainframe, text="Website:", font=LABEL_FONT, bg=BLACK, fg="white")
        self.web_label.grid(row=1, column=0)

        self.email_label = Label(self.mainframe, text="Email/Username:", font=LABEL_FONT, bg=BLACK, fg="white")
        self.email_label.grid(row=2, column=0)

        self.password_label = Label(self.mainframe, text="Password:", font=LABEL_FONT, bg=BLACK, fg="white")
        self.password_label.grid(row=3, column=0)

        # Entries
        self.web_entry = Entry(self.mainframe, font=ENTRY_FONT)
        self.web_entry.grid(row=1, column=1, sticky="EW", pady=(10, 10), padx=(0, 10))
        self.web_entry.focus()

        self.email_entry = Entry(self.mainframe, font=ENTRY_FONT)
        self.email_entry.grid(row=2, column=1, columnspan=2, sticky="EW", pady=(10, 10))
        self.email_entry.insert(0, "example@email.com")

        self.password_entry = Entry(self.mainframe, font=ENTRY_FONT)
        self.password_entry.grid(row=3, column=1, sticky="EW", pady=(10, 10), padx=(0, 10))

        # Buttons
        self.button_gen_pass = Button(self.mainframe, text="Generate Password", command=self.generate_password)
        self.button_gen_pass.grid(row=3, column=2, sticky="EW")

        self.add_button = Button(self.mainframe, text="Add", width=35, command=self.save_password)
        self.add_button.grid(row=4, column=1, columnspan=2, sticky="EW", pady=(10, 10))

        self.search_button = Button(self.mainframe, text="Search", command=self.search_password)
        self.search_button.grid(row=1, column=2, sticky="EW")

        # Add weights to the grid rows and columns
        # Changing the weights will change the size of the rows/columns relative to each other
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_rowconfigure(1, weight=1)
        self.mainframe.grid_rowconfigure(2, weight=1)
        self.mainframe.grid_rowconfigure(3, weight=1)
        self.mainframe.grid_rowconfigure(4, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(1, weight=1)
        self.mainframe.grid_columnconfigure(2, weight=1)

        try:
            with open('hashed_key.txt', mode='r') as file:
                 contents = file.read()
        except FileNotFoundError:
            NewEncryptionInterface(self)
        else:
            CheckEncryptionInterface(self)

        self.withdraw()
        self.mainloop()
        self.save_password()

    def search_password(self):
        """Check if there is a password saved for a given website
        """

        website = self.web_entry.get()
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
                messagebox.showinfo(title=website, message="There are no details for this Website yet")
        finally:
            self.web_entry.delete(0, END)

    def generate_password(self) -> None:
        """Generate a random password using letters, numbers and symbols
        """

        password_list = [choice(LETTERS_LOWER + LETTERS_UPPER) for _ in range(randint(8, 10))] + \
                        [choice(SYMBOLS) for _ in range(randint(2, 4))] + \
                        [choice(NUMBERS) for _ in range(randint(2, 4))]

        shuffle(password_list)
        password = "".join(password_list)

        self.password_entry.delete(0, END)
        self.password_entry.insert(0, password)
        pyperclip.copy(password)
    # ---------------------------- SAVE PASSWORD ------------------------------- #

    def save_password(self) -> None:
        """
        Prepare dictionary containing the username and the password for a given website and save it to json file
        """

        website = self.web_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
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
                self.web_entry.delete(0, END)
                self.email_entry.delete(0, END)
                self.email_entry.insert(0, "example@email.com")
                self.password_entry.delete(0, END)


class NewEncryptionInterface:

    def __init__(self, mng_interface: ManagerInterface):

        self.manager = mng_interface
        self.top = Toplevel()
        self.top.title("Encryption Key")
        self.top.config(padx=40, pady=20, bg=BLACK)

        # Logo
        self.top_canvas = Canvas(self.top, height=200, width=200, highlightthickness=0, bg=BLACK)
        logo_image = PhotoImage(file="logo.png")
        self.top_canvas.create_image(100, 100, image=logo_image)
        self.top_canvas.image = logo_image  # added this reference to prevent garbage image collection bug
        self.top_canvas.grid(column=0, row=0)

        # Request text
        self.request_canvas = Canvas(self.top, height=100, width=450, highlightthickness=0, bg=BLACK)
        self.request_canvas.create_text(
            225,
            50,
            text=ENCRYPTION_REQUEST_TEXT,
            justify="center",
            font=LABEL_FONT,
            width=430,
            fill="white")
        self.request_canvas.grid(row=2, column=0, pady=(0, 10))

        # Various labels
        self.welcome_label = Label(self.top,
                                   text="Welcome to the Password Manager!",
                                   font=LABEL_FONT,
                                   bg=BLACK,
                                   justify="center",
                                   fg="white")
        self.welcome_label.grid(row=1, column=0, pady=(0, 10))

        self.warning_label = Label(self.top,
                                   text="Please remember! If you lose your key it is not possible to recover it.",
                                   font=LABEL_FONT,
                                   bg=BLACK,
                                   justify='center',
                                   fg="white")
        self.warning_label.grid(row=3, column=0, pady=(0, 10))

        self.confirmation_label = Label(self.top, text="Please re-confirm key:", font=LABEL_FONT, bg=BLACK, fg="white")
        self.confirmation_label.grid(row=5, column=0, pady=(0, 10))

        # Encryption key inputs
        self.password_input = Entry(self.top, font=ENTRY_FONT, show='●')
        self.password_input.grid(row=4, column=0, pady=(0, 10), ipadx=40)

        self.confirmation_input = Entry(self.top, font=ENTRY_FONT, show='●')
        self.confirmation_input.grid(row=6, column=0, pady=(0, 10), ipadx=40)

        # Enter button
        self.enter_button = Button(self.top, font=ENTRY_FONT, text='Enter',
                                   command=self.encryption_key_setup)
        self.enter_button.grid(row=7, column=0, pady=(0, 10))

    def encryption_key_setup(self):
        """Function for setting up an encryption key the first time the user opens the program.
        Checks that the two key entered matches the confirmatory key and checks that the key 32 bytes long.
        Finally, if the key meets the criteria, it is hashed and saved to a text file and the main window is opened
        Takes the two keys entered by the user."""
        key_1 = self.password_input.get().encode('utf-8')
        key_2 = self.confirmation_input.get().encode('utf-8')

        # Check if the two keys entered by the user match and return an error if they don't
        if key_1 != key_2:
            messagebox.showerror(title='Non-matching keys',
                                 message='The two encryption keys entered do not match. Please enter matching keys.')

        # Check if the entered key is 32 bytes long and raise error if it is not
        elif len(key_1) != 32:
            messagebox.showerror(title="Key length error",
                                 message="The encryption key entered is not 32 bytes long. "
                                         "Please enter a key comprising 32 alphanumeric characters and simple symbols")

        # If the two keys match and are the right length then we will save a hash of the key and open main window
        else:
            hashed_key = bcrypt.hashpw(password=key_1, salt=bcrypt.gensalt())  # Create hashed key
            hashed_key = hashed_key.decode('utf-8')
            with open('hashed_key.txt', mode='w') as key_file:
                key_file.write(hashed_key)

            self.manager.authorization_key = key_1
            # Close the key entry window and open the main window
            self.top.destroy()
            self.manager.deiconify()


class CheckEncryptionInterface:

    def __init__(self, mng_interface: ManagerInterface):

        self.manager = mng_interface
        self.top = Toplevel()
        self.top.title("Encryption Key")
        self.top.config(padx=40, pady=20, bg=BLACK)

        # Logo
        self.top_canvas = Canvas(self.top, height=200, width=200, highlightthickness=0, bg=BLACK)
        logo_image = PhotoImage(file="logo.png")
        self.top_canvas.create_image(100, 100, image=logo_image)
        self.top_canvas.image = logo_image  # added this reference to prevent garbage image collection bug
        self.top_canvas.grid(column=0, row=0)

        self.welcome_label = Label(self.top,
                                   text="Welcome to the Password Manager!",
                                   font=LABEL_FONT,
                                   bg=BLACK,
                                   justify="center",
                                   fg="white")
        self.welcome_label.grid(row=1, column=0, pady=(0, 10))

        self.key_label = Label(self.top, text="Please enter encryption key", font=LABEL_FONT, bg=BLACK, fg="white")
        self.key_label.grid(row=2, column=0, pady=(0, 10))

        self.password_input = Entry(self.top, font=ENTRY_FONT, show='●')
        self.password_input.grid(row=3, column=0, pady=(0, 10), ipadx=40)

        self.login_button = Button(self.top, font=LABEL_FONT, text='Log in',
                                   command=self.encryption_key_check)
        self.login_button.grid(row=4, column=0)

    def encryption_key_check(self):
        """Checks that the user entered encryption key is correct by comparing to a saved hashed key.
        Takes the key entered by the user as an argument."""

        key_1 = self.password_input.get().encode('utf-8')
        with open('hashed_key.txt', mode='r') as key_file:
            hashed_key = key_file.read()
            hashed_key = hashed_key.encode('utf-8')

        # Check if the key matches the saved key and if correct then open the main window
        if bcrypt.checkpw(key_1, hashed_key):
            self.manager.authorization_key = key_1
            self.top.destroy()
            self.manager.deiconify()
        # If key is incorrect then raise error
        else:
            messagebox.showerror(title='Incorrect key', message='The encryption key entered is incorrect. '
                                                                'Please try again.')

def save_to_json(file_name: str, data_file: dict) -> None:
    """
    Open a json file in a write mode and save the data_file.

    :param file_name: name of the file with extension
    :param data_file: data saved as a dictionary
    """
    with open(f"{file_name}", "w") as file:
        # save data
        json.dump(data_file, file, indent=4)
