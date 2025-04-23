# main.py
from fastapi import FastAPI, File, UploadFile, Form
import requests
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil
import os
import uuid
from services.ocr_services import process_image, extract_fields

app = FastAPI()
UPLOAD_DIR = "./uploads"

# Garantir que a pasta de uploads exista
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.post("/upload/")
async def upload_image(
        file: UploadFile = File(...),
        search_nome: str = Form(""),
        search_cpf: str = Form("")
):
    #contents = await file.read()
    #return JSONResponse(content={"filename": file.filename, "message": "Success"})
    
    # Salvar arquivo temporariamente
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Processar a imagem para OCR
    ocr_result = process_image(file_path)
    filtered_data = extract_fields(ocr_result["text"], search_nome, search_cpf)
    # Remover arquivo temporário após uso
    os.remove(file_path)
    
    return JSONResponse(content={
        "ocr": ocr_result,
        "matched_data": filtered_data
    })

@app.post("/upload-url/")
async def upload_from_url(image_url: str, search_nome: str = "", search_cpf: str = ""):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            return JSONResponse(content={"error": "Erro ao baixar imagem"}, status_code=400)

        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.jpg")
        with open(file_path, "wb") as f:
            f.write(response.content)

        ocr_result = process_image(file_path)
        filtered_data = extract_fields(ocr_result["text"], search_nome, search_cpf)

        os.remove(file_path)

        return JSONResponse(content={
            "ocr": ocr_result,
            "matched_data": filtered_data
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)