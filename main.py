from tkinter import *

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# ---------------------------- SAVE PASSWORD ------------------------------- #

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=20, padx=20)
window.minsize(width=500, height=350)

# Make a frame and having it fill the whole root window using pack
mainframe = Frame(window)
mainframe.pack(fill=BOTH, expand=1)

canvas = Canvas(mainframe, width=200, height=200)
image_png = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image_png)
canvas.grid(row=0, column=1)

# Labels
web_label = Label(mainframe, text="Website:")
web_label.grid(row=1, column=0)
email_label = Label(mainframe, text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(mainframe, text="Password:")
password_label.grid(row=3, column=0)

# Entries
web_entry = Entry(mainframe)
web_entry.grid(row=1, column=1, columnspan=2, sticky="EW")
email_entry = Entry(mainframe)
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
password_entry = Entry(mainframe)
password_entry.grid(row=3, column=1, sticky="EW")

# Buttons
button_gen_pass = Button(mainframe, text="Generate Password")
button_gen_pass.grid(row=3, column=2, sticky="EW")
add_button = Button(mainframe, text="Add", width=35)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

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
