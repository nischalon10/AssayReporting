import tkinter as tk
from tkinter import ttk
import create_tab
import update_tab
import database_tab
import data_handler

# Initialize the database
data_handler.initialize_database()

# Create the main application window
root = tk.Tk()
root.title("PDF Form Filler")

# Enable resizing of the main window
root.geometry("1200x600")  # Set initial size of the window
root.minsize(800, 400)  # Set minimum window size
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Create a tabbed interface using ttk.Notebook
notebook = ttk.Notebook(root)
notebook.grid(sticky="nsew", padx=10, pady=10)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Add the Create Tab
create_frame = ttk.Frame(notebook)
notebook.add(create_frame, text="Create")
create_tab.setup_create_tab(create_frame, notebook)

# Add the Update Tab
update_frame = ttk.Frame(notebook)
notebook.add(update_frame, text="Update Data")
update_tab.setup_update_tab(update_frame, notebook)

# Add the Database Tab
database_frame = ttk.Frame(notebook)
notebook.add(database_frame, text="Database")
database_tab.setup_database_tab(database_frame, notebook)
database_tab.on_application_exit(root)

# Run the application
root.mainloop()
