import base64
import os
import io
import json
import requests
import streamlit as st
from PIL import Image
from google.cloud import vision
import google.generativeai as genai  # Google Gemini API

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secretsgoogle.json"

# Set Google Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Google Cloud clients
vision_client = vision.ImageAnnotatorClient()

# Define fields to extract
EXTRACT_FIELDS = {
    "insured_name": "",
    "insured_address": "",
    "insured_city": "",
    "insured_state": "",
    "insured_zip": "",
    "insurance_programs": {
        "Medicare": "",
        "Medicaid": "",
        "CHAMPUS": "",
        "CHAMPVA": "",
        "Group_Health_Plan": "",
        "FECA Black_Lung": "",
        "Other": "",
    },
    "patient_name": "",
    "patient_birth_date": "",
    "patient_sex": "",
    "patient_address": "",
    "patient_city": "",
    "patient_state": "",
    "patient_zip": "",
    "patient_phone": "",
    "patient_relationship": "",
    "patient_status": "",
    "other_insured_name": "",
    "other_insured_policy": "",
    "other_insured_birth_date": "",
    "other_insured_sex": "",
    "other_insured_employer": "",
    "other_insured_insurance_plan": "",
    "other_insured_reserved_use": "",
    "condition_employment": "",
    "condition_auto_accident": "",
    "condition_auto_accident_place": "",
    "condition_other_accident": "",
    "Date_of_Current_Illness_Injury_or_Pregnancy": "",
    "First_Date_of_Similar_Illness": "",
    "Dates_Patient_Unable_to_Work_From": "",
    "Dates_Patient_Unable_to_Work_To": "",
    "Referring_Physician_Name": "",
    "Referring_Physician_ID": "",
    "Hospitalization_Dates_From": "",
    "Hospitalization_Dates_To": "",
    "Outside_Lab": "",
    "Charges": "",
    "Medicaid_Resubmission_Code": "",
    "Original_Reference_Number": "",
    "Prior_Authorization_Number": "",
    "Diagnosis_1": "",
    "Diagnosis_2": "",
    "Diagnosis_3": "",
    "Diagnosis_4": "",
    "Date_of_Service_From": "",
    "Date_of_Service_To": "",
    "Place_of_Service": "",
    "Type_of_Service": "",
    "Procedures_CPT_HCPCS_Modifier": "",
    "Diagnosis_Code": "",
    "Procedure_Charges": "",
    "Days_or_Units": "",
    "EPSDT_or_Family_Plan": "",
    "EMG": "",
    "COB": "",
    "Reserved_for_Local_Use": "",
    "Federal_Tax_ID": "",
    "Patient_Account_Number": "",
    "Accept_Assignment": "",
    "Total_Charge": "",
    "Amount_Paid": "",
    "Balance_Due": "",
    "Physician_Supplier_Signature": "",
    "Signed_Date": "",
    "Facility_Name_and_Address": "",
    "Physician_Supplier_Billing_Name_and_Address": "",
    "PIN": "",
    "Group_Number": "",
    "signed_date": "",
    "Insured_ID_Number": "",
    "Telephone": "",
    "Insured_Policy_Group_or_FECA_Number": "",
    "Insured_Birth_Date": "",
    "Sex": "",
    "Employer_or_School_Name": "",
    "Insurance_Plan_Name": "",
    "Another_Health_Benefit_Plan": "",
    "Insured_or_Authorized_Person_Signature": "",
}


GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
)


def extract_text_from_image(image):
    """Extracts text from an image using Google Vision API."""
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_content = image_bytes.getvalue()

    vision_image = vision.Image(content=image_content)
    response = vision_client.document_text_detection(image=vision_image)

    if response.error.message:
        return f"Error: {response.error.message}"

    return (
        response.full_text_annotation.text
        if response.full_text_annotation.text
        else "No text detected"
    )


def process_text_with_gemini(text, output_file="gemini_response.txt"):
    """Uses Gemini API to extract structured data from text and saves response to a txt file."""
    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Extract structured information from the following text as a **valid JSON object**.\n\n"
                            "⚠️ **JSON Formatting Rules:**\n"
                            '1. **Return only a valid JSON object** with **double quotes (`"`) for all keys and values**.\n'
                            '2. **All missing fields must be empty strings (`""`)** – do not use `null`.\n'
                            "3. **Ensure all fields listed below are included**, even if their values are empty.\n"
                            "4. **Convert all date fields to `MM-DD-YYYY` format** (e.g., `February 10, 1979` → `02-10-1979`).\n"
                            "5. **Extract only the street address** for `insured_address` and `patient_address` (omit city, state, zip).\n"
                            "6. **Do not add explanations, line breaks, or extra text – return only the JSON.**\n"
                            "7. **Ensure the response is properly escaped and does not contain formatting issues.**\n\n"
                            "🚀 **Extract the following fields as JSON:**\n"
                            + json.dumps(EXTRACT_FIELDS, indent=2)
                            + "\n\n"
                            "Now, extract the data from the text below and return **only the valid JSON response**:\n"
                        )
                    },
                    {"text": text},
                ]
            }
        ]
    }

    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        data=json.dumps(payload),
    )

    if response.status_code != 200:
        # error_message = f"Gemini API Error: {response.status_code} - {response.text}
        error_message = {response.text}
        with open(output_file, "w") as file:
            file.write(error_message)
        return error_message

    response_data = response.json()
    structured_text = (
        response_data.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text", "")
    )

    try:
        json_data = json.loads(structured_text)

        # Save JSON response to a text file
        with open(output_file, "w") as file:
            json.dump(json_data, file, indent=4)

        return json_data
    except json.JSONDecodeError:
        # Save raw text and remove unwanted formatting
        cleaned_text = structured_text.strip().split("\n")

        if cleaned_text[0].strip() == "```json":
            cleaned_text.pop(0)
        if cleaned_text[-1].strip() == "```":
            cleaned_text.pop()

        with open(output_file, "w") as file:
            file.write("\n".join(cleaned_text))

        return "\n".join(cleaned_text)


def display_pdf(pdf_path):
    """Embed PDF in Streamlit using an iframe."""
    with open(pdf_path, "rb") as pdf_file:
        base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
