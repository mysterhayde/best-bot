FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY Sources .
RUN useradd -m botuser
USER botuser
CMD ["python", "main.py"]