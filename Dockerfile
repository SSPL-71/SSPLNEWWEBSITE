FROM python:3.9-slim

WORKDIR /site

COPY . /site                            # ✅ Copy everything at once

RUN apt-get update && apt-get install -y ghostscript

RUN pip install --no-cache-dir -r requirements.txt  # ✅ Install dependencies after everything is copied

CMD ["python3", "app.py"]

EXPOSE 10000