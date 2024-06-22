FROM python:3.11-slim
COPY . .
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "80"]