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
    "patient_name": "",
    "patient_dob": "",
    "patient_gender": "",
    "patient_address": "",
    "patient_phone": "",
    "insured_name": "",
    "insured_policy_number": "",
    "diagnosis": "",
    "service_dates": "",
    "total_charge": "",
    "amount_paid": "",
    "balance_due": "",
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
                        "text": "Extract relevant structured information from the following text and return it as a JSON object:"
                    },
                    {"text": text},
                    {
                        "text": "Ensure the response is in JSON format with only the following fields if any fields are missing still return the field but say missing. Additionally, we need to return all these fields for a form so make sure you return them:"
                        + ", ".join(EXTRACT_FIELDS)
                    },
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
        error_message = f"Gemini API Error: {response.status_code} - {response.text}"
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
        error_message = (
            f"Gemini Processing Error: Invalid JSON response - {structured_text}"
        )
        with open(output_file, "w") as file:
            file.write(error_message)
        return error_message


def main():
    st.title("Medical Document Processing with Google Vision & Gemini AI")
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
                if "Error" not in text_input:
                    st.success("Text extraction successful!")
                else:
                    st.error("No text detected. Please try another image.")

    if st.button("Extract Information"):
        if text_input and "Error" not in text_input:
            with st.spinner("Processing text with Gemini AI..."):
                extracted_info = process_text_with_gemini(text_input)
                st.subheader("Extracted Information")
                if isinstance(extracted_info, str):
                    st.error(extracted_info)
                else:
                    st.json(extracted_info)
                    json_data = json.dumps(extracted_info, indent=4)
                    json_bytes = io.BytesIO(json_data.encode("utf-8"))
                    st.download_button(
                        "Download JSON",
                        data=json_bytes,
                        file_name="extracted_information.json",
                        mime="application/json",
                    )
        else:
            st.error("Please enter text or upload an image.")


if __name__ == "__main__":
    main()
