FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY consumer consumer
COPY workers workers
COPY settings.py settings.py

CMD ["python", "-m", "consumer.main"]
