
import google.generativeai as gen
import os
from dotenv import load_dotenv
load_dotenv()
gen.configure(api_key=os.getenv("Gem-api-key"))
text_model=gen.GenerativeModel("gemini-2.5-flash")
image_model=gen.GenerativeModel("gemini-2.5-flash")

for m in gen.list_models():
    print(m.name)

Max_prompt=4000

def build_prompt(extracted_content,user_prompt):
    """
    Build structured prompt for gemini
    """
    clean_content=extracted_content[:Max_prompt]

    formetted_promt=f"""
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
        response=text_model.generate_content(promt)
        return response.text
    except Exception as e:
        return f"Errror genrating response:{str(e)}"


def generate_image_response(image,user_prompt):
    """
    send image+instruction to gemini

    """
    try:
        response=image_model.generate_content([user_prompt,image])
        return response.text
    except Exception as e:
        return f"Error genrating image response:{str(e)}"