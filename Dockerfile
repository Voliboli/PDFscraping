FROM python:3.10-slim

RUN apt update && apt install -y default-jre && rm -rf /var/lib/apt/lists/*

ENV PROJECT_DIR /usr/src/voliboli

WORKDIR ${PROJECT_DIR}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
