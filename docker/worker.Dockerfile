FROM python:3.11-slim
WORKDIR /app

ENV PYTHONPATH=/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY workers workers
copy services services
COPY core core

CMD ["celery", "-A", "workers.celery_app", "worker", "--loglevel=info"]
