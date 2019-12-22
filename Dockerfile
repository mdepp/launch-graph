FROM python:3.8.1

RUN apt-get update
RUN apt-get install -y graphviz
RUN pip install graphviz regex

COPY . /app

CMD ["python", "/app/main.py"]