FROM python:3.8-bullseye

RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list
RUN apt-get update &&\
    apt-get install -y gcc &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/home/

ENV VIRTUAL_ENV=${APP_HOME}venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR $APP_HOME

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip &&\
    pip install -r requirements.txt &&\
    rm -rf /root/.cache/pip &&\
    rm requirements.txt

COPY pub_chem_api ${APP_HOME}

# optionally : CMD["python", "main.py"]