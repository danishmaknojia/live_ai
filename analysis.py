# import os
# import google.generativeai as genai


# def configure_gemini_api():
#     """Configures Google Gemini API using the environment variable for the API key."""
#     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#     genai.configure(api_key=GEMINI_API_KEY)


# def load_query_string(file_path):
#     """Loads the query string from a file."""
#     with open(file_path, "r") as file:
#         query_string = file.read()
#     return query_string


# def create_generative_model():
#     """Creates and configures the generative model."""
#     generation_config = {
#         "temperature": 1,
#         "top_p": 0.95,
#         "top_k": 40,
#         "max_output_tokens": 8192,
#         "response_mime_type": "text/plain",
#     }

#     model = genai.GenerativeModel(
#         model_name="gemini-2.0-flash",
#         generation_config=generation_config,
#         system_instruction="You are a health insurance claim expert",
#     )
#     return model


# def start_chat_session(model, query_string):
#     """Starts a chat session with the model."""
#     chat_session = model.start_chat(
#         history=[
#             {
#                 "role": "user",
#                 "parts": [
#                     f"This is my data that im filling in the CMS1500 claim form:\n{query_string}\n In a single sentence tell me if I'm at a higher risk of not getting approved. if so then why?",
#                 ],
#             },
#             {
#                 "role": "model",
#                 "parts": [
#                     "Based on the provided data, you are at a higher risk of claim denial due to inconsistencies and missing information, particularly regarding the insured's details and the relationships between the patient and insured, as well as other fields like Tax ID. Make sure your answer is a single sentence\n",
#                 ],
#             },
#         ]
#     )
#     return chat_session


# def get_response(chat_session, query_string):
#     """Sends the query string to the chat session and retrieves the response."""
#     response = chat_session.send_message(query_string)
#     return response.text


# def main(file_path):
#     """Main function to process the claim form and get the model response."""
#     configure_gemini_api()
#     query_string = load_query_string(file_path)
#     model = create_generative_model()
#     chat_session = start_chat_session(model, query_string)
#     response = get_response(chat_session, query_string)
#     return response


# if __name__ == "__main__":
#     file_path = "/Users/danishmak/Documents/Hackathon/gemini_response.txt"
#     main(file_path)

import os
import pandas as pd
import google.generativeai as genai
from langchain.vectorstores import Chroma
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import faiss


def analysis():
    # Set Google Gemini API Key
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)

    # Load the gemini_response.txt as a query string
    with open("gemini_response.txt", "r") as file:
        query_string = file.read()

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
        system_instruction="You are a health insurance claim expert",
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    """This is my data that im filling in the CMS1500 claim form:{
    "insured_name": "John Doe",
    "insured_address": null,
    "insured_city": null,
    "insured_state": null,
    "insured_zip": null,
    "insurance_programs": {
        "Medicare": null,
        "Medicaid": null,
        "CHAMPUS": null,
        "CHAMPVA": null,
        "Group_Health_Plan": null,
        "FECA Black_Lung": null,
        "Other": null
    },
    "patient_name": "Jane Doe",
    "patient_birth_date": "02-14-1985",
    "patient_sex": "M",
    "patient_address": "789 Oak Ave",
    "patient_city": "Los Angeles",
    "patient_state": "CA",
    "patient_zip": "90001",
    "patient_phone": "555-123-4567",
    "patient_relationship": null,
    "patient_status": null,
    "other_insured_name": "Mike Johnson",
    "other_insured_policy": "G123456789",
    "other_insured_birth_date": null,
    "other_insured_sex": null,
    "other_insured_employer": null,
    "other_insured_insurance_plan": "XYZ Health",
    "other_insured_reserved_use": null,
    "condition_employment": null,
    "condition_auto_accident": null,
    "condition_auto_accident_place": null,
    "condition_other_accident": null,
    "Date_of_Current_Illness_Injury_or_Pregnancy": "02-01-2024",
    "First_Date_of_Similar_Illness": null,
    "Dates_Patient_Unable_to_Work_From": null,
    "Dates_Patient_Unable_to_Work_To": null,
    "Referring_Physician_Name": "Dr. Emily Brown",
    "Referring_Physician_ID": "MD67890",
    "Hospitalization_Dates_From": null,
    "Hospitalization_Dates_To": null,
    "Outside_Lab": null,
    "Charges": null,
    "Medicaid_Resubmission_Code": null,
    "Original_Reference_Number": null,
    "Prior_Authorization_Number": null,
    "Diagnosis_1": "Flu (J11.1)",
    "Diagnosis_2": "Fever",
    "Diagnosis_3": "Cough",
    "Diagnosis_4": null,
    "Date_of_Service_From": "02-07-2024",
    "Date_of_Service_To": "02-07-2024",
    "Place_of_Service": "Clinic",
    "Type_of_Service": null,
    "Procedures_CPT_HCPCS_Modifier": "99214",
    "Diagnosis_Code": null,
    "Procedure_Charges": "250",
    "Days_or_Units": null,
    "EPSDT_or_Family_Plan": null,
    "EMG": null,
    "COB": null,
    "Reserved_for_Local_Use": null,
    "Federal_Tax_ID": null,
    "Patient_Account_Number": null,
    "Accept_Assignment": null,
    "Total_Charge": "1500",
    "Amount_Paid": "200",
    "Balance_Due": "1300",
    "Physician_Supplier_Signature": null,
    "Signed_Date": null,
    "Facility_Name_and_Address": "HealthCare Center, 123 Wellness St",
    "Physician_Supplier_Billing_Name_and_Address": "Dr. Emily Brown, MD",
    "PIN": null,
    "Group_Number": "G345678901",
    "signed_date": null,
    "Insured_ID_Number": "A987654321",
    "Telephone": null,
    "Insured_Policy_Group_or_FECA_Number": null,
    "Insured_Birth_Date": null,
    "Sex": null,
    "Employer_or_School_Name": null,
    "Insurance_Plan_Name": "Blue Shield",
    "Another_Health_Benefit_Plan": null,
    "Insured_or_Authorized_Person_Signature": null
    }  In a single sentence tell me if I'm at a higher risk of not getting approved. if so then why?", """
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Based on the provided data, you are at a higher risk of claim denial due to inconsistencies and missing information, particularly regarding the insured's details and the relationships between the patient and insured, as well as other fields like Tax ID. Make sure your answer is a single sentence\n",
                ],
            },
        ]
    )

    response = chat_session.send_message(
        f"This is my data that im filling in the CMS1500 claim form:\n{query_string}\n In a single sentence tell me if I'm at a higher risk of not getting approve. if so then why?"
    )

    return response.text
