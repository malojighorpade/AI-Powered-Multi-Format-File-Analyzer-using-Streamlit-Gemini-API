from google import genai as gen
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Create client instead of configure (new SDK way)
client = gen.Client(api_key=st.secrets["GEMINI_API_KEY"])

text_model = "gemini-2.5-flash"
image_model = "gemini-2.5-flash"


Max_prompt = 4000

def build_prompt(extracted_content, user_prompt):
    """
    Build structured prompt for gemini
    """
    clean_content = extracted_content[:Max_prompt]

    formetted_promt = f"""
You are an AI file analysis assisitent .format User INstruction:
{user_prompt}
File_content:
{clean_content}
Instruction:
-Analyze the file content carefully.
-provide a clear ,structured response.
-ID data is tebular,summarise insights.
-if text,explain key points
"""
    return formetted_promt.strip()


def generate_text_response(promt):
    """
    send structured promt to gemini
    and return clean response text
    """
    try:
        response = client.models.generate_content(
            model=text_model,
            contents=promt
        )
        return response.text
    except Exception as e:
        return f"Errror genrating response:{str(e)}"


def generate_image_response(image, user_prompt):
    """
    send image+instruction to gemini
    """
    try:
        response = client.models.generate_content(
            model=image_model,
            contents=[user_prompt, image]
        )
        return response.text
    except Exception as e:
        return f"Error genrating image response:{str(e)}"
