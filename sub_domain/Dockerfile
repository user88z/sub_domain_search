FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src/
ADD . /src/
RUN pip3 install -r requirements.txt
CMD python3 manage.py runserver 0.0.0.0:8080
EXPOSE 8080