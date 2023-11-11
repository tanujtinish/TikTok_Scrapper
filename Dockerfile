FROM python:3.11-slim-bookworm

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*
RUN sudo apt-get install libgl1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install flask[async]

COPY . .

RUN python3 src/datasets/predownload_nltk_datasets.py

EXPOSE 8000

RUN ls
CMD ["python", "src/web_server.py"]