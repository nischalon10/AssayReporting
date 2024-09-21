import tkinter as tk
from tkinter import filedialog, messagebox
import data_handler
import form_fields_validation  # Import the form fields validation module
from pdf_filler import fill_pdf_form
import os
import subprocess
import database_tab

def prefill_fa_number(entry):
    fa_number = data_handler.generate_fa_number()
    entry.config(state=tk.NORMAL)
    entry.delete(0, tk.END)
    entry.insert(0, fa_number)
    entry.config(state=tk.DISABLED)

def submit_form_create(entries, template_path, refresh_db_table):
    data = {
        'faNoField': entries['faNoField'].get(),
        'customerNameField': entries['customerNameField'].get(),
        'sampleTypeField': entries['sampleTypeField'].get(),
        'sampleWeightField': entries['sampleWeightField'].get(),
        'finenessPercentField': entries['finenessPercentField'].get(),
        'finenessPartsField': entries['finenessPartsField'].get(),
        'otherInfoField': entries['otherInfoField'].get()
    }

    # Validate form data
    is_valid, message = form_fields_validation.validate_all_fields(data)
    if not is_valid:
        messagebox.showerror("Validation Error", message)
        return

    # Ask user for the save location with FA number as prefix
    fa_number = data['faNoField']
    default_filename = f"{fa_number}_filled_template.pdf"
    output_path = filedialog.asksaveasfilename(
        initialfile=default_filename,
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Select destination for the filled PDF"
    )

    # If the user cancels the save dialog, do nothing
    if not output_path:
        messagebox.showwarning("Cancelled", "File save location not selected.")
        return

    # Try to save the PDF file
    try:
        fill_pdf_form(template_path, output_path, data)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save PDF: {str(e)}")
        return

    # After successfully saving the PDF, save data to the database
    success, message = data_handler.process_form_data(data)
    if not success:
        messagebox.showerror("Error", message)
        return

    # Clear the form fields after successful save and generate a new FA number
    clear_form_create(entries)
    
    # Confirmation message and option to open the file
    open_file = messagebox.askyesno(
        "PDF Saved",
        f"PDF saved successfully at {output_path}.\n\nDo you want to open the file now?"
    )
    if open_file:
        open_pdf(output_path)
    
    # Refresh the database table
    refresh_db_table()

def clear_form_create(entries):
    for entry in entries.values():
        if entry['state'] == tk.NORMAL:
            entry.delete(0, tk.END)
    prefill_fa_number(entries['faNoField'])

def open_pdf(file_path):
    if os.path.isfile(file_path):
        if os.name == 'nt':
            os.startfile(file_path)
        elif os.name == 'posix':
            subprocess.run(['open', file_path] if os.uname().sysname == 'Darwin' else ['xdg-open', file_path])
    else:
        messagebox.showerror("Error", "File not found!")

def setup_create_tab(frame, notebook):
    entries = {}
    template_path = "./template.pdf"

    frame.grid_columnconfigure(1, weight=1)
    tk.Label(frame, text="FA No").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entries['faNoField'] = tk.Entry(frame, state=tk.DISABLED)
    entries['faNoField'].grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    labels_and_fields = [
        ("Customer Name", 'customerNameField'),
        ("Sample Type", 'sampleTypeField'),
        ("Sample Weight", 'sampleWeightField'),
        ("Fineness %", 'finenessPercentField'),
        ("Fineness Parts", 'finenessPartsField'),
        ("Other Information", 'otherInfoField')
    ]

    for i, (label_text, field_name) in enumerate(labels_and_fields, start=1):
        tk.Label(frame, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entries[field_name] = tk.Entry(frame)
        entries[field_name].grid(row=i, column=1, padx=10, pady=5, sticky="ew")

    submit_button = tk.Button(frame, text="Submit and Generate Report", command=lambda: submit_form_create(entries, template_path, lambda: database_tab.refresh_db_table(notebook)))
    submit_button.grid(row=7, column=1, padx=10, pady=20, sticky="ew")

    clear_button = tk.Button(frame, text="Clear", command=lambda: clear_form_create(entries))
    clear_button.grid(row=7, column=0, padx=10, pady=20, sticky="ew")

    prefill_fa_number(entries['faNoField'])
