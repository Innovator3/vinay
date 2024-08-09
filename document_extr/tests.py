from django.test import TestCase
import google.generativeai as genai
import base64
import io
import fitz
import os


api_key = "AIzaSyDygyBDJftTOf0BqhUiI36gdtvNEL97Dgo"
genai.configure(api_key=api_key)


def input_image_setup(uploaded_file):
    bytes_data = uploaded_file.read()
    image_parts = {
        "mime_type": uploaded_file.content_type,
        "data": base64.b64encode(bytes_data).decode("utf-8"),
    }
    return image_parts


def dymanic_path(*args):

    current_directory = os.getcwd()
    dir = os.path.join(current_directory, *args)
    return dir


def delete_all_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    return "Deleted"


def get_gemini_response(image_data=None, ocr_content=None):

    gemini_prompt = """
                You are an expert in analyzing US mortgage documents like Deed, Deed of Trust, Mortgage, Satisfaction of Mortgage, and Release.
                Upon receiving an input, which can be either an image or text of one of these documents, you are to:
                1. Classify the document type and provide a confidence score for the classification.
                2. Based on the document type, extract detailed information, if present, including:
                    - Buyer first name and its confidence score.
                    - Buyer last name and its confidence score.
                    - Buyer address, city, and zipcode, each with its own confidence score.
                    - Seller first name and its confidence score.
                    - Seller last name and its confidence score.
                    - Seller address, city, and zipcode, each with its own confidence score.
                    - Property address, Lot, and Block, each with its own confidence score.
                If any detail is not found within the document, clearly indicate it as "Not found in the document" and provide a confidence score for this assertion as well.
                Your response should be structured in JSON format, ensuring each extracted value is paired with a corresponding confidence score. For example:
                {
                    "DocumentType": "Mortgage", "DocumentTypeConfidence": 0.95,
                    "Buyer": {
                    "FirstName": "John", "FirstNameConfidence": 0.90,
                    "LastName": "Doe", "LastNameConfidence": 0.92,
                    "Address": "123 Elm St", "AddressConfidence": 0.88,
                    "City": "Springfield", "CityConfidence": 0.87,
                    "Zipcode": "12345", "ZipcodeConfidence": 0.89
                    },
                    "Seller": {
                    "FirstName": "Jane", "FirstNameConfidence": 0.91,
                    "LastName": "Smith", "LastNameConfidence": 0.93,
                    "Address": "456 Oak St", "AddressConfidence": 0.90,
                    "City": "Shelbyville", "CityConfidence": 0.92,
                    "Zipcode": "67890", "ZipcodeConfidence": 0.94
                    },
                    "PropertyDetails": {
                    "Address": "789 Pine St", "AddressConfidence": 0.95,
                    "Lot": "12", "LotConfidence": 0.93,
                    "Block": "3", "BlockConfidence": 0.94
                    }
                }
                This detailed extraction, complete with confidence scores, aids in ensuring the precision and reliability of the data extracted from the mortgage documents.
                """

    model_name = "gemini-pro-vision" if image_data else "gemini-pro"
    model = genai.GenerativeModel(model_name)

    content = image_data if image_data else {"text": ocr_content}
    response = model.generate_content([gemini_prompt, content])

    return response.text


def extract_pdf_text(pdf_content):

    pdf_file = io.BytesIO(pdf_content)

    doc = fitz.open(stream=pdf_file, filetype="pdf")
    text = ""
    for page in doc:
        pix = page.get_pixmap(dpi=150)
        text += page.get_text()
        pix.save(dymanic_path("static", "images", f"page-%04i.png" % page.number))

    doc.close()
    return text
