FROM python:3.12.11-slim-bookworm

WORKDIR /opt/app

RUN apt update && apt install -y curl net-tools dnsutils

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY wsgi.py wsgi.py
COPY watch.sh watch.sh

CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:8000", "-w", "8"]
