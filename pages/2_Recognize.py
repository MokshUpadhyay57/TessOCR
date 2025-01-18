import io
import pytesseract
import streamlit as st
from PIL import Image
import fitz
import time
from pdf2image import convert_from_bytes

# Configure Tesseract Path
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Constants for tesseract
Segmentation_modes = {"Automatic": 3, "Single Column": 4, "Uniform Block of Text": 6}
Languages = {"English": "eng", "Hindi": "hin"}
Engine_mode = {"LSTM": 1, "Legacy + LSTM": 3}


def file_upload(uploaded_file):
    """file upload and displays uploaded images."""
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[1].lower()
        print(file_extension)
        if file_extension == "pdf":
            pdf_pages = convert_pdf_to_images(uploaded_file)
            st.session_state.pdf_images = pdf_pages
            st.success(f"PDF with {len(pdf_pages)} page(s) uploaded successfully.")
            for i, page_img in enumerate(pdf_pages):
                column1.image(page_img, caption=f"Page {i+1} of Uploaded PDF", use_container_width=True)
            return pdf_pages
        elif file_extension in ["jpg", "jpeg", "png"]:
            img = Image.open(uploaded_file)
            st.session_state.uploaded_image = img
            column1.image(img, caption="Uploaded Image")
            return img
        else:
            st.error("Unsupported file type. Please upload a PDF or an image file.")
            return None


def convert_pdf_to_images(pdf_file):
    pdf_bytes = pdf_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append(img)
    
    return images



def ocr_image(img, lang, engine_mode, segmentation_modes):
    tess_dir = r"F:/Internship/STREAMLIT/tesseract/tessdata/"
    config = f'--tessdata-dir {tess_dir} --psm {segmentation_modes} --oem {engine_mode}'
    txt = pytesseract.image_to_string(img, config=config, lang=lang)
    return txt


def detect_script(img):
    """ function to detect script """
    tess_dir = r"F:/Internship/STREAMLIT/tesseract/tessdata/"
    config = f'--tessdata-dir {tess_dir} --psm 0'
    osd = pytesseract.image_to_osd(img, config=config)
    for line in osd.splitlines():
        if line.startswith('Script: '):
            script = line.split(':')[1].strip()
            print(line)
        if line.startswith('Rotate'):
            rotation = line.split(':')[1].strip()
            print(line)
    return script, rotation


st.set_page_config(layout="wide", page_title="OCR Using Tesseract OCR")

col1, col2, col3 = st.columns([0.7, 0.6, 0.8])
selected_lang = col1.selectbox(label="Language", options=Languages.keys())
selected_engine = col2.selectbox(label="Engine", options=Engine_mode.keys())
selected_segmentation = col3.selectbox(label="Segmentation Mode", options=Segmentation_modes.keys())

c1, c2 = col1.columns([0.5, 0.5], gap="medium")
uploaded_file = st.file_uploader("Upload an image or PDF...", type=["jpg", "jpeg", "png", "pdf"])
column1, column2 = st.columns([0.5, 0.5], gap="medium")

with column1:
    image = file_upload(uploaded_file)
    
with column2:
    if c1.button("Recognize Text", type="primary", use_container_width=True):
        with st.spinner('Performing OCR...'):
            if uploaded_file is None:  # Error handling if no file uploaded
                st.write("Please upload a file before clicking 'Recognize Text'")
            else :
                if uploaded_file.type == "application/pdf":
                    all_text = ""
                    for i, image in enumerate (st.session_state.pdf_images,1):
                        text = ocr_image(image, Languages[selected_lang], Engine_mode[selected_engine], Segmentation_modes[selected_segmentation])
                        all_text += f"Page {i}:\n{text}\n\n"
                    st.session_state.ocr_text = all_text
                    column2.text_area("", all_text, height=300)
                else:
                    text = ocr_image(image, Languages[selected_lang], Engine_mode[selected_engine], Segmentation_modes[selected_segmentation])
                    st.session_state.ocr_text = text
                    column2.text_area("", text, height=300)
                

with column2:
    if c2.button("Detect Script", use_container_width=True):
        if uploaded_file is None:  # Error handling if no file uploaded
                st.write("Please upload a file before clicking 'Detect Text'")
        else:
            with st.spinner('Detecting script...'):
                script, rotation = detect_script(image)
                time.sleep(2)  # Simulate processing time
                column2.text_area("The script in the image is " + script + "\n" + "The rotation in the image is {rotation} degree", height=300)
