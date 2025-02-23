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
        page_title="Medical Document Processor", page_icon="🏥", layout="centered"
    )
    st.title("🏥 Medical Document Processing")
    st.markdown(
        "Effortlessly extract, analyze, and process medical documents using Google Vision & Gemini AI."
    )
    st.markdown(
        "This app allows users to upload medical documents in text or image format, extract key details using AI-powered tools, generate structured reports, and receive claim feedback insights."
    )

    # Sidebar for input selection
    st.sidebar.header("Input Options")
    input_option = st.sidebar.radio("Select Input Method", ("Text", "Image"))
    text_input = ""
    extracted_info = None

    # Input section
    st.subheader("Upload or Enter Details")
    if input_option == "Text":
        text_input = st.text_area("Enter medical form text:", height=150)
    elif input_option == "Image":
        image_file = st.file_uploader(
            "Upload an Image",
            type=["jpg", "jpeg", "png"],
            help="Supports JPG, JPEG, PNG formats",
        )
        if image_file:
            image = Image.open(image_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            with st.spinner("Extracting text from image..."):
                text_input = extract_text_from_image(image)
                if "Error" not in text_input:
                    st.success("Text extracted successfully!")
                else:
                    st.error("No text detected. Please try another image.")

    # Process button
    if st.button("Extract & Analyze Information", use_container_width=True):
        if text_input and "Error" not in text_input:
            with st.spinner("Processing text with Gemini AI..."):
                extracted_info = process_text_with_gemini(text_input)
                st.subheader("📄 Extracted Information")
                # st.write(
                #     extracted_info
                #     if extracted_info
                #     else "No relevant details extracted."
                # )

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

                # Claim feedback analysis
                st.subheader("📝 Claim Feedback")
                with st.spinner("Generating insights..."):
                    result = analysis()
                    st.markdown(result)
        else:
            st.error("Please enter text or upload an image.")


if __name__ == "__main__":
    main()
