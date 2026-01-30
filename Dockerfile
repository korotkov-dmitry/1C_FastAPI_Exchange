FROM python:3.9-slim as Exchange1C

WORKDIR /app

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:8000"]
#для маленького сервера
#CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "main:app", "-b", "0.0.0.0:8000"]

