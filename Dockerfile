FROM python:3.11-slim-buster
WORKDIR /danchenko_svitlo_bot
COPY requirements.txt ./
RUN apt-get update && apt-get install -y iputils-ping
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
