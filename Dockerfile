
FROM python:latest

#set env variable for redis conection
ENV REDIS_URL=redis

WORKDIR /code

COPY requirements.txt /code

#dependencies for python
RUN pip install -r requirements.txt --no-cache-dir

COPY . /code

# dev server for now
CMD flask run --host=0.0.0.0
