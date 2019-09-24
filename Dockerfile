FROM python:3.7

RUN mkdir -p /app

COPY . /app

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install -r requirements.txt

CMD ./entrypoint.sh
