import datetime
import sqlite3  # Using SQLite for database operations, can be changed to another DB system

# Database configuration (using SQLite for demonstration purposes)
DB_FILE = 'form_data.db'

# Function to initialize the database and create the table if it doesn't exist
def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS form_entries (
                        id INTEGER PRIMARY KEY,
                        fa_number TEXT,
                        date TEXT,
                        customer_name TEXT,
                        sample_type TEXT,
                        sample_weight TEXT,
                        fineness_percent TEXT,
                        fineness_parts TEXT,
                        other_info TEXT)''')
    conn.commit()
    conn.close()

# Function to get current local date-time in the specified format
def get_current_timestamp():
    return datetime.datetime.now().strftime("%d-%b-%Y %I:%M %p")

# Function to auto-generate FA number (basic implementation, can be customized)
def generate_fa_number():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM form_entries")
    fa_count = cursor.fetchone()[0] + 1
    fa_number = f"FA-{fa_count:05d}"  # Example format: FA-00001
    conn.close()
    return fa_number

# Function to validate form responses (add specific checks as needed)
def validate_responses(data):
    if not data.get('customerNameField'):
        return False, "Customer Name cannot be empty."
    if not data.get('sampleTypeField'):
        return False, "Sample Type cannot be empty."
    if not data.get('sampleWeightField'):
        return False, "Sample Weight cannot be empty."
    # Add more validations as needed
    return True, ""

# Function to check if the entry already exists in the database
def check_duplicate_entry(data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM form_entries WHERE customer_name = ? AND sample_type = ? AND sample_weight = ?",
                   (data['customerNameField'], data['sampleTypeField'], data['sampleWeightField']))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    return False

# Function to insert form data into the database
def insert_into_database(data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO form_entries (
                        fa_number, date, customer_name, sample_type, sample_weight,
                        fineness_percent, fineness_parts, other_info)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (data['faNoField'], data['dateField'], data['customerNameField'], 
                    data['sampleTypeField'], data['sampleWeightField'], data['finenessPercentField'],
                    data['finenessPartsField'], data['otherInfoField']))

    conn.commit()
    conn.close()

# Function to handle all data processing
def process_form_data(data):
    # Generate date-time stamp
    data['dateField'] = get_current_timestamp()
    
    # Generate FA number
    data['faNoField'] = generate_fa_number()
    
    # Validate responses
    is_valid, message = validate_responses(data)
    if not is_valid:
        return False, message
    
    # Check for duplicate entry
    if check_duplicate_entry(data):
        return False, "Duplicate entry found in the database."

    # Insert into the database
    insert_into_database(data)
    return True, "Data processed and saved successfully."


def get_form_data(fa_number):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM form_entries WHERE fa_number = ?", (fa_number,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'faNoField': row[1],
            'dateField': row[2],
            'customerNameField': row[3],
            'sampleTypeField': row[4],
            'sampleWeightField': row[5],
            'finenessPercentField': row[6],
            'finenessPartsField': row[7],
            'otherInfoField': row[8]
        }
    return None

# Function to update form data in the database
def update_form_data(data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''UPDATE form_entries SET 
                      customer_name = ?, 
                      sample_type = ?, 
                      sample_weight = ?, 
                      fineness_percent = ?, 
                      fineness_parts = ?, 
                      other_info = ? 
                      WHERE fa_number = ?''',
                   (data['customerNameField'], data['sampleTypeField'], data['sampleWeightField'],
                    data['finenessPercentField'], data['finenessPartsField'], data['otherInfoField'],
                    data['faNoField']))
    conn.commit()
    conn.close()
    return True, "Data updated successfully."

# Function to fetch all records from the database
def get_all_records():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM form_entries")
    records = cursor.fetchall()
    conn.close()
    return records
