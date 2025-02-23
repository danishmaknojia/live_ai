from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

pdf_path = "/Users/danishmak/Documents/Hackathon/claimform.pdf"
output_path = "/Users/danishmak/Documents/Hackathon/filled_claimform.pdf"

# Grid spacing
GRID_SPACING = 20  # Adjust for density

adjust_sex_coord = lambda sex, x, y: (
    (sex, x - 10, y) if sex == "F" else (sex, x - 48, y)
)

adjust_Patient_Relationship_to_Insured = lambda relation, x, y: (
    (relation, x - 10, y) if relation == "F" else (relation, x - 48, y)
)

# Data to overlay (adjust coordinates as needed)
form_data = form_data = {
    "INSURED’S NAME": ("John Doe", 377, 657),
    "INSURED’S ADDRESS": ("456 Elm St, Apt 23", 377, 630),
    "Insurance_Programs": {
        "Medicare": ("X", 25, 677),
        "Medicaid": ("X", 75, 677),
        "CHAMPUS": ("X", 125, 677),
        "CHAMPVA": ("X", 189, 677),
        "Group_Health_Plan": ("X", 240, 677),
        "FECA Black_Lung": ("X", 298, 677),
        "Other": ("X", 342, 677),
    },
    "Patient_Information": {
        "Patient_Name": ("Jane Doe", 25, 657),
        "Patient_Birth_Date": ("02/14/1985", 235, 654),
        "Sex": adjust_sex_coord("M", 367, 654),
        "Patient_Address": ("789 Oak Ave", 25, 630),
        "City": ("Los Angeles", 25, 610),
        "State": ("CA", 205, 610),
        "Zip_Code": ("90001", 25, 582),
        "Telephone": ("555-123-4567", 127, 582),
        "Patient_Relationship_to_Insured": ("Spouse", 110, 555),
        "Patient_Status": ("Single", 310, 555),
    },
    "Other_Insured_Information": {
        "Other_Insured_Name": ("Mike Johnson", 110, 525),
        "Other_Insured_Policy_or_Group_Number": ("G123456789", 310, 525),
        "Other_Insured_Birth_Date": ("06/10/1978", 450, 525),
        "Sex": ("M", 550, 525),
        "Employer_or_School_Name": ("ABC Corp", 110, 505),
        "Insurance_Plan_Name_or_Program_Name": ("XYZ Health", 310, 505),
        "Reserved_for_Local_Use": ("N/A", 450, 505),
    },
    "Condition_Related_To": {
        "Employment": ("Yes", 110, 475),
        "Auto_Accident": ("No", 310, 475),
        "Place": ("California", 450, 475),
        "Other_Accident": ("No", 550, 475),
    },
    "Authorization": {
        "Patient_or_Authorized_Person_Signature": ("Jane Doe", 110, 445),
        "Signed_Date": ("03/20/2024", 310, 445),
    },
    "Insured": {
        "Insured_ID_Number": ("A987654321", 110, 415),
        "Insured_Name": ("John Doe", 310, 415),
        "Insured_Address": ("456 Elm St, Apt 23", 450, 415),
        "City": ("Chicago", 550, 415),
        "State": ("IL", 650, 415),
        "Zip_Code": ("60610", 750, 415),
        "Telephone": ("555-789-1234", 850, 415),
        "Insured_Policy_Group_or_FECA_Number": ("G345678901", 110, 385),
        "Insured_Birth_Date": ("07/20/1980", 310, 385),
        "Sex": ("M", 450, 385),
        "Employer_or_School_Name": ("Tech Solutions", 550, 385),
        "Insurance_Plan_Name_or_Program_Name": ("Blue Shield", 700, 385),
        "Another_Health_Benefit_Plan": ("No", 850, 385),
        "Insured_or_Authorized_Person_Signature": ("John Doe", 110, 355),
    },
    "Medical_Information": {
        "Date_of_Current_Illness_Injury_or_Pregnancy": ("02/01/2024", 110, 325),
        "First_Date_of_Similar_Illness": ("01/15/2024", 310, 325),
        "Dates_Patient_Unable_to_Work": {
            "From": ("02/02/2024", 110, 295),
            "To": ("02/15/2024", 250, 295),
        },
        "Referring_Physician_Name": ("Dr. Emily Brown", 450, 295),
        "Referring_Physician_ID": ("MD67890", 600, 295),
        "Hospitalization_Dates": {
            "From": ("02/05/2024", 110, 265),
            "To": ("02/10/2024", 250, 265),
        },
        "Outside_Lab": ("Yes", 450, 265),
        "Charges": ("$1200", 600, 265),
        "Medicaid_Resubmission_Code": ("N/A", 750, 265),
        "Original_Reference_Number": ("ABC123", 900, 265),
        "Prior_Authorization_Number": ("PA56789", 1050, 265),
        "Diagnosis_or_Nature_of_Illness_or_Injury": {
            "Diagnosis_1": ("Flu", 110, 235),
            "Diagnosis_2": ("Fever", 250, 235),
            "Diagnosis_3": ("Cough", 450, 235),
            "Diagnosis_4": ("N/A", 600, 235),
        },
    },
    "Procedures_Services_Supplies": {
        "Service_Entries": [
            {
                "Date_of_Service": {
                    "From": ("02/07/2024", 110, 205),
                    "To": ("02/07/2024", 250, 205),
                },
                "Place_of_Service": ("Clinic", 450, 205),
                "Type_of_Service": ("Consultation", 600, 205),
                "Procedures_CPT_HCPCS_Modifier": ("99214", 750, 205),
                "Diagnosis_Code": ("J11.1", 900, 205),
                "Charges": ("$250", 1050, 205),
                "Days_or_Units": ("1", 1200, 205),
                "EPSDT_or_Family_Plan": ("No", 1350, 205),
                "EMG": ("No", 1500, 205),
                "COB": ("No", 1650, 205),
                "Reserved_for_Local_Use": ("N/A", 1800, 205),
            }
        ]
    },
    "Billing_Information": {
        "Federal_Tax_ID": ("98-7654321", 110, 175),
        "Patient_Account_Number": ("ACCT-12345", 250, 175),
        "Accept_Assignment": ("Yes", 450, 175),
        "Total_Charge": ("$1500", 600, 175),
        "Amount_Paid": ("$200", 750, 175),
        "Balance_Due": ("$1300", 900, 175),
        "Physician_Supplier_Signature": ("Dr. Emily Brown", 1050, 175),
        "Signed_Date": ("02/10/2024", 1200, 175),
        "Facility_Name_and_Address": ("HealthCare Center, 123 Wellness St", 110, 145),
        "Physician_Supplier_Billing_Name_and_Address": (
            "Dr. Emily Brown, MD",
            450,
            145,
        ),
        "PIN": ("567890", 750, 145),
        "Group_Number": ("G12345", 900, 145),
    },
}


# Function to recursively extract and draw text fields
def extract_fields(data, can):
    """Recursively extracts and draws text fields from form_data."""
    for key, value in data.items():
        if isinstance(value, tuple) and len(value) == 3:  # Valid (text, x, y) tuple
            text, x, y = value
            can.drawString(x, y, text)
        elif isinstance(value, dict):  # If it's a nested dictionary, recurse
            extract_fields(value, can)
        elif isinstance(value, list):  # Handle lists (e.g., Service Entries)
            for item in value:
                if isinstance(item, dict):
                    extract_fields(item, can)


# Load the original PDF
reader = PdfReader(pdf_path)
writer = PdfWriter()

# Create a new PDF overlay with text and grid
packet = BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
width, height = letter  # Get page size

# Draw grid lines
can.setStrokeColorRGB(0.8, 0.8, 0.8)  # Light gray grid color
can.setLineWidth(0.5)

# Vertical grid lines
for x in range(0, int(width), GRID_SPACING):
    can.line(x, 0, x, height)
    can.drawString(x + 2, 5, str(x))  # Label x-axis

# Horizontal grid lines
for y in range(0, int(height), GRID_SPACING):
    can.line(0, y, width, y)
    can.drawString(2, y + 2, str(y))  # Label y-axis

# Draw text at specified positions
can.setStrokeColorRGB(0, 0, 0)  # Black text color
extract_fields(form_data, can)

can.save()
packet.seek(0)

# Merge overlay with original PDF
overlay_pdf = PdfReader(packet)
for i, page in enumerate(reader.pages):
    page.merge_page(overlay_pdf.pages[0])  # Overlay only the first page
    writer.add_page(page)

# Save the new filled PDF
with open(output_path, "wb") as output_pdf:
    writer.write(output_pdf)

print(f"Filled form with grid saved to {output_path}")
