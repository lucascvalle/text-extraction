# Use a slim Python 3.9 image as base to keep the final image small
FROM python:3.9-slim

# Install Tesseract OCR and development libraries
# These are required for image text extraction
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy Python dependency list to the container
COPY requirements.txt .

# Install dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all remaining files from current directory to /app in the container
COPY . .

# Expose port 5000 for external access (used by uvicorn server)
EXPOSE 5000

# Default command to run the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

## ~ 1. Build the Docker image ~ ##
# docker build -t text-extraction-img .

## ~ 2. Run the container ~ ##
# Redirecting to port 8003 on host machine
# docker run -p 5005:5000 --name text-extraction-ctn text-extraction-img

## ~ 3. Test the API endpoint ~ ##
# curl -X POST "http://127.0.0.1:5005/upload/" -F "file=@pagina1.png"
# curl -X POST "http://homologacao.sigplac.com.br:5005/upload/" -F "file=@pagina1.png"
