FROM python:3.9-slim

WORKDIR /site

COPY requirements.txt .                 # ✅ Copy requirements first
RUN pip install --no-cache-dir -r requirements.txt  # ✅ Install all dependencies

COPY . /site                            # ✅ Then copy the rest of your app

RUN apt-get update && apt-get install -y ghostscript

CMD ["python3", "app.py"]

EXPOSE 10000