FROM python:3.7-stretch

RUN mkdir /app
WORKDIR /app
RUN export PYTHONPATH=`pwd`

RUN apt-get update && \
    apt-get install -y build-essential cmake && \
    apt-get install -y libopenblas-dev liblapack-dev && \
    apt-get install -y libx11-dev libgtk-3-dev && \
    pip install dlib && \
    pip install face_recognition && \
    rm -rf ~/.cache/pip && \
    apt-get clean

COPY ./requirements.txt /app
RUN pip install -r /app/requirements.txt && \
    rm -rf ~/.cache/pip

COPY ./resources/page_properties /app/resource/page_properties
COPY ./setup.py /app
COPY ./uwsgi.ini /app
COPY ./scripts /app/scripts
COPY ./sharesio /app/sharesio

RUN ./scripts/install.sh

ENTRYPOINT ["/app/scripts/flask.sh"]