FROM python:3.11-slim

# # Set workdir
WORKDIR /app

# # Install system dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy src directory into the container
COPY src /app/src
EXPOSE 8000 8501

# # Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

CMD ["sh", "-c", "uvicorn src.api.main:app --host 0.0.0.0 --port 8000 & streamlit run src/ui/dashboard.py --server.port=8501 --server.address=0.0.0.0"]
