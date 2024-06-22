FROM python:3.11-slim
COPY . .
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh
CMD ["uvicorn", "main:app", "--host", "192.168.0.236", "--port", "80"]