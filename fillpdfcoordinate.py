from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

pdf_path = "claimform.pdf"
output_path = "filled_claimform.pdf"

# Grid spacing
GRID_SPACING = 20  # Adjust for density

adjust_sex_coord = lambda sex, x, y: (
    (sex, x - 10, y) if sex == "F" else (sex, x - 48, y)
)

# Data to overlay (adjust coordinates as needed)
# Example dynamic variables (to be assigned actual values elsewhere in the code)
insured_name = "John Doe"
insured_address = "123 Main St, Apt 4B"
insured_city = "New York"
insured_state = "NY"
insured_zip = "10001"
insurance_programs = {
    "Medicare": "",
    "Medicaid": "",
    "CHAMPUS": "",
    "CHAMPVA": "",
    "Group_Health_Plan": "",
    "FECA Black_Lung": "X",
    "Other": "",
}

patient_name = "Jane Doe"
patient_birth_date = "02/14/1985"
patient_sex = "F"  # "M" or "F"
patient_address = "456 Elm St, Apt 23"
patient_city = "Los Angeles"
patient_state = "CA"
patient_zip = "90001"
patient_phone = "555-123-4567"
patient_relationship = "X"  # single
patient_status = "X"  # employment

other_insured_name = "Mike Johnson"
other_insured_policy = "G123456789"
other_insured_birth_date = "06/10/1978"
other_insured_sex = "X"  # M
other_insured_employer = "ABC Corporation"
other_insured_insurance_plan = "XYZ Health Plan"
other_insured_reserved_use = "N/A"

condition_employment = "X"  # Yes
condition_auto_accident = ""
condition_auto_accident_place = "CA"
condition_other_accident = ""

Date_of_Current_Illness_Injury_or_Pregnancy = "01/15/2024"
First_Date_of_Similar_Illness = "12/01/2023"
Dates_Patient_Unable_to_Work_From = "01/20/2024"
Dates_Patient_Unable_to_Work_To = "02/05/2024"
Referring_Physician_Name = "Dr. John Smith"
Referring_Physician_ID = "RP123456"
Hospitalization_Dates_From = "01/25/2024"
Hospitalization_Dates_To = "02/02/2024"
Outside_Lab = "X"
Charges = "500"
Medicaid_Resubmission_Code = "07"
Original_Reference_Number = "OR987654"
Prior_Authorization_Number = "PA123456"
Diagnosis_1 = "J11.1"
Diagnosis_2 = "E11.9"
Diagnosis_3 = "I10"
Diagnosis_4 = "M54.5"
Date_of_Service_From = "02/01/2024"
Date_of_Service_To = "02/10/2024"
Place_of_Service = "2"
Type_of_Service = "3"
Procedures_CPT_HCPCS_Modifier = "99214"
Diagnosis_Code = "J11.1"
Charges = "$250"
Days_or_Units = "1"
EPSDT_or_Family_Plan = "No"
EMG = "No"
COB = "No"
Reserved_for_Local_Use = "N/A"
Federal_Tax_ID = "98-7654321"
Patient_Account_Number = "ACCT-12345"
Accept_Assignment = "X"
Total_Charge = "$1500"
Amount_Paid = "$200"
Balance_Due = "$1300"
Physician_Supplier_Signature = "Dr. Emily Brown"
Signed_Date = "02/10/2024"
Facility_Name_and_Address = "HealthCare Center, 123 Wellness St"
Physician_Supplier_Billing_Name_and_Address = "Dr. Emily Brown, MD"
PIN = "567890"
Group_Number = "G12345"
signed_date = "10/2/2024"
Insured_ID_Number = "INS123456"
Telephone = "123 456-7890"
Insured_Policy_Group_or_FECA_Number = "POL987654"
Insured_Birth_Date = "03/15/1980"
Sex = "X"  # M
Employer_or_School_Name = "ABC Corporation"
Insurance_Plan_Name = "XYZ Health Plan"
Another_Health_Benefit_Plan = "X"  # Yes
Insured_or_Authorized_Person_Signature = "John Doe"


# Form data mapping
form_data = {
    "INSURED’S NAME": (insured_name, 377, 657),
    "INSURED’S ADDRESS": (insured_address, 377, 630),
    "INSURED’S CITY": (insured_city, 377, 605),
    "INSURED’S STATE": (insured_state, 550, 605),
    "INSURED’S ZIP": (insured_zip, 377, 582),
    "Insurance_Programs": {
        "Medicare": (insurance_programs["Medicare"], 25, 677),
        "Medicaid": (insurance_programs["Medicaid"], 75, 677),
        "CHAMPUS": (insurance_programs["CHAMPUS"], 125, 677),
        "CHAMPVA": (insurance_programs["CHAMPVA"], 189, 677),
        "Group_Health_Plan": (insurance_programs["Group_Health_Plan"], 240, 677),
        "FECA Black_Lung": (insurance_programs["FECA Black_Lung"], 298, 677),
        "Other": (insurance_programs["Other"], 342, 677),
    },
    "Patient_Information": {
        "Patient_Name": (patient_name, 25, 657),
        "Patient_Birth_Date": (patient_birth_date, 235, 654),
        "Sex": adjust_sex_coord(patient_sex, 367, 654),
        "Patient_Address": (patient_address, 25, 630),
        "City": (patient_city, 25, 610),
        "State": (patient_state, 205, 610),
        "Zip_Code": (patient_zip, 25, 582),
        "Telephone": (patient_phone, 127, 582),
        "Patient_Relationship_to_Insured": (patient_relationship, 255, 630),
        "Patient_Status": (patient_status, 269, 605),
    },
    "Other_Insured_Information": {
        "Other_Insured_Name": (other_insured_name, 25, 558),
        "Other_Insured_Policy_or_Group_Number": (other_insured_policy, 25, 535),
        "Other_Insured_Birth_Date": (other_insured_birth_date, 25, 508),
        "Sex": (other_insured_sex, 146, 508),
        "Employer_or_School_Name": (other_insured_employer, 25, 488),
        "Insurance_Plan_Name_or_Program_Name": (other_insured_insurance_plan, 25, 465),
        "Reserved_for_Local_Use": (other_insured_reserved_use, 250, 465),
    },
    "Condition_Related_To": {
        "Employment": (condition_employment, 268, 535),
        "Auto_Accident": (condition_auto_accident, 268, 510),
        "Place": (condition_auto_accident_place, 342, 510),
        "Other_Accident": (condition_other_accident, 268, 485),
    },
    "Authorization": {
        "Insured_ID_Number": (Insured_ID_Number, 380, 680),
        "Telephone": (Telephone, 488, 583),
        "Insured_Policy_Group_or_FECA_Number": (
            Insured_Policy_Group_or_FECA_Number,
            380,
            560,
        ),
        "Insured_Birth_Date": (Insured_Birth_Date, 407, 533),
        "Sex": (Sex, 507, 533),
        "Employer_or_School_Name": (Employer_or_School_Name, 380, 510),
        "Insurance_Plan_Name": (Insurance_Plan_Name, 380, 484),
        "Another_Health_Benefit_Plan": (Another_Health_Benefit_Plan, 390, 461),
        "Insured_or_Authorized_Person_Signature": (
            Insured_or_Authorized_Person_Signature,
            420,
            420,
        ),
        "Patient_or_Authorized_Person_Signature": (patient_name, 110, 420),
        "Signed_Date": (signed_date, 310, 420),
    },
    "Medical_Information": {
        "Date_of_Current_Illness_Injury_or_Pregnancy": (
            Dates_Patient_Unable_to_Work_From,
            27,
            390,
        ),
        "First_Date_of_Similar_Illness": (First_Date_of_Similar_Illness, 280, 390),
        "Dates_Patient_Unable_to_Work_From": (
            Dates_Patient_Unable_to_Work_From,
            410,
            390,
        ),
        "Dates_Patient_Unable_to_Work_To": (Dates_Patient_Unable_to_Work_To, 505, 390),
        "Referring_Physician_Name": (Referring_Physician_Name, 27, 364),
        "Referring_Physician_ID": (Referring_Physician_ID, 220, 364),
        "Hospitalization_Dates_From": (Hospitalization_Dates_From, 410, 364),
        "Hospitalization_Dates_To": (Hospitalization_Dates_To, 505, 364),
        "Outside_Lab": (Outside_Lab, 390, 342),
        "Lab_Charges": (Charges, 462, 342),  # Avoid duplicate "Charges"
        "Medicaid_Resubmission_Code": (Medicaid_Resubmission_Code, 380, 317),
        "Original_Reference_Number": (Original_Reference_Number, 462, 317),
        "Prior_Authorization_Number": (Prior_Authorization_Number, 380, 297),
        "Diagnosis_1": (Diagnosis_1, 41, 317),
        "Diagnosis_2": (Diagnosis_2, 41, 295),
        "Diagnosis_3": (Diagnosis_3, 240, 317),
        "Diagnosis_4": (Diagnosis_4, 240, 295),
    },
    "Procedures_Services_Supplies": {
        "Date_of_Service_From": (Date_of_Service_From, 23, 245),
        "Date_of_Service_To": (Date_of_Service_To, 83, 245),
        "Place_of_Service": (Place_of_Service, 154, 245),
        "Type_of_Service": (Type_of_Service, 174, 245),
        "Procedures_CPT_HCPCS_Modifier": (Procedures_CPT_HCPCS_Modifier, 200, 245),
        "Diagnosis_Code": (Diagnosis_Code, 324, 245),
        "Procedure_Charges": (Charges, 384, 245),  # Differentiate from lab charges
        "Days_or_Units": (Days_or_Units, 444, 245),
        "EPSDT_or_Family_Plan": (EPSDT_or_Family_Plan, 464, 245),
        "EMG": (EMG, 484, 245),
        "COB": (COB, 504, 245),
        "Reserved_for_Local_Use": (Reserved_for_Local_Use, 524, 245),
    },
    "Billing_Information": {
        "Federal_Tax_ID": (Federal_Tax_ID, 25, 103),
        "Patient_Account_Number": (Patient_Account_Number, 180, 103),
        "Accept_Assignment": (Accept_Assignment, 290, 103),
        "Total_Charge": (Total_Charge, 390, 103),
        "Amount_Paid": (Amount_Paid, 470, 103),
        "Balance_Due": (Balance_Due, 530, 103),
        "Physician_Supplier_Signature": (Physician_Supplier_Signature, 55, 40),
        "Signed_Date": (Signed_Date, 40, 60),
        "Facility_Name_and_Address": (Facility_Name_and_Address, 180, 60),
        "Physician_Supplier_Billing_Name_and_Address": (
            Physician_Supplier_Billing_Name_and_Address,
            380,
            60,
        ),
        "PIN": (PIN, 400, 40),
        "Group_Number": (Group_Number, 500, 40),
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
