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
    }  In a single sentence tell me if I'm at a higher risk of not getting approved. if so then why?",Then give pointers as feedback\n """
                ],
            },
            {
                "role": "model",
                "parts": [
                    'Based on the provided data, there are several inconsistencies and missing fields that significantly increase the risk of claim denial.\n\nHere are pointers for improvement:\n\n*   *Insured Information:* Fill in all missing ⁠ insured_address ⁠, ⁠ insured_city ⁠, ⁠ insured_state ⁠, ⁠ insured_zip ⁠ fields. Make sure the data is consistent with the insurance company\'s records for John Doe. Also fill in the ⁠ Insured_Birth_Date ⁠ and ⁠ Sex ⁠ of the insured.\n*   *Patient Information:* The patient\'s sex is listed as "M" (male) while the ⁠ patient_name ⁠ is "Jane Doe", indicating a female. Correct this inconsistency to accurately reflect the patient\'s sex. ⁠ patient_relationship ⁠ and ⁠ patient_status ⁠ are missing\n*   *Insurance Information:* You have information for "Other Insured" (Mike Johnson, XYZ Health), ensure this section is completed if Jane Doe is covered under another policy. Clarify the relationship between the insured (John Doe) and the patient (Jane Doe) in the ⁠ patient_relationship ⁠ field.\n*   *Condition Information:*  If the current illness is related to employment, auto accident, or other accident, populate the corresponding fields accurately. If none apply, consider marking them as "No" or leaving them blank if appropriate.\n*   *Referring Physician Information:* Make sure you have all of the necessary NPI and taxonomy information for the referrring physician.\n*   *Diagnosis Codes:* While you have "Flu (J11.1)" as Diagnosis_1, Diagnosis_2 and Diagnosis_3 are just descriptive ("Fever," "Cough"). Replace these with appropriate ICD-10 codes for accurate billing.\n*   *Service Line Details:* The ⁠ Diagnosis_Code ⁠ field is missing for the service line (procedure 99214). You *must* link the procedure code to at least one relevant diagnosis code (Diagnosis 1, Diagnosis 2, etc.). The ⁠ Days_or_Units ⁠ field is also missing\n*   *Billing Provider Information:* Fill in ⁠ Federal_Tax_ID ⁠, ⁠ PIN ⁠, ⁠ Telephone ⁠ of provider\n*   *Assignment and Signature:* Determine if you ⁠ Accept_Assignment ⁠,  the ⁠ Physician_Supplier_Signature ⁠ and ⁠ Signed_Date ⁠ are missing.\n*   *Total Charges and Amounts:* The sum of all ⁠ Procedure_Charges ⁠ should equal the ⁠ Total_Charge ⁠. Here your listed single procedure charge is $250, but your total charge is $1500. You need to have an itemized line by line breakdown of all procedures performed for the total charge. Ensure these figures are accurate.\n*   *Dates:* Verify all dates are in the correct format (MM-DD-YYYY) and logical sequence. ⁠ signed_date ⁠ is missing.\n\nAddressing these issues will significantly improve the likelihood of claim approval.\n',
                ],
            },
        ]
    )

    response = chat_session.send_message(
        f"This is my data that im filling in the CMS1500 claim form:\n{query_string}\n In a single sentence tell me if I'm at a higher risk of not getting approve. if so then why? Then give pointers as feedback\n\n"
    )

    return response.text
