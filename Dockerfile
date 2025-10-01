FROM python:3.9-slim

WORKDIR /site

COPY . /site

RUN apt-get update && apt-get install -y ghostscript

COPY app.py .
RUN pip install flask

CMD ["python3", "app.py"]

EXPOSE 10000