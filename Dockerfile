FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
# Copy src directory into the container
COPY src /app/src
EXPOSE 8000 8501
CMD ["sh", "-c", "uvicorn src.api.main:app --host 0.0.0.0 --port 8000 & streamlit run src/ui/dashboard.py --server.port=8501 --server.address=0.0.0.0"]
