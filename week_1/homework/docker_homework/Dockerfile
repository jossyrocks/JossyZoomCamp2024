FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2 python-dotenv

WORKDIR /app
COPY pipeline.py pipeline.py
COPY .env .env

ENTRYPOINT [ "python", "new_pipeline.py" ]