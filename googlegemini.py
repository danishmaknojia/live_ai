import os
import io
import json
import requests
import streamlit as st
from PIL import Image
from google.cloud import vision
import google.generativeai as genai  # Google Gemini API

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "/Users/danishmak/Documents/Hackathon/secretsgoogle.json"
)

# Set Google Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Google Cloud clients
vision_client = vision.ImageAnnotatorClient()

# Define fields to extract
EXTRACT_FIELDS = {
    "patient_name": "",
    "patient_dob": "",
    "patient_gender": "",
    "patient_address": "",
    "patient_phone": "",
    "patient_relationship_to_insured": "",
    "patient_status": "",
    "insured_name": "",
    "insured_policy_number": "",
    "insured_employer_or_school": "",
    "insurance_plan_name": "",
    "insurance_program_name": "",
    "condition_related_to_employment": "",
    "condition_related_to_auto_accident": "",
    "condition_related_to_other_accident": "",
    "diagnosis": "",
    "secondary_diagnosis": "",
    "service_dates": "",
    "referring_physician_name": "",
    "referring_physician_id": "",
    "facility_name": "",
    "facility_address": "",
    "total_charge": "",
    "amount_paid": "",
    "balance_due": "",
    "federal_tax_id": "",
    "patient_account_number": "",
    "accept_assignment": "",
    "prior_authorization_number": "",
    "outside_lab": "",
}

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
)


def extract_text_from_image(image):
    """Extracts text from an image using Google Vision API."""
    try:
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

    except Exception as e:
        return f"Error extracting text: {str(e)}"


def process_text_with_gemini(text):
    """Uses Gemini API to extract structured data from text."""
    extracted_info = {key: "Not Found" for key in EXTRACT_FIELDS}

    headers = {"Content-Type": "application/json"}
    # payload = {"contents": [{"parts": [{"text": text}]}]}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Extract relevant structured information from the following text:"
                    },
                    {"text": text},
                    {
                        "text": "Ensure the response is in JSON format with only the following fields if any fields are missing still return the field but say missing. Additionally, we need to return all these fields for a form so make sure you return them: "
                        + ", ".join(EXTRACT_FIELDS)
                    },
                ]
            }
        ]
    }
    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            data=json.dumps(payload),
        )

        # Check if response is empty
        if response.status_code != 200:
            return f"Gemini API Error: {response.status_code} - {response.text}"

        response_data = response.json()

        # Ensure response contains expected data
        if "candidates" not in response_data or not response_data["candidates"]:
            return "Gemini Processing Error: Empty response"

        structured_text = (
            response_data["candidates"][0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

        if not structured_text.strip():
            return "Gemini Processing Error: No text extracted"

        # Process structured text (assuming JSON format)
        try:
            extracted_info = json.loads(structured_text)
        except json.JSONDecodeError:
            return f"Gemini Processing Error: Invalid JSON response - {structured_text}"

    except Exception as e:
        return f"Gemini Processing Error: {str(e)}"

    return extracted_info


def main():
    st.title("CMS-1500 Form Extractor Using Google Vision & Gemini AI")

    input_option = st.radio("Select Input Method", ("Text", "Image"))
    text_input = ""

    if input_option == "Text":
        text_input = st.text_area("Enter medical form text:")
    elif input_option == "Image":
        image_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
        if image_file:
            image = Image.open(image_file)
            st.image(
                image, caption="Uploaded Image", use_container_width=True
            )  # Updated deprecated parameter
            with st.spinner("Extracting text..."):
                text_input = extract_text_from_image(image)
                if "Error" not in text_input and text_input.strip():
                    st.success("Text extraction successful!")
                else:
                    st.error("No text detected. Please try another image.")

    if st.button("Extract Information"):
        if text_input and "Error" not in text_input:
            with st.spinner("Processing text with Gemini AI..."):
                extracted_info = process_text_with_gemini(text_input)
                st.subheader("Extracted Information")

                if isinstance(extracted_info, str):  # Handle errors returned as strings
                    st.error(extracted_info)
                else:
                    # Display extracted info
                    for key, value in extracted_info.items():
                        st.text_input(key.replace("_", " ").title(), value)
        else:
            st.error("Please enter text or upload an image.")


if __name__ == "__main__":
    main()
