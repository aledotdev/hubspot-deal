FROM python:3.7.3
ADD /app /app
WORKDIR /app
ADD ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt