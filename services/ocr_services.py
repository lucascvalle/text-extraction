# services/ocr_services.py
import pytesseract
from PIL import Image
from datetime import datetime
import uuid
import re


def process_image(image_file: str) -> dict:
    """
    Realiza a extração de texto de uma imagem usando OCR (Tesseract).
    """
    try:
        image = Image.open(image_file)
        extracted_text = pytesseract.image_to_string(image)
        response = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "message": "Text extracted successfully",
            "text": extracted_text,
        }
    except Exception as e:
        response = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "message": f"Error extracting text: {str(e)}",
            "text": "",
        }
    return response


def extract_fields(text: str, nome: str = "", cpf: str = "") -> dict:
    found_nome = nome.lower() in text.lower() if nome else False
    found_cpf = False
    cpf_regex = r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"

    if cpf:
        matches = re.findall(cpf_regex, text)
        found_cpf = any(cpf.replace(".", "").replace("-", "") in m.replace(".", "").replace("-", "") for m in matches)

    return {
        "nome_match": found_nome,
        "cpf_match": found_cpf
    }
