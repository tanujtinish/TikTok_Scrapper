
FROM python:3.9.6

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

    
WORKDIR /app

COPY . /app

COPY requirements.txt .
RUN pip install --upgrade pip

# Install project dependencies
RUN pip install -r requirements.txt

# Install NLTK datasets
RUN python3 src/datasets/predownload_nltk_datasets.py

EXPOSE 8000

RUN ls
CMD ["python", "src/web_server.py"]
