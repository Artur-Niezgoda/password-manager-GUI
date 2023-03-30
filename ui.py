"""
This module contains a GUI for a password manager that includes classes for managing and encrypting passwords.

Classes:

ManagerInterface: 
    This is the main interface for managing passwords. It has methods for searching, saving, generating, encrypting, and decrypting passwords.
NewEncryptionInterface: 
    This interface is used to set up a new encryption key and store it in a hashed file.
CheckEncryptionInterface: 
    This interface is used to check if an entered encryption key is the same as the one stored in the file.
Methods:

ManagerInterface.search_password(): 
    This method searches the data file to see if a password has already been stored for a given website.
ManagerInterface.save_password(): 
    This method saves a username/email and password for a given website to the data file.
ManagerInterface.generate_password(): 
    This method generates a random password using a combination of lowercase letters, uppercase letters, numbers, and symbols.
ManagerInterface.encrypt_data(): 
    This method encrypts the data in the data file using Fernet encryption from the cryptography module.
ManagerInterface.decrypt_data(): 
    This method decrypts the data in the data file using Fernet decryption from the cryptography module.
NewEncryptionInterface.encryption_key_setup(): 
    This method sets up a new encryption key by having the user enter a 32-character alphanumeric and symbol sequence, then hashes and stores it in a file.
CheckEncryptionInterface.encryption_key_check(): 
    This method checks if an entered encryption key is the same as the one stored in the hashed file.

Static Functions:

save_file(): 
    This function is used to save bytes to a file.
Constants:

BLACK: A color theme for the GUI.
LABEL_FONT: Font settings for labels.
ENTRY_FONT: Font settings for entry boxes.
LETTERS_LOWER: List of lowercase letters used to generate random passwords.
LETTERS_UPPER: List of uppercase letters used to generate random passwords.
NUMBERS: List of numbers used to generate random passwords.
SYMBOLS: List of symbols used to generate random passwords.
ENCRYPTION_REQUEST_TEXT: Text displayed in the NewEncryptionInterface window to prompt the user to enter an encryption key.
"""

class ManagerInterface(Tk):
    """ Class creating the main GUI for the password manager

    Attributes:
         authorization_key (string)
            key used for encryption
         'save_password' (function)
            function saving encrypted data to the file
    """

    def __init__(self):
        """
        Constructor of the ManagerInterface class
        """

        super().__init__()

        # Set initial values for instance variables
        self.authorization_key = ""

        # Set window title, size, and background color
        self.title("Password Manager")
        self.config(pady=20, padx=20, bg=BLACK)
        self.minsize(width=500, height=450)

        # Make a frame and having it fill the whole window using pack
        self.mainframe = Frame(self, bg=BLACK)
        self.mainframe.pack(fill="both", expand=True)

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
        # Try to open the file 'hashed_key.txt' for reading
            open('hashed_key.txt', mode='r')
        except FileNotFoundError:
        # If the file doesn't exist, prompt the user to create a new encryption key
            NewEncryptionInterface(self)
        else:
        # If the file does exist, prompt the user to enter the encryption key
            CheckEncryptionInterface(self)

        # Hide the main window
        self.withdraw()

        # Start the main event loop to display the GUI
        self.mainloop()

        # Save the password data to the file
        self.save_password()

    def search_password(self) -> None:
        """Check if there is a password saved for a given website

        This method gets the website name from the web_entry field in the GUI.
        It then reads from a file called "data.txt" in the current directory,
        and attempts to find the saved details for the given website. If found,
        it shows a message box displaying the saved username and password.
        If not found, it shows a message box saying no details have been saved.

        Returns:
            None
        """

        # Get website name from GUI entry field
        website = self.web_entry.get()

        try:
            # Read encrypted data from file
            with open("data.txt", "rb") as file:
                data = file.read()
        except FileNotFoundError:
            # Show message if file not found
            messagebox.showinfo(title="File not found", message="No Data File Found")
        else:
            # Decrypt the data
            data = self.decrypt_data(data)

            # Check if website is in the decrypted data
            if website.capitalize() in data:
                # Get the stored username and password
                user_name = data[website.capitalize()]["email"]
                stored_pass = data[website.capitalize()]["password"]

                # Show the username and password in a message box
                messagebox.showinfo(title=website, message=f"Username: {user_name} \n"
                                                           f"Password: {stored_pass} \n")
            else:
                # Show message if website not found in data
                messagebox.showinfo(title=website, message="There are no details for this Website yet")

        finally:
            # Clear the GUI entry field and delete the data variable
            self.web_entry.delete(0, END)
            del data

    def generate_password(self) -> None:
        """Generate a random password using letters, numbers and symbols

        This method generates a random password of length between 8 and 10, with
        2 to 4 symbols and 2 to 4 numbers included. It then shuffles the characters
        and shows the generated password in the password_entry field in the GUI.
        It also copies the password to the clipboard using pyperclip.

        Returns:
            None
        """

        # Generate a list of random characters for the password
        password_list = [choice(LETTERS_LOWER + LETTERS_UPPER) for _ in range(randint(8, 10))] + \
                        [choice(SYMBOLS) for _ in range(randint(2, 4))] + \
                        [choice(NUMBERS) for _ in range(randint(2, 4))]

        # Shuffle the characters and join them into a string
        shuffle(password_list)
        password = "".join(password_list)

        # Clear the password entry field in the GUI, insert the generated password, and copy to clipboard
        self.password_entry.delete(0, END)
        self.password_entry.insert(0, password)
        pyperclip.copy(password)

    def save_password(self) -> None:
        """
        Prepare dictionary containing the username and the password for a given website and save it to json file
        """
        website = self.web_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Create a new dictionary with website, email, and password and format it correctly for the JSON file
        new_data = {
            website.capitalize(): {
                "email": email.lower(),
                "password": password,
            }
        }

        # Check if any of the fields are empty, if so, show an error message
        if website == "" or email == "" or password == "":
            messagebox.showinfo(title="Empty Fields", message="One or more of the fields remain empty. Please fill all the fields")
        else:
            try:
                # Try to open the data file, and load the existing data
                with open("data.txt", "rb") as file:
                    # load old data
                    data = file.read()
                # Decrypt the existing data file
                data = self.decrypt_data(data)
            except FileNotFoundError:
                # If no existing data file found, encrypt the new data, save it to a new file, and create that file
                new_data = self.encrypt_data(new_data)
                save_file("data.txt", new_data)
            else:
                # If there is an existing data file, update the data with the new data and save it to the file
                data.update(new_data)
                data = self.encrypt_data(data)
                save_file("data.txt", data)
                # Delete the data object
                del data
            finally:
                # Clear all the fields after everything is done
                self.web_entry.delete(0, END)
                self.email_entry.delete(0, END)
                self.email_entry.insert(0, "example@email.com")
                self.password_entry.delete(0, END)

    def encrypt_data(self, data_file: dict) -> object:
        """
        Encrypt data using the authorization key
        :param data_file: json data
        :return: encrypted data as an object of Fernet class
        """
        # Convert the data_file dictionary into bytes and encrypt it using Fernet with the authorization key
        data_file = base64.b64encode(str(data_file).encode('utf-8'))
        data_file = Fernet(base64.b64encode(self.authorization_key)).encrypt(data_file)
        return data_file

    def decrypt_data(self, data_file: object) -> dict:
        """
        Decrypt given data
        :param data_file: an encrypted data as a Fernet class object
        :return: decrypted data as a JSON
        """
        # Decrypt the data_file object using Fernet with the authorization key, then convert it back to JSON format
        data_file = Fernet(base64.b64encode(self.authorization_key)).decrypt(data_file)
        data_file = base64.b64decode(data_file)
        data_file = data_file.decode("utf-8").replace("'", "\"")
        data_file = json.loads(data_file)
        return data_file

    
class NewEncryptionInterface:
    """
    Class that creates interface for setting up an encryption key if the user opens the program for the first time.

    Attributes:
        manager (object): object from main window class
    """
    def __init__(self, mng_interface: ManagerInterface):
        """
        Constructor of NewEncryptionInterface class. Creates the Toplevel object of the Tkinter class
        :param mng_interface: an object from main window class
        """
        # Assign attributes
        self.manager = mng_interface
        # Create a new Toplevel object
        self.top = Toplevel()
        # Configure the window
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
        """Check if the entered key matches the confirmatory key and check if the key is 32 bytes long.
        If it matches the criteria, hash the key and save it to a text file. Finally open the main window"""

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
    """Class that creates the interface to validate the access to the password manager

    Attributes:
        manager (object)
            object of the main window class
    """

    def __init__(self, mng_interface: ManagerInterface):
        """
        Constructor of the class
        :param mng_interface: object of the main window class
        """

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
        """Check if the encryption key entered by the user is correct by comparing it to a saved hashed key"""

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


def save_file(file_name: str, data_file: object) -> None:
    """
    Function that saves data to a file
    :param file_name: string containing name of the file to be saved
    :param data_file: object containing encrypted data
    """

    with open(f"{file_name}", "wb") as file:
        file.write(data_file)
