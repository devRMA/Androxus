FROM python:3.10.1

WORKDIR /usr/src/bot

ENV PYTHONUNBUFFERED 1

COPY . .

RUN apt-get update; \
    pip install -r ./requirements.txt; \
    useradd -ms /bin/bash bot;

USER bot

ENTRYPOINT ["python", "main.py"]
