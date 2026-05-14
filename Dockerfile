FROM python:3.12.13

ARG USER="user-app"
ARG USER_ID=999
ARG GROUP="group-app"
ARG GROUP_ID=999

WORKDIR /opt/app/

# Set environment varibles
# python
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=30

RUN apt-get update  \
    && apt-get install --no-install-recommends -y \
      supervisor \
      nginx \
    # Cleaning cache:
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    # Installing `python` packages:
    && pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY gunicorn/config.py /etc/gunicorn/config.py
COPY gunicorn/launcher.sh /etc/gunicorn/launcher.sh

COPY nginx.conf /etc/nginx/nginx.conf

COPY server.cfg /etc/supervisor/conf.d/server.cfg
COPY server.sh /etc/server.sh

COPY wsgi.py wsgi.py

RUN addgroup --system --gid ${GROUP_ID} ${GROUP}
RUN adduser --system --uid ${USER_ID} --gid ${GROUP_ID} --no-create-home ${USER}

USER ${USER_ID}:${GROUP_ID}

CMD ["sh", "/etc/server.sh"]