FROM python:3.12.10-slim

WORKDIR /

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

EXPOSE 3000

CMD ["python", "-m", "src.main"]
