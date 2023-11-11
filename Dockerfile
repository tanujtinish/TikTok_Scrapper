
FROM --platform=linux/amd64 ubuntu:focal

ENV TZ=Asia/Kolkata
ENV DEBIAN_FRONTEND=noninteractive

# Update and install packages without prompts
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
       jq \
       build-essential \
       python3.9 \
       python3-pip \
       docker-compose \
       jsonnet \
       bison \
       mercurial \
    && rm -rf /var/lib/apt/lists/*
    
RUN pip install --upgrade pip

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
    
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip

# Install project dependencies
RUN pip install -r requirements.txt

COPY . .

# Install NLTK datasets
RUN python3 src/datasets/predownload_nltk_datasets.py

RUN apt update -y && apt install libgl1-mesa-glx sudo chromium chromium-driver -y
# Download and install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

EXPOSE 8000

RUN ls
CMD ["python", "src/web_server.py"]
