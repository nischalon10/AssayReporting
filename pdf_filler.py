from pdfrw import PdfReader, PdfWriter

def fill_pdf_form(template_path, output_path, data):
    """
    Fills a PDF form with provided data and saves the result to an output file.

    :param template_path: Path to the template PDF file
    :param output_path: Path where the filled PDF will be saved
    :param data: Dictionary containing field names as keys and field values as values
    """
    # Read the PDF template
    template_pdf = PdfReader(template_path)
    annotations = template_pdf.pages[0].Annots

    # Fill in the form fields
    for annotation in annotations:
        if annotation.Subtype == '/Widget' and annotation.T:
            field_name = annotation.T[1:-1]
            if field_name in data:
                annotation.V = data[field_name]
                annotation.AP = None  # Remove appearance, force PDF to regenerate

    # Write filled PDF to file
    PdfWriter().write(output_path, template_pdf)
    print(f"PDF filled and saved to {output_path}")