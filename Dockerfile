FROM python:3.8.5-slim-buster
RUN apt-get update -y && apt install awscli -y && apt-get install -y gcc

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

CMD ["python3", "Sensor_Fault_Detection/main.py"]