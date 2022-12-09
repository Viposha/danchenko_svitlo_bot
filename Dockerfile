FROM python:3.11-slim-buster
WORKDIR /danchenko_svitlo_bot
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
