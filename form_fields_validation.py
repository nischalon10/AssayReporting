import re

# Define the regex patterns based on the provided rules.
CUSTOMER_NAME_PATTERN = re.compile(r'^[A-Za-z0-9\s/]+$')
FINENESS_PATTERN = re.compile(r'^\d{2}\.\d{2}$')

def validate_customer_name(customer_name):
    """Validate customer name based on regex pattern."""
    if not customer_name.strip():
        return False, "Customer Name cannot be empty."
    if not CUSTOMER_NAME_PATTERN.match(customer_name):
        return False, "Customer Name can only contain letters, numbers, spaces, and slashes (/)."
    return True, ""

def validate_sample_type(sample_type):
    """Validate sample type (e.g., should not be empty)."""
    if not sample_type.strip():
        return False, "Sample Type cannot be empty."
    return True, ""

def validate_sample_weight(sample_weight):
    """Validate sample weight (e.g., should be a number greater than zero)."""
    try:
        weight = float(sample_weight)
        if weight <= 0:
            return False, "Sample Weight must be greater than zero."
    except ValueError:
        return False, "Sample Weight must be a valid number."
    return True, ""

def validate_fineness_percent(fineness_percent):
    """Validate fineness percent based on the pattern."""
    if not FINENESS_PATTERN.match(fineness_percent):
        return False, "Fineness in % must be a number with exactly two decimal places, e.g., 12.34."
    return True, ""

def validate_fineness_parts(fineness_parts):
    """Validate fineness parts (e.g., should be a string representing a fraction)."""
    if '/' in fineness_parts and len(fineness_parts.split('/')) == 2:
        numerator, denominator = fineness_parts.split('/')
        try:
            num = int(numerator)
            denom = int(denominator)
            if denom == 0:
                return False, "Denominator cannot be zero."
            return True, ""
        except ValueError:
            return False, "Fineness Parts must be in the form 'numerator/denominator'."
    else:
        return False, "Fineness Parts must be in the form 'numerator/denominator'."

def validate_other_info(other_info):
    """Optional validation for other info (e.g., no validation)."""
    return True, ""  # No validation rule provided, always returns True

def validate_all_fields(data):
    """Validate all fields using individual field validation functions."""
    validators = {
        'customerNameField': validate_customer_name,
        'sampleTypeField': validate_sample_type,
        'sampleWeightField': validate_sample_weight,
        'finenessPercentField': validate_fineness_percent,
        'finenessPartsField': validate_fineness_parts,
        'otherInfoField': validate_other_info,
    }
    
    for field, validator in validators.items():
        is_valid, message = validator(data.get(field, ""))
        if not is_valid:
            return False, message
    
    return True, "All fields are valid."

# Example of usage:
data = {
    'customerNameField': 'Customer/123',
    'sampleTypeField': 'Gold',
    'sampleWeightField': '12.34',
    'finenessPercentField': '56.78',
    'finenessPartsField': '5/6',
    'otherInfoField': 'No additional info',
}

