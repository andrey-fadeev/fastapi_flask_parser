FROM python:3.9-slim
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT celery -A tasks worker --loglevel=ERROR