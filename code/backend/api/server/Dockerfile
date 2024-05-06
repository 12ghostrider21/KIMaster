FROM python:3.11.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

EXPOSE 12345

CMD ["python", "main.py", "12345", "8000", "0.0.0.0", "0.0.0.0"]



