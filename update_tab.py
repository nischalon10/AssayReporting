import tkinter as tk
from tkinter import filedialog, messagebox
import data_handler
import form_fields_validation  # Import the form fields validation module
from pdf_filler import fill_pdf_form
import os
import subprocess
import database_tab

def retrieve_data(entries):
    fa_number = entries['faNoField'].get()
    data = data_handler.get_form_data(fa_number)
    if not data:
        messagebox.showerror("Error", f"No data found for FA number: {fa_number}")
        return

    for key in entries:
        if key in data:
            entries[key].delete(0, tk.END)
            entries[key].insert(0, data[key])

def submit_form_update(entries, template_path, refresh_db_table):
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
    default_filename = f"{fa_number}_updated_template.pdf"
    output_path = filedialog.asksaveasfilename(
        initialfile=default_filename,
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Select destination for the updated PDF"
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

    # After successfully saving the PDF, update the data in the database
    success, message = data_handler.update_form_data(data)
    if not success:
        messagebox.showerror("Error", message)
        return

    # Confirmation message and option to open the file
    open_file = messagebox.askyesno(
        "PDF Saved",
        f"Updated PDF saved successfully at {output_path}.\n\nDo you want to open the file now?"
    )
    if open_file:
        open_pdf(output_path)

    # Refresh the database table after updating the record
    refresh_db_table()

def open_pdf(file_path):
    if os.path.isfile(file_path):
        if os.name == 'nt':
            os.startfile(file_path)
        elif os.name == 'posix':
            subprocess.run(['open', file_path] if os.uname().sysname == 'Darwin' else ['xdg-open', file_path])
    else:
        messagebox.showerror("Error", "File not found!")

def setup_update_tab(frame, notebook):
    entries = {}
    template_path = "./template.pdf"

    frame.grid_columnconfigure(1, weight=1)
    tk.Label(frame, text="FA No").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entries['faNoField'] = tk.Entry(frame)
    entries['faNoField'].grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    retrieve_button = tk.Button(frame, text="Retrieve", command=lambda: retrieve_data(entries))
    retrieve_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

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

    submit_button = tk.Button(frame, text="Update and Generate Report", command=lambda: submit_form_update(entries, template_path, lambda: database_tab.refresh_db_table(notebook)))
    submit_button.grid(row=8, column=1, columnspan=2, padx=10, pady=20, sticky="ew")
