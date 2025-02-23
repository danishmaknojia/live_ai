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
#     st.title("Medical Document Processing with Google Vision & Gemini AI")
#     input_option = st.radio("Select Input Method", ("Text", "Image"))
#     text_input = ""
#     extracted_info = False

#     if input_option == "Text":
#         text_input = st.text_area("Enter medical form text:")
#     elif input_option == "Image":
#         image_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
#         if image_file:
#             image = Image.open(image_file)
#             st.image(image, caption="Uploaded Image", use_column_width=True)
#             with st.spinner("Extracting text..."):
#                 text_input = extract_text_from_image(image)
#                 if "Error" not in text_input:
#                     st.success("Text extraction successful!")
#                 else:
#                     st.error("No text detected. Please try another image.")

#     if st.button("Extract Information"):
#         if text_input and "Error" not in text_input:
#             with st.spinner("Processing text with Gemini AI..."):
#                 extracted_info = process_text_with_gemini(text_input)
#                 st.subheader("Extracted Information")

#                 if extracted_info:
#                     with st.spinner("Generating PDF..."):
#                         subprocess.run(
#                             ["python", "makepdf.py"], check=True
#                         )  # Run makepdf.py to generate PDF
#                     st.success("PDF generated successfully!")

#                     pdf_path = "filled_claimform.pdf"

#                     # Show a button to preview the PDF
#                     if os.path.exists(pdf_path):
#                         st.subheader("Processed Claim Form Preview")
#                         display_pdf(pdf_path)

#                         # Provide a download button
#                         with open(pdf_path, "rb") as pdf_file:
#                             pdf_bytes = pdf_file.read()
#                         st.download_button(
#                             label="Download PDF",
#                             data=pdf_bytes,
#                             file_name="filled_claimform.pdf",
#                             mime="application/pdf",
#                         )


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
from analysis import *  # Import the analysis module


def main():
    st.title("Medical Document Processing with Google Vision & Gemini AI")
    input_option = st.radio("Select Input Method", ("Text", "Image"))
    text_input = ""
    extracted_info = False

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

                if extracted_info:
                    with st.spinner("Generating PDF..."):
                        subprocess.run(
                            ["python", "makepdf.py"], check=True
                        )  # Run makepdf.py to generate PDF
                    st.success("PDF generated successfully!")

                    pdf_path = "filled_claimform.pdf"

                    # Show a button to preview the PDF
                    if os.path.exists(pdf_path):
                        st.subheader("Processed Claim Form Preview")
                        display_pdf(pdf_path)

                        # Provide a download button
                        with open(pdf_path, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()
                        st.download_button(
                            label="Download PDF",
                            data=pdf_bytes,
                            file_name="filled_claimform.pdf",
                            mime="application/pdf",
                        )

                    # Adding the claim approval/denial reasoning here

                st.subheader("Claim Feedback")
                with st.spinner("Generating Insights..."):
                    # Run analysis.py as a subprocess and capture the output

                    result = analysis()

                    # Display the result in Streamlit

                    st.markdown(result)

        else:
            st.error("Please enter text or upload an image.")


if __name__ == "__main__":
    main()
