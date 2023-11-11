FROM python:3.11-slim-bookworm

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /metajungle-opl

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r flask[async]

RUN python3 src/datasets/predownload_nltk_datasets.py

COPY . .

EXPOSE 8000

RUN ls
CMD ["python", "src/web_server.py"]