import tkinter as tk
import os
import subprocess
import sys
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from clustering import run_clustering



def new_scan():
    # Clear entry fields
    eps_entry.delete(0, tk.END)
    eps_entry.insert(0, "1.0")
    min_samples_entry.delete(0, tk.END)
    min_samples_entry.insert(0, "3")

    # Clear clustering information output
    cluster_info_tree.delete(*cluster_info_tree.get_children())
    processing_info_label.config(text="")

def refresh():
    # Restart the application
    python = sys.executable
    os.execl(python, python, *sys.argv)

def open_help_window():
    help_text = """EPSILON (EPS):
- The maximum distance between two samples for them to be considered as in the same neighborhood.
- Larger EPSILON values allow for larger gaps between points in the same cluster.

MIN_SAMPLES:
- The number of samples in a neighborhood for a point to be considered as a core point.
- Larger MIN_SAMPLES values require more points to form a dense region.

SUCCESS THRESHOLD:
- The minimum success rate required for a cluster to be considered normal or non-anomalous.
- Clusters with a success rate (successful attempts / total attempts) below this threshold will be flagged as suspicious or anomalous.
- Adjusting this threshold allows for customizing what constitutes a normal or non-anomalous cluster based on the ratio of successful attempts to total attempts.
  
DBSCAN CLUSTERING:
- DBSCAN (Density-Based Spatial Clustering of Applications with Noise) is a clustering algorithm that groups together points that are closely packed, and marks points that lie alone in low-density regions as outliers.
- It defines clusters as continuous regions of high density separated by regions of low density."""
    
    help_window = tk.Toplevel(root)
    help_window.title("Help")
    help_window.geometry("400x300+{}+{}".format(root.winfo_x() + 50, root.winfo_y() + 50))  # Position relative to main window
    
    help_text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, width=50, height=20)
    help_text_widget.insert(tk.END, help_text)
    help_text_widget.pack(fill="both", expand=True, padx=10, pady=10)

def show_about():
    messagebox.showinfo("About", "Sherlock Scan\nVersion 1.0\n\nDeveloped by Istvan Hanzo")

def run_clustering_command():
    eps_value = float(eps_entry.get())
    min_samples_value = int(min_samples_entry.get())
    success_threshold = float(success_threshold_entry.get())  # Retrieve success threshold value
    cluster_counts, processing_time_seconds, rows_processed, flag = run_clustering(eps_value, min_samples_value, success_threshold)

    # Display clustering information
    cluster_info_tree.delete(*cluster_info_tree.get_children())  # Clear existing data
    for cluster_label in cluster_counts.index:
        attempts = cluster_counts.loc[cluster_label, "Attempts"]
        successful = cluster_counts.loc[cluster_label, "Successful"]
        flag_value = successful / attempts < success_threshold if attempts > 0 else False
        cluster_info_tree.insert('', 'end', values=(cluster_label, attempts, successful, flag_value))

    # Format processing information and performance data
    processing_info = f"Processed: {rows_processed} rows\nProcessing time: {processing_time_seconds:.2f} seconds\nRows/Second: {rows_processed / processing_time_seconds:.2f}"

    # Update the label text
    processing_info_label.config(text=processing_info)
    
def open_last_log():
    log_folder = "scan_logs"
    if not os.path.exists(log_folder):
        messagebox.showinfo("Info", "No log files found.")
        return

    log_files = os.listdir(log_folder)
    if not log_files:
        messagebox.showinfo("Info", "No log files found.")
        return

    # Sort log files based on filename timestamps
    sorted_log_files = sorted(log_files, reverse=True)

    latest_log_file = sorted_log_files[0]

    os_name = os.name
    if os_name == 'nt':  # Windows
        os.startfile(os.path.join(log_folder, latest_log_file))
    elif os_name == 'posix':  # Linux
        subprocess.Popen(["xdg-open", os.path.join(log_folder, latest_log_file)])

def open_log_folder():
    log_folder = "scan_logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    os_name = os.name
    if os_name == 'nt':  # Windows
        subprocess.Popen(["explorer", log_folder])
    elif os_name == 'posix':  # Linux
        subprocess.Popen(["xdg-open", log_folder])

root = tk.Tk()
root.title("Sherlock Scan")

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create File menu
file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)

# Define commands with keyboard shortcuts
root.bind("<Control-n>", lambda event: new_scan())
root.bind("<Control-r>", lambda event: refresh())
root.bind("<Control-q>", lambda event: root.quit())

# Add commands to File menu with keyboard shortcuts
file_menu.add_command(label="New Scan", command=new_scan, accelerator="Ctrl+N")
file_menu.add_command(label="Refresh", command=refresh, accelerator="Ctrl+R")
file_menu.add_command(label="Exit", command=root.quit, accelerator="Ctrl+Q")

# Configure root window to handle keyboard shortcuts
root.bind_all("<Control-n>", lambda event: new_scan())
root.bind_all("<Control-r>", lambda event: refresh())
root.bind_all("<Control-q>", lambda event: root.quit())

# Create Help menu
help_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Help", command=open_help_window)
help_menu.add_command(label="About", command=show_about)

# Create frame for input fields
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

# Add entry fields for epsilon, min_samples, and success threshold
epsilon_label = ttk.Label(input_frame, text="Epsilon:")
epsilon_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
eps_entry = ttk.Entry(input_frame)
eps_entry.insert(0, "1.0")  # Default value
eps_entry.grid(row=0, column=1, padx=5, pady=5)

min_samples_label = ttk.Label(input_frame, text="Min Samples:")
min_samples_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
min_samples_entry = ttk.Entry(input_frame)
min_samples_entry.insert(0, "3")  # Default value
min_samples_entry.grid(row=1, column=1, padx=5, pady=5)

success_threshold_label = ttk.Label(input_frame, text="Success Threshold:")
success_threshold_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
success_threshold_entry = ttk.Entry(input_frame)
success_threshold_entry.insert(0, "0.5")  # Default value
success_threshold_entry.grid(row=2, column=1, padx=5, pady=5)

# Add button to run clustering
run_button = ttk.Button(input_frame, text="Run Clustering", command=run_clustering_command)
run_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Create frame for output
output_frame = ttk.Frame(root)
output_frame.pack(pady=10)

# Add treeview to display clustering information
cluster_info_tree = ttk.Treeview(output_frame, columns=("Cluster Label", "Attempts", "Successful", "Flag"), show="headings")

# Configure column headings
for column in ("Cluster Label", "Attempts", "Successful", "Flag"):
    cluster_info_tree.heading(column, text=column)

# Adjust column widths
for column, width in zip(("Cluster Label", "Attempts", "Successful", "Flag"), (120, 100, 100, 75)):
    cluster_info_tree.column(column, width=width)

# Configure border style
ttk.Style().configure("Treeview", borderwidth=2, relief="solid")

cluster_info_tree.pack(side="top", fill="both", expand=True)

# Add scrollbar for the treeview
tree_scroll = ttk.Scrollbar(output_frame, orient="vertical", command=cluster_info_tree.yview)
tree_scroll.pack(side="right", fill="y")
cluster_info_tree.configure(yscrollcommand=tree_scroll.set)

# Add label to display processing information
processing_info_label = ttk.Label(output_frame, text="")
processing_info_label.pack(pady=(5, 0), padx=10, anchor='w')

# Add button to open last log file
last_log_button = ttk.Button(root, text="Last Log", command=open_last_log)
last_log_button.pack(side="right", padx=5, pady=5)

# Add button to open log folder
log_folder_button = ttk.Button(root, text="Log Folder", command=open_log_folder)
log_folder_button.pack(side="right", padx=5, pady=5)

root.mainloop()
