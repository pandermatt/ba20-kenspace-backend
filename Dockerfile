FROM python:3.7

LABEL maintainer="p.andermatt@me.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm
RUN python -m spacy download de_core_news_sm

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "waitress_server.py" ]

ENV PORT 5000
EXPOSE 5000
