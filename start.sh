#!/bin/bash
# Start FastAPI backend (Port 8000)
uvicorn server.app:app --host 127.0.0.1 --port 8000 &

# Start Streamlit frontend (Port 8501)
streamlit run app.py --server.port 8501 --server.address 127.0.0.1 --server.enableCORS false &

# Start Nginx (Port 7860, exposed to outside)
nginx -g "daemon off;"
