FROM python:3.12.11-slim-bookworm

WORKDIR /opt/app

RUN apt update && apt install -y curl

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY wsgi.py wsgi.py

CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:8888", "-w", "1"]
