import pandas as pd
from PyPDF2 import PdfReader

from PIL import Image
import io
MAX_CHAR=5000

def detect_file_type(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        return "csv"

    elif file_name.endswith((".xlsx", ".xls")):
        return "excel"

    elif file_name.endswith(".pdf"):
        return "pdf"

    elif file_name.endswith((".png", ".jpg", ".jpeg")):
        return "image"

    else:
        return "unsupported"
def process_csv(file):
    df=pd.read_csv(file)

    text=df.head(350).to_string()
    return text[:MAX_CHAR]

def process_pdf(file):
    reader = PdfReader(file)

    text=""
    for i in reader.pages:
        text=text+i.extract_text()or""
    return text[:MAX_CHAR]

def process_image(file):
    image=Image.open(file)
    return image
def process_excel(file):
    df=pd.read_excel(file)
   
    text=df.head(350).to_string()
    return text[:MAX_CHAR]
