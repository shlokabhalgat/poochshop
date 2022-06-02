# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /poochshop
COPY requirements.txt /poochshop/
RUN pip install -r requirements.txt
COPY . /poochshop/