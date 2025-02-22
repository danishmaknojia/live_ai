from pypdf import PdfReader, PdfWriter

# Load the PDF
pdf_path = "/Users/danishmak/Documents/Hackathon/claimform.pdf"
output_path = "/Users/danishmak/Documents/Hackathon/filled_claimform.pdf"

reader = PdfReader(pdf_path)
writer = PdfWriter()

# Check for fillable form fields
fields = reader.get_fields()
if fields:
    print("Available Fillable Fields:")
    for field_name in fields.keys():
        print(field_name)
else:
    print("No fillable form fields found. The PDF might not be an interactive form.")

# Dictionary mapping extracted field names to values
form_data = {
    "INSURED’S NAME": "John Doe",
    "INSURED’S ADDRESS": "123 Main St",
    "CITY": "New York",
    "STATE": "NY",
    "ZIP CODE": "10001",
    "INSURED’S POLICY GROUP OR FECA NUMBER": "A12345678",
    "PATIENT’S NAME": "Jane Doe",
    "PATIENT’S BIRTH DATE": "01/01/1990",
    "PHYSICIAN’S NAME": "Dr. Smith",
}

# Ensure we only use available fields
if fields:
    form_data = {key: value for key, value in form_data.items() if key in fields}
    if not form_data:
        print("Warning: None of the specified fields match the actual PDF form fields.")
else:
    print("Error: No interactive form fields found in the PDF.")

# Fill form fields
for page in reader.pages:
    writer.add_page(page)
    writer.update_page_form_field_values(page, form_data)

# Save the filled form
with open(output_path, "wb") as output_pdf:
    writer.write(output_pdf)

print(f"Filled form saved to {output_path}")
