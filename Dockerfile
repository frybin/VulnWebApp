FROM python:3.6-alpine

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY webapp webapp
COPY config config
COPY app.py db_setup.py start.sh ./
RUN chmod +x start.sh
RUN python db_setup.py

ENV FLASK_APP app.py
ENV FLASK_ENV development

EXPOSE 5000
ENTRYPOINT ["./start.sh"]