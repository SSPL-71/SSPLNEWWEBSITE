FROM python:3.9-slim

WORKDIR /site

COPY . /site

RUN apt-get update && apt-get install -y ghostscript


RUN pip install --no-cache-dir -r requirements.txt


# ✅ This is the only CMD you need
CMD ["python3", "app.py"]

EXPOSE 10000