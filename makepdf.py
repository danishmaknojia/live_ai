from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import json

pdf_path = "claimform.pdf"
output_path = "filled_claimform.pdf"

# Grid spacing
GRID_SPACING = 20  # Adjust for density

import json


# Load JSON file and replace all null values with empty strings
with open("gemini_response.txt", "r") as file:
    data = json.load(file)

# Convert None (null) values to empty strings
for key, value in data.items():
    if value is None:
        data[key] = ""
    elif isinstance(value, dict):  # Handle nested dictionaries
        for sub_key, sub_value in value.items():
            if sub_value is None:
                data[key][sub_key] = ""


# Extract values with fallback to empty string ("") if key is missing
insured_name = data.get("insured_name", "")
insured_address = data.get("insured_address", "")
insured_city = data.get("insured_city", "")
insured_state = data.get("insured_state", "")
insured_zip = data.get("insured_zip", "")

insurance_programs = {
    "Medicare": "X" if data.get("insurance_programs", {}).get("Medicare") else "",
    "CHAMPUS": "X" if data.get("insurance_programs", {}).get("CHAMPUS") else "",
    "CHAMPVA": "X" if data.get("insurance_programs", {}).get("CHAMPVA") else "",
    "Medicaid": "X" if data.get("insurance_programs", {}).get("Medicaid") else "",
    "FECA Black_Lung": (
        "X" if data.get("insurance_programs", {}).get("FECA Black_Lung") else ""
    ),
    "Other": "X" if data.get("insurance_programs", {}).get("Other") else "",
    "Group_Health_Plan": (
        "X" if data.get("insurance_programs", {}).get("Group_Health_Plan") else ""
    ),
}

patient_name = data.get("patient_name", "")
patient_birth_date = data.get("patient_birth_date", "")
patient_sex = "X" if data.get("patient_sex", "").lower() in ["male", "m"] else "X"
patient_address = data.get("patient_address", "")
patient_city = data.get("patient_city", "")
patient_state = data.get("patient_state", "")
patient_zip = data.get("patient_zip", "")
patient_phone = data.get("patient_phone", "") or " "
patient_relationship = data.get("patient_relationship", "")
patient_status = data.get("patient_status", "")

other_insured_name = data.get("other_insured_name", "")
other_insured_policy = data.get("other_insured_policy", "") or " "
other_insured_birth_date = data.get("other_insured_birth_date", "")
other_insured_sex = "x"
other_insured_employer = data.get("other_insured_employer", "")
other_insured_insurance_plan = data.get("other_insured_insurance_plan", "")
other_insured_reserved_use = data.get("other_insured_reserved_use", "")

condition_employment = "x"
condition_auto_accident = " "
condition_auto_accident_place = data.get("condition_auto_accident_place", "")
condition_other_accident = " "

Date_of_Current_Illness_Injury_or_Pregnancy = data.get(
    "Date_of_Current_Illness_Injury_or_Pregnancy", ""
)
First_Date_of_Similar_Illness = data.get("First_Date_of_Similar_Illness", "")
Dates_Patient_Unable_to_Work_From = data.get("Dates_Patient_Unable_to_Work_From", "")
Dates_Patient_Unable_to_Work_To = data.get("Dates_Patient_Unable_to_Work_To", "")
Referring_Physician_Name = data.get("Referring_Physician_Name", "")
Referring_Physician_ID = data.get("Referring_Physician_ID", "")
Hospitalization_Dates_From = data.get("Hospitalization_Dates_From", "")
Hospitalization_Dates_To = data.get("Hospitalization_Dates_To", "")
Outside_Lab = "X"
Charges = data.get("Charges", "")
Medicaid_Resubmission_Code = data.get("Medicaid_Resubmission_Code", "")
Original_Reference_Number = data.get("Original_Reference_Number", "")
Prior_Authorization_Number = data.get("Prior_Authorization_Number", "")

Diagnosis_1 = data.get("Diagnosis_1", "")
Diagnosis_2 = data.get("Diagnosis_2", "")
Diagnosis_3 = data.get("Diagnosis_3", "")
Diagnosis_4 = data.get("Diagnosis_4", "")

Date_of_Service_From = data.get("Date_of_Service_From", "")
Date_of_Service_To = data.get("Date_of_Service_To", "")
Place_of_Service = data.get("Place_of_Service", "")
Type_of_Service = data.get("Type_of_Service", "")
Procedures_CPT_HCPCS_Modifier = data.get("Procedures_CPT_HCPCS_Modifier", "")
Diagnosis_Code = data.get("Diagnosis_Code", "")
Procedure_Charges = data.get("Procedure_Charges", "")
Days_or_Units = data.get("Days_or_Units", "")
EPSDT_or_Family_Plan = data.get("EPSDT_or_Family_Plan", "")
EMG = data.get("EMG", "")
COB = data.get("COB", "")
Reserved_for_Local_Use = data.get("Reserved_for_Local_Use", "")

Federal_Tax_ID = data.get("Federal_Tax_ID", "")
Patient_Account_Number = data.get("Patient_Account_Number", "")
Accept_Assignment = "X"
Total_Charge = data.get("Total_Charge", "")
Amount_Paid = data.get("Amount_Paid", "")
Balance_Due = data.get("Balance_Due", "")
Physician_Supplier_Signature = data.get("Physician_Supplier_Signature", "")
Signed_Date = data.get("Signed_Date", "")

Facility_Name_and_Address = data.get("Facility_Name_and_Address", "")
Physician_Supplier_Billing_Name_and_Address = data.get(
    "Physician_Supplier_Billing_Name_and_Address", ""
)
PIN = data.get("PIN", "")
Group_Number = data.get("Group_Number", "")
signed_date = data.get("signed_date", "")
Insured_ID_Number = data.get("Insured_ID_Number", "")
Telephone = data.get("Telephone", "")
Insured_Policy_Group_or_FECA_Number = data.get(
    "Insured_Policy_Group_or_FECA_Number", ""
)
Insured_Birth_Date = data.get("Insured_Birth_Date", "")
Sex = "X"
Employer_or_School_Name = data.get("Employer_or_School_Name", "")
Insurance_Plan_Name = data.get("Insurance_Plan_Name", "")
Another_Health_Benefit_Plan = "X"
Insured_or_Authorized_Person_Signature = data.get(
    "Insured_or_Authorized_Person_Signature", ""
)

# Print extracted values (for debugging)
print(f"Patient Name: {patient_name}")
print(f"Patient Birth Date: {patient_birth_date}")
print(f"Patient Sex: {patient_sex}")
print(f"Patient Address: {patient_address}")
print(f"Patient Phone: {patient_phone}")
print(f"Insured Name: {insured_name}")
print(f"Diagnosis 1: {Diagnosis_1}")
print(f"Total Charge: {Total_Charge}")
print(f"Amount Paid: {Amount_Paid}")
print(f"Balance Due: {Balance_Due}")


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
        "Sex": (patient_sex, 357, 654),
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
# can.setStrokeColorRGB(0.8, 0.8, 0.8)  # Light gray grid color
# can.setLineWidth(0.5)

# Vertical grid lines
# for x in range(0, int(width), GRID_SPACING):
#     can.line(x, 0, x, height)
#     can.drawString(x + 2, 5, str(x))  # Label x-axis

# Horizontal grid lines
# for y in range(0, int(height), GRID_SPACING):
#     can.line(0, y, width, y)
#     can.drawString(2, y + 2, str(y))  # Label y-axis

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
