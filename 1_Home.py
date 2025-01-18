import streamlit as st


def main():
    st.set_page_config(layout="wide", page_title="TessOCR: OCR Using Tesseract OCR", page_icon=":computer:")
    st.title("Welcome to TessOCR")

    # Introduction
    st.write("""
        TessOCR simplifies Optical Character Recognition (OCR) using the Tesseract OCR engine. 
        Easily extract text from images for various tasks like document digitization and text analysis. 
        With a user-friendly interface, TessOCR makes interacting with text content seamless.
    """)

    # Visual Elements
    st.image("images/tess_ocr.png", use_container_width=True)

    # Key Features
    st.header("Key Features")
    st.markdown("""
        - **User-Friendly Interface:** Upload images and start OCR with a few clicks.
        - **Flexible Input Options:** Supports JPG, JPEG, and PNG formats.
        - **Customization:** Customize OCR settings like language and segmentation mode.
        - **Script Detection:** Detect languages for multilingual OCR tasks.
        - **Real-time Feedback:** Get instant feedback on text extraction progress.
    """)

    # How It Works
    st.header("How It Works")
    st.markdown("""
        1. **Upload Image:** Select an image with text.
        2. **Configure OCR Settings:** Customize language and segmentation mode if needed.
        3. **Initiate OCR:** Click 'Recognize Text' to start the process.
        4. **Review Results:** View extracted text and detected languages in real-time.
        5. **Download Text:** Optionally download the extracted text as a text file.
    """)

    st.write("\n\n")

    # Button to navigate to another page
    if st.button("Start Your OCR Journey - Upload Your File Now!", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Recognize.py")
        st.session_state.page = "Upload"


main()
