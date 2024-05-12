import pytesseract
import streamlit as st
from PIL import Image
import time

Segmentation_modes = {"Automatic": 3, "Single Column": 4, "Uniform Block of Text": 6}
Languages = {"English": "eng", "Hindi": "hin", "Assamese": "asm", "Bengali": "ben"}
Engine_mode = {"LSTM": 1, "Legacy + LSTM": 3}


def file_upload():
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        column1.image(img, caption="Uploaded Image")
        return img


def ocr_image(img, lang, engine_mode, segmentation_modes):
    tess_dir = r"/home/moksh/Desktop/Tesseract_Training/tesseract/tessdata"
    config = f'--tessdata-dir {tess_dir} --psm {segmentation_modes} --oem {engine_mode}'
    txt = pytesseract.image_to_string(img, config=config, lang=lang)
    return txt


def detect_script(img):
    tess_dir = r"/home/moksh/Desktop/Tesseract_Training/tesseract/tessdata"
    config = f'--tessdata-dir {tess_dir} --psm 0'
    osd = pytesseract.image_to_osd(img, config=config)
    for line in osd.splitlines():
        if line.startswith('Script: '):
            script = line.split(':')[1].strip()
            print(line)
        if line.startswith('Rotate'):
            r = line.split(':')[1].strip()
            print(line)
    return script, r


st.set_page_config(layout="wide", page_title="OCR Using Tesseract OCR")
col1, col2, col3 = st.columns([0.7, 0.6, 0.8])
selected_lang = col1.selectbox(label="Language", options=Languages.keys())
selected_engine = col2.selectbox(label="Engine", options=Engine_mode.keys())
selected_segmentation = col3.selectbox(label="Segmentation Mode", options=Segmentation_modes.keys())

c1, c2 = col1.columns([0.5, 0.5], gap="medium")
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
column1, column2 = st.columns([0.5, 0.5], gap="medium")

with column1:
    image = file_upload()
with column2:
    if c1.button("Recognize Text", type="primary", use_container_width=True):
        with st.spinner('Performing OCR...'):
            text = ocr_image(image,
                             Languages[selected_lang],
                             Engine_mode[selected_engine],
                             Segmentation_modes[selected_segmentation])
            time.sleep(5)  # Simulate processing time
            column2.write(text)

            if "ocr_text" not in st.session_state:
                st.session_state.ocr_text = text

with column2:
    if c2.button("Detect Script", use_container_width=True):
        with st.spinner('Detecting script...'):
            script, rotation = detect_script(image)
            time.sleep(2)  # Simulate processing time
            column2.write("The detected script in the image is " + script)
            column2.write(f"The detected rotation in the image is {rotation} degree")
