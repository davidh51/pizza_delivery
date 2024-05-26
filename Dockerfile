FROM python:3.11.2

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

#CMD ["python3", "./app/run.py"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
