FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r /app/requirements.txt
EXPOSE 7878
CMD ["python3", "-m", "kai11.services.server", "--index", "/app/outputs/vector_store.jsonl", "--host", "0.0.0.0", "--port", "7878"]
