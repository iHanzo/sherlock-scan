# Menu bar with Help section
menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=clear_fields)
file_menu.add_command(label="Reload", command=reload_script)
file_menu.add_command(label="Exit", command=root.destroy)

edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Edit Username List", command=edit_usernames)
edit_menu.add_command(label="Edit Password List", command=edit_passwords)
edit_menu.add_command(label="Edit Header List", command=edit_headers)
edit_menu.add_separator()  # Optional: Adds a separator line in the menu
edit_menu.add_command(label="Open Users Table", command=open_users_table)

help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Help", command=show_help)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Spray and Pray\nVersion 1.0"))

# Input Frame for URL, usernames, passwords, and headers
input_frame = Frame(root)
input_frame.grid(pady=10)

# URL entry
url_label = Label(input_frame, text="Target URL:")
url_label.grid(row=0, column=0, sticky=W)
url_entry = Entry(input_frame, width=70)
url_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=W)
url_entry.insert(0, default_url)

# Usernames file entry
usernames_label = Label(input_frame, text="Usernames File:")
usernames_label.grid(row=1, column=0, sticky=W)
usernames_entry = Entry(input_frame, width=50)
usernames_entry.grid(row=1, column=1, padx=5, pady=5)
usernames_entry.insert(0, default_usernames_path)
usernames_btn = Button(input_frame, text="Browse", command=lambda: select_file(usernames_entry))
usernames_btn.grid(row=1, column=2, padx=5, pady=5, sticky=W)

# Passwords file entry
passwords_label = Label(input_frame, text="Passwords File:")
passwords_label.grid(row=2, column=0, sticky=W)
passwords_entry = Entry(input_frame, width=50)
passwords_entry.grid(row=2, column=1, padx=5, pady=5)
passwords_entry.insert(0, default_passwords_path)
passwords_btn = Button(input_frame, text="Browse", command=lambda: select_file(passwords_entry))
passwords_btn.grid(row=2, column=2, padx=5, pady=5, sticky=W)

# Headers CSV file entry
headers_label = Label(input_frame, text="Headers CSV File:")
headers_label.grid(row=3, column=0, sticky=W)
headers_entry = Entry(input_frame, width=50)
headers_entry.grid(row=3, column=1, padx=5, pady=5)
headers_entry.insert(0, default_headers_path)
headers_btn = Button(input_frame, text="Browse", command=lambda: select_file(headers_entry))
headers_btn.grid(row=3, column=2, padx=5, pady=5, sticky=W)

# Control Frame for options and buttons
control_frame = Frame(root)
control_frame.grid(pady=5)

# Iteration mode selection
iteration_modes = [
    ("Stuffing", "stuffing_mode"),
    ("Random", "random_order"),
    ("Systematic", "systematic_order"),
]
mode_label = Label(control_frame, text="Iteration Mode", font="bold")
mode_label.grid(row=4, column=0, sticky=W, pady=(10, 0))
for i, (text, mode) in enumerate(iteration_modes, 5):
    Radiobutton(control_frame, text=text, variable=iteration_mode_var, value=mode).grid(row=i, column=0, sticky=W)

# Header customization mode selection
header_var = StringVar(value="same_for_all")
modes = [
    ("Uniform Headers for All Requests", "uniform_headers"),
    ("Random Headers for Each Request", "random_headers_each_request"),
    ("Randomize Each Header Value Individually", "randomize_each_header"),
    ("Unique Headers per Username", "unique_headers_per_username"),
]
mode_label = Label(control_frame, text="Header Customization Mode" , font="bold")
mode_label.grid(row=4, column=1, sticky=W, pady=(10, 0))
for i, (text, mode) in enumerate(modes, 5):
    Radiobutton(control_frame, text=text, variable=header_var, value=mode).grid(row=i, column=1, sticky=W)

# Minimum and maximum delay entry
delay_title_label = Label(control_frame, text='Attempt delay', font="bold")
delay_title_label.grid(row=4, column=2, columnspan=2, sticky=W)

min_delay_label = Label(control_frame, text="Min Delay (s):")
min_delay_label.grid(row=5, column=2, sticky=W)
min_delay_entry = Entry(control_frame, width=10)
min_delay_entry.grid(row=6, column=2, sticky=W)
min_delay_entry.insert(0, default_delay)

max_delay_label = Label(control_frame, text="Max Delay (s):")
max_delay_label.grid(row=7, column=2, sticky=W)
max_delay_entry = Entry(control_frame, width=10)
max_delay_entry.grid(row=8, column=2, sticky=W)
max_delay_entry.insert(0, default_delay)

# Start button
start_button = Button(control_frame, text="Start", command=on_start)
start_button.grid(row=9, column=1, pady=5, padx=50, sticky=W+E)

# Cancel button
cancel_button = Button(control_frame, text="Cancel", command=cancel_run)
cancel_button.grid(row=10, column=1, pady=5, padx=50, sticky=W+E)

# Create the progress bar in your GUI setup
progress = ttk.Progressbar(root, orient=HORIZONTAL, length=800, mode='determinate')
progress.grid(row=11, column=0, columnspan=3, pady=10)

