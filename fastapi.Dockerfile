FROM python:3.9-slim
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]