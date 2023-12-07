FROM python:3.8-slim-buster

ENV PYTHONDONTWRITTEBYTEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# ENV HTTPS_PROXY="http://fodev.org:8118"

RUN mkdir -p /app

WORKDIR /app

COPY ./core .

RUN pip3 install pip --upgrade
RUN pip3 install -r requirements.txt

CMD yes yes | python3 manage.py makemigrations && \
        python3 manage.py migrate  && \
        yes yes | python3 manage.py collectstatic && \        
        python3 manage.py create_superuser && \
        python3 manage.py run_scraper && \
        python3 manage.py runserver 0.0.0.0:${SCRAPER_OUTER_PORT}
