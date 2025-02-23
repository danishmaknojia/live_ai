import os
import io
import re
import streamlit as st
from PIL import Image
from google.cloud import vision, language_v1

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "/Users/danishmak/Documents/Hackathon/secretsgoogle.json"
)

# Initialize Google Cloud clients
vision_client = vision.ImageAnnotatorClient()
language_client = language_v1.LanguageServiceClient()

# Define fields to extract with default "Not Found" values
EXTRACT_FIELDS = {
    "patient_name": "Not Found",
    "patient_dob": "Not Found",
    "patient_gender": "Not Found",
    "patient_address": "Not Found",
    "patient_phone": "Not Found",
    "insured_name": "Not Found",
    "insured_policy_number": "Not Found",
    "insurance_plan_name": "Not Found",
    "service_dates": "Not Found",
    "diagnosis": "Not Found",
    "total_charge": "Not Found",
    "amount_paid": "Not Found",
    "balance_due": "Not Found",
    "facility_name": "Not Found",
    "facility_address": "Not Found",
    "patient_account_number": "Not Found",
}


def extract_text_from_image(image):
    """Extracts structured text from an image using Google Vision API."""
    try:
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_content = image_bytes.getvalue()

        image = vision.Image(content=image_content)
        response = vision_client.document_text_detection(image=image)

        if response.error.message:
            return f"Error: {response.error.message}"

        return (
            response.full_text_annotation.text
            if response.full_text_annotation.text
            else "No text detected"
        )

    except Exception as e:
        return f"Error extracting text: {str(e)}"


def analyze_text_with_google_nlp(text):
    """Analyzes text using Google Cloud NLP API and extracts relevant fields."""
    extracted_info = EXTRACT_FIELDS.copy()

    try:
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = language_client.analyze_entities(document=document)

        for entity in response.entities:
            entity_type = language_v1.Entity.Type(entity.type_).name
            entity_text = entity.name

            if entity_type == "PERSON":
                if extracted_info["patient_name"] == "Not Found":
                    extracted_info["patient_name"] = entity_text
                elif extracted_info["insured_name"] == "Not Found":
                    extracted_info["insured_name"] = entity_text
            elif entity_type == "DATE":
                if extracted_info["patient_dob"] == "Not Found":
                    extracted_info["patient_dob"] = entity_text
                elif extracted_info["service_dates"] == "Not Found":
                    extracted_info["service_dates"] = entity_text
            elif entity_type == "LOCATION":
                if extracted_info["patient_address"] == "Not Found":
                    extracted_info["patient_address"] = entity_text
                elif extracted_info["facility_address"] == "Not Found":
                    extracted_info["facility_address"] = entity_text
            elif entity_type == "ORGANIZATION" and "insurance" in entity_text.lower():
                extracted_info["insurance_plan_name"] = entity_text
            elif entity_type == "NUMBER":
                if "$" in entity_text and extracted_info["total_charge"] == "Not Found":
                    extracted_info["total_charge"] = entity_text

        # Extract additional details using regex
        extracted_info.update(extract_with_regex(text))

    except Exception as e:
        extracted_info["error"] = f"NLP Processing Error: {str(e)}"

    return extracted_info


def extract_with_regex(text):
    """Extracts specific details using regex patterns."""
    extracted = {}

    patterns = {
        "patient_phone": r"\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}",
        "total_charge": r"Total Charge:\s*\$?(\d+(?:\.\d{2})?)",
        "amount_paid": r"Amount Paid:\s*\$?(\d+(?:\.\d{2})?)",
        "balance_due": r"Balance Due:\s*\$?(\d+(?:\.\d{2})?)",
        "diagnosis": r"(?i)Diagnosis:\s*(.+)",
        "facility_name": r"Facility Name:\s*(.+)",
        "facility_address": r"Facility Address:\s*(.+)",
        "patient_account_number": r"Account Number:\s*(\d+)",
        "insured_policy_number": r"Policy Number:\s*(\S+)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted[key] = match.group(1).strip()

    return extracted


def main():
    st.title("CMS-1500 Form Extractor Using Google Cloud NLP & Vision API")

    input_option = st.radio("Select Input Method", ("Text", "Image"))
    text_input = ""

    if input_option == "Text":
        text_input = st.text_area("Enter medical form text:")
    elif input_option == "Image":
        image_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
        if image_file:
            image = Image.open(image_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            with st.spinner("Extracting text..."):
                text_input = extract_text_from_image(image)
                if "Error" not in text_input and text_input.strip():
                    st.success("Text extraction successful!")
                else:
                    st.error("No text detected. Please try another image.")

    if st.button("Extract Information"):
        if text_input and "Error" not in text_input:
            with st.spinner("Processing text with NLP..."):
                info = analyze_text_with_google_nlp(text_input)
                st.subheader("Extracted Information")
                for key, value in info.items():
                    st.text_input(key.replace("_", " ").title(), value)
        else:
            st.error("Please enter text or upload an image.")


if __name__ == "__main__":
    main()
