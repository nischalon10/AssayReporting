# PDF Form Filler Application

This application is designed to fill out PDF forms based on user input. It includes functionality to manage form entries, update existing entries, and export data to CSV or open it directly in Excel.

## Features

- **Create PDF Forms**: Fill out a new PDF form based on user input.
- **Update Forms**: Retrieve and update existing form data in the database.
- **Database Management**: View, export, and manipulate data stored in the SQLite database.
- **Export to CSV**: Save database entries as a CSV file.

## Requirements

Ensure you have the following packages installed:

- `tkinter` (Standard Python library for GUI applications)
- `pdfrw` (For PDF reading and writing)
- `pandas` (For handling CSV exports and data manipulation)
- `pyinstaller` (For creating a standalone executable)

To install all necessary dependencies, run:

```bash
pip install -r requirements.txt
```

## How to Run the Application

1. **Clone the Repository**:
   Clone the repository or download the source code files.

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Ensure `template.pdf` is Present**:
   Place the `template.pdf` file in the same directory as `main.py`. This file is necessary for the application to generate filled PDF forms.

3. **Run the Application**:
   Run the application directly using Python:

   ```bash
   python main.py
   ```

4. **Creating an Executable**:
   If you want to compile the application into a single executable:

   **For Windows**:

   ```bash
   pyinstaller --onefile --noconsole --add-data "template.pdf;." main.py
   ```

   **For macOS/Linux**:

   ```bash
   pyinstaller --onefile --windowed --add-data "template.pdf:." main.py
   ```

   This will create an executable in the `dist` directory.

5. **Running the Executable**:
   Navigate to the `dist` directory and run the `main.exe` (Windows) or `main` (macOS/Linux) file.

## File Structure

- `main.py`: Entry point for the application.
- `create_tab.py`: Contains the logic and UI for creating new PDF forms.
- `update_tab.py`: Handles updating existing form entries.
- `database_tab.py`: Displays the database entries and allows export to CSV.
- `data_handler.py`: Manages database interactions and data processing.
- `form_fields_validation.py`: Contains validation logic for form fields.
- `pdf_filler.py`: Functions for filling out and saving PDF forms.
- `template.pdf`: The PDF template used for filling in the form data.

## Handling Common Issues

1. **PDF File Not Found**: If the application cannot find `template.pdf`, ensure it is in the same directory as `main.py`. You may need to adjust the file path in the `resource_path` function in `main.py`.

2. **Permission Issues**: If you encounter permission errors when running the executable, try running it with administrator privileges.

3. **Missing Dependencies**: Ensure all required packages are installed. Use the command below to install missing packages:

   ```bash
   pip install -r requirements.txt
   ```

## Additional Information

For further customization or troubleshooting, refer to the code comments in each Python file. If you have any questions or need additional support, feel free to contact the project maintainers.

### Instructions:

1. **Create a `README.md` File**:
   - Save the above content into a file named `README.md` in your project directory.

2. **Update Repository URL** (if applicable):
   - Replace `<repository_url>` in the clone command with your actual repository URL if sharing with others.

3. **Additional Instructions**:
   - Modify any sections to better fit your project’s structure or additional dependencies.
