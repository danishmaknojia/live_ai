import os
import subprocess
import streamlit as st
from PIL import Image
from helper import *
from makepdf import *
from analysis import *
import base64
from io import BytesIO
import warnings

warnings.filterwarnings("ignore")


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()


def main():
    st.set_page_config(
        page_title="MedClaimVerify - Medical Document Processor",
        page_icon="🏥",
        layout="centered",
    )

    # Display logo and brand name
    logo_path = "images/logo.jpeg"
    col1, col2 = st.columns([1, 4])

    with col1:
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            # Create a clickable link around the logo
            st.markdown(
                f'<a href="/" target="_self"><img src="data:image/jpeg;base64,{image_to_base64(logo)}" width="100" /></a>',
                unsafe_allow_html=True,
            )
    with col2:
        st.title("MedClaimVerify 🏥")

    # Define the current page in session_state (to simulate page navigation)
    if "page" not in st.session_state:
        st.session_state.page = "Home"  # Default page

    # Select which "page" to show using session_state
    if st.session_state.page == "Home":
        # Home page - Upload and enter details
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
        input_option = st.sidebar.radio(
            "Select Input Method", ("Text", "Image"), index=0
        )
        text_input = ""

        # Input section
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
                    use_container_width=True,
                )
                with st.spinner("Extracting text from image..."):
                    text_input = extract_text_from_image(image)
                    if text_input.strip():
                        st.success("Text extracted successfully!")
                    else:
                        st.error(
                            "No text detected. Try another image with clearer text."
                        )

        # Button for navigation to processing
        if st.button("Extract & Analyze Information"):
            if text_input.strip():
                st.session_state.text_input = text_input
                st.session_state.page = (
                    "Process Information"  # Set the page state to 'Process Information'
                )
            else:
                st.error("Please enter text or upload an image.")

        # Display content at the bottom of the first page
        st.markdown(
            """
    <div style="text-align: center; padding-top: 40px; padding-bottom: 20px;">
        <h2>Why Choose MedClaimVerify?</h2>
    </div>
    <div style="display: flex; justify-content: space-around; padding: 20px; border: 2px solid #ccc; border-radius: 10px; background-color: transparent;">
        <div style="width: 30%; padding: 15px; border-radius: 10px; background-color: transparent;">
            <h3>🏆 The Best Medical Claim Automation Tool</h3>
            <p>Whether you need to extract data from medical forms, validate claim accuracy, or generate a CMS-1500 form, 
            our AI-powered platform ensures seamless claim automation.</p>
        </div>
        <div style="width: 30%; padding: 15px; border-radius: 10px; background-color: transparent;">
            <h3>🤖 Smart Automation & AI Validation</h3>
            <p>Our advanced AI extracts patient and billing details from uploaded documents, filling out claim forms automatically 
            and validating accuracy in real-time.</p>
        </div>
        <div style="width: 30%; padding: 15px; border-radius: 10px; background-color: transparent;">
            <h3>🔒 Safe & Hassle-Free Processing</h3>
            <p>All information remains secure and is not stored after processing, ensuring a private and smooth claim submission experience.</p>
        </div>
    </div>
    """,
            unsafe_allow_html=True,
        )

    elif st.session_state.page == "Process Information":
        # Process Information page - Show results and generate PDF
        text_input = st.session_state.get("text_input", "")

        if text_input:
            with st.spinner("Processing text with AI..."):
                extracted_info = process_text_with_gemini(text_input)

                # Display extracted info
                # Confirmation before generating PDF
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
            st.error(
                "No text input found. Please go back and provide input in the Home page."
            )


if __name__ == "__main__":
    main()
