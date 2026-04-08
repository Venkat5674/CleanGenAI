FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 7860 to match Hugging Face's requirements
EXPOSE 7860

# Run the FastAPI server natively required for OpenEnv grading
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]