FROM python:3.10-slim

WORKDIR /app

# Install nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uv

COPY . .

# Setup Nginx
COPY nginx.conf /etc/nginx/nginx.conf
RUN chmod +x start.sh

# Expose port 7860 to match Hugging Face's requirements
EXPOSE 7860

# Run the Nginx proxy routing to FastAPI and Streamlit
CMD ["./start.sh"]