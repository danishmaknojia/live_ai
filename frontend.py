import os
import io
import re
import streamlit as st
from PIL import Image
from google.cloud import vision, language_v1
import spacy
from spacy.pipeline import EntityRuler

# Set Google Cloud credentials (Replace with your actual credentials file path)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "/Users/danishmak/Documents/Hackathon/secretsgoogle.json"
)

# Initialize Google Cloud clients
vision_client = vision.ImageAnnotatorClient()
language_client = language_v1.LanguageServiceClient()

# Load spaCy model and define entity patterns
nlp = spacy.load("en_core_web_sm")


def add_custom_rules(nlp):
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = [
        {"label": "PATIENT_NAME", "pattern": "Sarah Smith"},
        {
            "label": "DATE_OF_BIRTH",
            "pattern": {"TEXT": {"regex": r"\b\d{1,2}/\d{1,2}/\d{4}\b"}},
        },
        {
            "label": "PHONE_NUMBER",
            "pattern": {"TEXT": {"regex": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"}},
        },
        {
            "label": "INSURANCE_PLAN",
            "pattern": {
                "TEXT": {"regex": r"(?i)(medicare|medicaid|blue\s*cross|cigna|aetna)"}
            },
        },
        {
            "label": "TOTAL_CHARGE",
            "pattern": {"TEXT": {"regex": r"\$\d{1,5}(\.\d{2})?"}},
        },
        {
            "label": "DIAGNOSIS",
            "pattern": {"TEXT": {"regex": r"(Dx:|Diagnosis:)\s*([\w\s]+)"}},
        },
    ]
    ruler.add_patterns(patterns)


add_custom_rules(nlp)

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
    "reserved_for_local_use": "",
}


def extract_text_from_image(image):
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_content = image_bytes.getvalue()
    image = vision.Image(content=image_content)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else "No text detected"


def extract_with_spacy(text):
    doc = nlp(text)
    extracted_info = {field: "" for field in EXTRACT_FIELDS}
    for ent in doc.ents:
        if ent.label_ in extracted_info:
            extracted_info[ent.label_] = ent.text
    return extracted_info


def analyze_text(text):
    extracted_info = extract_with_spacy(text)

    if not extracted_info["patient_phone"]:
        phone_match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
        if phone_match:
            extracted_info["patient_phone"] = phone_match.group()

    if not extracted_info["total_charge"]:
        amount_match = re.search(r"\$\d+(\.\d{2})?", text)
        if amount_match:
            extracted_info["total_charge"] = amount_match.group()

    diagnosis_match = re.search(r"diagnosis:\s*([\w\s]+)", text, re.IGNORECASE)
    if diagnosis_match:
        extracted_info["diagnosis"] = diagnosis_match.group(1)

    return extracted_info


def main():
    st.title("CMS-1500 Form Filler Using Google Cloud NLP & Vision API + spaCy NER")
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
                if text_input.strip():
                    st.success("Text extraction successful!")
                else:
                    st.error("No text detected. Please try another image.")
    if st.button("Extract Information"):
        if text_input:
            info = analyze_text(text_input)
            st.subheader("Extracted Information")
            for key, value in info.items():
                st.text_input(key.replace("_", " ").title(), value)
        else:
            st.error("Please enter text or upload an image.")


if __name__ == "__main__":
    main()
