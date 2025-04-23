# 📄 Text Extraction API (OCR) — FastAPI + Tesseract + Docker

Este projeto é uma API RESTful feita com **FastAPI** que utiliza **Tesseract OCR** para extrair texto de imagens.  
Permite o envio de arquivos ou URLs de imagens, realizando a leitura OCR e retornando o texto extraído — com opção de filtrar por nome ou CPF.

---

## 🚀 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Docker](https://www.docker.com/)
- Python 3.9

---

## 🧪 Endpoints disponíveis

### `POST /upload/`

Envia uma imagem diretamente para extração de texto (upload local).

**Exemplo com `curl`:**

```bash
curl -X POST "http://127.0.0.1:5005/upload/" -F "file=@pagina1.png"
```

---

### `POST /upload-url/`

Envia uma **URL de imagem** e opcionalmente parâmetros `search_nome` e `search_cpf`.

**Exemplo com `curl`:**

```bash
curl -X POST "http://127.0.0.1:5005/upload-url/" \
  -d "image_url=https://i.ibb.co/35L33Rtz/documento.png" \
  -d "search_nome=" \
  -d "search_cpf="
```

---

## 🐳 Docker

### 🔧 Build da imagem

```bash
docker build -t text-extraction-img .
```

### ▶️ Executar o container

```bash
docker run -p 5005:5000 --name text-extraction-ctn text-extraction-img
```

A aplicação estará disponível em:

```
http://127.0.0.1:5005
```

---

## 🧰 Requisitos

- Docker (ou Python 3.9+ com pip)
- Se for rodar localmente sem Docker, instale o Tesseract:
  
  **Ubuntu:**
  ```bash
  sudo apt install tesseract-ocr
  ```

  **MacOS:**
  ```bash
  brew install tesseract
  ```

---

## 📂 Estrutura do Projeto

```
.
├── main.py
├── requirements.txt
├── Dockerfile
├── /services
│   └── ocr_services.py
├── /uploads
└── README.md
```

---

## 📑 Exemplo de Resposta

```json
{
  "ocr": {
    "id": "f83c33e9-8a92-4e22-91c1-f834f0b6a126",
    "timestamp": "2025-04-16T15:38:21.123Z",
    "message": "Text extracted successfully",
    "text": "extracted text"
  },
  "matched_data": {
    "nome": "false",
    "cpf": "false"
  }
}
```

---

## ✍️ Autor

Desenvolvido por [@pfrolim](https://github.com/pfrolim) e [@lucascvalle](https://github.com/lucascvalle)

---
