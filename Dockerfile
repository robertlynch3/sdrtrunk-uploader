FROM python:3.11

ADD ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

ADD server.py /
ADD gunicorn.py /

CMD ["gunicorn", "server:app", "--config", "/gunicorn.py"]