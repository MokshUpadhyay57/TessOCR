
import streamlit as st


def main():
    global file_name
    st.set_page_config(layout="wide", page_title="Download OCR Text")
    col1, col2 = st.columns([0.4, 0.5], gap="medium")
    download_format = col1.selectbox(label="Select a Option", options=["Plain Text (TXT)", "PDF", "Word Document (DOCX)"])

    # Retrieve OCR text from session state
    ocr_text = st.session_state['ocr_text']
    # Display the OCR text
    if ocr_text:
        st.subheader("Here is the OCR text")
        st.write(ocr_text)

        custom_file_name = col2.text_input("Enter custom file name:")

        # Determine file name and MIME type based on selected format
        # Determine file name and MIME type based on selected format
        if download_format == "Plain Text (TXT)":
            file_extension = ".txt"
            mime_type = "text/plain"
        elif download_format == "PDF":
            file_extension = ".pdf"
            mime_type = "application/pdf"
        elif download_format == "Word Document (DOCX)":
            file_extension = ".docx"
            mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        file_name = custom_file_name + file_extension
        # Download button
        col2.download_button(
                label="Download",
                data=ocr_text,
                file_name=file_name,
                mime=mime_type,
        )


if __name__ == "__main__":
    main()
