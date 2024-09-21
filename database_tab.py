import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import data_handler
import os
import pandas as pd
import subprocess

# Global variable to store the temporary file path
temp_file_path = None

# Function to refresh the database table in the Treeview
def refresh_db_table(treeview):
    for row in treeview.get_children():
        treeview.delete(row)
    records = data_handler.get_all_records()
    for index, record in enumerate(records):
        # Exclude the ID column when inserting values
        display_record = record[1:]  # Skip the first element (ID)
        if index % 2 == 0:
            treeview.insert('', tk.END, values=display_record, tags=('evenrow',))
        else:
            treeview.insert('', tk.END, values=display_record, tags=('oddrow',))

# Function to open the database in Excel
def open_in_excel(treeview):
    global temp_file_path  # Use global variable to track the temp file path
    records = [treeview.item(row)["values"] for row in treeview.get_children()]
    if not records:
        messagebox.showinfo("No Data", "No data available to open in Excel.")
        return

    columns = ["FA No", "Date", "Customer Name", "Sample Type",
               "Sample Weight", "Fineness %", "Fineness Parts", "Other Info"]

    df = pd.DataFrame(records, columns=columns)

    # Create a specific folder for temporary files
    temp_folder = "temp_files"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # Create a unique filename for the CSV file
    temp_file_path = os.path.join(temp_folder, "database_export.csv")
    df.to_csv(temp_file_path, index=False)

    # Open the CSV file in Excel
    try:
        os.startfile(temp_file_path)  # For Windows
    except AttributeError:
        subprocess.run(['open', temp_file_path])  # For MacOS
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Excel: {str(e)}")

# Function to save the database table as a CSV file at user-specified location
def save_as_csv(treeview):
    records = [treeview.item(row)["values"] for row in treeview.get_children()]
    if not records:
        messagebox.showinfo("No Data", "No data available to save as CSV.")
        return

    columns = ["FA No", "Date", "Customer Name", "Sample Type",
               "Sample Weight", "Fineness %", "Fineness Parts", "Other Info"]

    df = pd.DataFrame(records, columns=columns)

    # Ask user where to save the CSV file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save as CSV",
        initialfile="database_export.csv"
    )
    if file_path:
        try:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", f"Data saved successfully as {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV: {str(e)}")

# Function to delete the temporary file on application exit
def delete_temp_file():
    global temp_file_path
    if temp_file_path and os.path.exists(temp_file_path):
        os.remove(temp_file_path)
        print(f"Temporary file {temp_file_path} deleted.")

# Function to set up the database tab UI
def setup_database_tab(frame, notebook):
    # Create a Treeview widget to display the database records without the "ID" column
    treeview = ttk.Treeview(frame, columns=("FA No", "Date", "Customer Name", "Sample Type",
                                            "Sample Weight", "Fineness %", "Fineness Parts", "Other Info"), show="headings")

    # Define a style for the Treeview headers
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'), background="lightblue")

    # Configure column headings
    headings = ["FA No", "Date", "Customer Name", "Sample Type",
                "Sample Weight", "Fineness %", "Fineness Parts", "Other Info"]

    # Set headers with bold font and background color
    for col in headings:
        treeview.heading(col, text=col, anchor='center')

    # Enable column resizing in the database table
    for col in treeview["columns"]:
        treeview.column(col, width=100, anchor="center", stretch=True)

    # Alternate row colors
    treeview.tag_configure('oddrow', background='lightgray')
    treeview.tag_configure('evenrow', background='white')

    # Add vertical scrollbar to the database table
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)
    treeview.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    treeview.pack(fill="both", expand=True)

    # Add buttons for refreshing, opening in Excel, and saving as CSV
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=10)

    refresh_button = tk.Button(button_frame, text="Refresh Database", command=lambda: refresh_db_table(treeview))
    refresh_button.pack(side="left", padx=10)

    excel_button = tk.Button(button_frame, text="Open in Excel", command=lambda: open_in_excel(treeview))
    excel_button.pack(side="left", padx=10)

    save_csv_button = tk.Button(button_frame, text="Save as CSV", command=lambda: save_as_csv(treeview))
    save_csv_button.pack(side="left", padx=10)

    # Populate the database table initially
    refresh_db_table(treeview)

    # Register the table refresh function in notebook for other tabs to use
    notebook.refresh_db_table = lambda: refresh_db_table(treeview)

# Function to set up application exit handler
def on_application_exit(root):
    root.protocol("WM_DELETE_WINDOW", lambda: [delete_temp_file(), root.destroy()])
