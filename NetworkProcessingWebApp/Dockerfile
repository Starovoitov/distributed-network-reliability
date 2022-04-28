FROM python:3.7-slim-buster

WORKDIR /networking_data_generation

COPY . .

RUN apt-get update
RUN apt-get install gcc -y
RUN apt-get install libcairo2-dev pkg-config python3.7-dev libffi6 libffi-dev libpq-dev -y

RUN pip3 --default-timeout=10000 install -r requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=${PYTHONPATH}:/networking_data_generation

EXPOSE 8080

CMD ["python3", "NetworkProcessingWebApp/network_processing.py"]