# import os
# import base64
# import io
# import json
# import streamlit as st
# from PIL import Image
# from helper import *
# from makepdf import *
# import subprocess
# from analysis import *


# def main():
#     st.set_page_config(
#         page_title="Medical Document Processor", page_icon="🏥", layout="centered"
#     )
#     st.title("🏥 Medical Document Processing")
#     st.markdown(
#         "Effortlessly extract, analyze, and process medical documents using Computer Vision & Generative AI."
#     )
#     st.markdown(
#         "This app allows users to upload medical documents in text or image format, extract key details using AI-powered tools, generate structured reports, and receive claim feedback insights."
#     )

#     # Sidebar for input selection
#     st.sidebar.header("Input Options")
#     input_option = st.sidebar.radio("Select Input Method", ("Text", "Image"))
#     text_input = ""
#     extracted_info = None

#     # Input section
#     st.subheader("Upload or Enter Details")
#     if input_option == "Text":
#         text_input = st.text_area("Enter medical form text:", height=150)
#     elif input_option == "Image":
#         image_file = st.file_uploader(
#             "Upload an Image",
#             type=["jpg", "jpeg", "png"],
#             help="Supports JPG, JPEG, PNG formats",
#         )
#         if image_file:
#             image = Image.open(image_file)
#             st.image(image, caption="Uploaded Image", use_column_width=True)
#             with st.spinner("Extracting text from image..."):
#                 text_input = extract_text_from_image(image)
#                 if "Error" not in text_input:
#                     st.success("Text extracted successfully!")
#                 else:
#                     st.error("No text detected. Please try another image.")

#     # Process button
#     if st.button("Extract & Analyze Information", use_container_width=True):
#         if text_input and "Error" not in text_input:
#             with st.spinner("Processing text with Gemini AI..."):
#                 extracted_info = process_text_with_gemini(text_input)
#                 st.subheader("📄 Extracted Information")
#                 # st.write(
#                 #     extracted_info
#                 #     if extracted_info
#                 #     else "No relevant details extracted."
#                 # )

#                 if extracted_info:
#                     with st.spinner("Generating PDF..."):
#                         subprocess.run(["python", "makepdf.py"], check=True)

#                     pdf_path = "filled_claimform.pdf"
#                     if os.path.exists(pdf_path):
#                         st.subheader("📝 Processed Claim Form Preview")
#                         display_pdf(pdf_path)
#                         with open(pdf_path, "rb") as pdf_file:
#                             pdf_bytes = pdf_file.read()
#                         st.download_button(
#                             label="💾 Download Processed PDF",
#                             data=pdf_bytes,
#                             file_name="filled_claimform.pdf",
#                             mime="application/pdf",
#                         )

#                 # Claim feedback analysis
#                 st.subheader("📝 Claim Feedback")
#                 with st.spinner("Generating insights..."):
#                     result = analysis()
#                     st.markdown(result)
#         else:
#             st.error("Please enter text or upload an image.")


# if __name__ == "__main__":
#     main()

import os
import base64
import io
import json
import streamlit as st
from PIL import Image
from helper import *
from makepdf import *
import subprocess
from analysis import *


def main():
    st.set_page_config(
        page_title="MedClaimVerify - Medical Document Processor",
        page_icon="🏥",
        layout="centered",
    )

    # Display logo in the top left and brand name
    logo_path = "images/logo.jpeg"
    col1, col2 = st.columns([1, 4])
    with col1:
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            st.image(logo, width=100)
    with col2:
        st.title("MedClaimVerify 🏥")

    st.markdown(
        "<h2>Effortlessly extract, analyze, and process medical documents using AI.</h2>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "This app helps users upload medical documents (text or image), extract key details using AI, generate structured reports, and receive claim feedback insights.",
        help="Supports accessibility features such as keyboard navigation and screen reader compatibility.",
    )

    # Sidebar for input selection
    st.sidebar.header("Input Options")
    input_option = st.sidebar.radio("Select Input Method", ("Text", "Image"), index=0)
    text_input = ""
    extracted_info = None

    # Input section
    st.subheader("Upload or Enter Details")
    if input_option == "Text":
        text_input = st.text_area(
            "Enter medical form text:",
            height=150,
            help="Use plain text for better extraction accuracy.",
        )
    elif input_option == "Image":
        image_file = st.file_uploader(
            "Upload an Image",
            type=["jpg", "jpeg", "png"],
            help="Supports JPG, JPEG, PNG formats. Ensure text is clearly visible for best results.",
        )
        if image_file:
            image = Image.open(image_file)
            st.image(
                image,
                caption="Uploaded Image: AI will extract text from this.",
                use_column_width=True,
            )
            with st.spinner("Extracting text from image..."):
                text_input = extract_text_from_image(image)
                if text_input.strip():
                    st.success("Text extracted successfully!")
                else:
                    st.error("No text detected. Try another image with clearer text.")

    # Process button with keyboard navigation support
    if st.button(
        "Extract & Analyze Information",
        use_container_width=True,
        help="Click or press Enter to process data.",
    ):
        if text_input.strip():
            with st.spinner("Processing text with AI..."):
                extracted_info = process_text_with_gemini(text_input)

                # st.subheader("📄 Extracted Information")
                # if extracted_info:
                #     st.text_area(
                #         "Processed Data:",
                #         extracted_info,
                #         height=200,
                #         help="Review extracted information before generating the claim form.",
                #     )

                # Confirmation before generating PDF
                if extracted_info:
                    with st.spinner("Generating PDF..."):
                        subprocess.run(["python", "makepdf.py"], check=True)

                        pdf_path = "filled_claimform.pdf"
                        if os.path.exists(pdf_path):
                            st.subheader("📝 Processed Claim Form Preview")
                            display_pdf(pdf_path)
                            with open(pdf_path, "rb") as pdf_file:
                                pdf_bytes = pdf_file.read()
                            st.download_button(
                                label="💾 Download Processed PDF",
                                data=pdf_bytes,
                                file_name="filled_claimform.pdf",
                                mime="application/pdf",
                            )

                    # if st.checkbox("Confirm and generate claim form PDF"):
                    #     with st.spinner("Generating PDF..."):
                    #         subprocess.run(["python", "makepdf.py"], check=True)
                    #         pdf_path = "filled_claimform.pdf"
                    #         if os.path.exists(pdf_path):
                    #             st.subheader("📝 Processed Claim Form Preview")
                    #             display_pdf(pdf_path)
                    #             with open(pdf_path, "rb") as pdf_file:
                    #                 pdf_bytes = pdf_file.read()
                    #             st.download_button(
                    #                 label="💾 Download Processed PDF",
                    #                 data=pdf_bytes,
                    #                 file_name="filled_claimform.pdf",
                    #                 mime="application/pdf",
                    #                 help="Download your claim form for submission.",
                    #             )

                # Claim feedback analysis
                st.subheader("📝 Claim Feedback")
                with st.spinner("Generating insights..."):
                    result = analysis()
                    st.markdown(result)
        else:
            st.error("Please enter text or upload an image.")

    st.markdown(
        """
    <div style="text-align: center;">
        <h2>Why Choose MedClaimVerify?</h2>
    </div>
    <div style="display: flex; justify-content: space-around;">
        <div style="width: 30%; padding: 10px; border-radius: 10px; background-color: transparent;">
            <h3>🏆 The Best Medical Claim Automation Tool</h3>
            <p>Whether you need to extract data from medical forms, validate claim accuracy, or generate a CMS-1500 form, 
            our AI-powered platform ensures seamless claim automation.</p>
        </div>
        <div style="width: 30%; padding: 10px; border-radius: 10px; background-color: transparent;">
            <h3>🤖 Smart Automation & AI Validation</h3>
            <p>Our advanced AI extracts patient and billing details from uploaded documents, filling out claim forms automatically 
            and validating accuracy in real-time.</p>
        </div>
        <div style="width: 30%; padding: 10px; border-radius: 10px; background-color: transparent;">
            <h3>🔒 Safe & Hassle-Free Processing</h3>
            <p>All information remains secure and is not stored after processing, ensuring a private and smooth claim submission experience.</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
