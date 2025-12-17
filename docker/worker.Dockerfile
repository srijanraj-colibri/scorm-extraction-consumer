FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY workers workers
COPY settings.py settings.py

CMD ["celery", "-A", "workers.celery_app", "worker", "--loglevel=info"]
