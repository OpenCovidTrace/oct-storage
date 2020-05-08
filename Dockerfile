FROM python:3.7.7-buster

RUN mkdir /code
ADD requirements.txt /code
ADD requirements_test.txt /code

WORKDIR /code
RUN pip install -r requirements.txt
RUN pip install -r requirements_test.txt

ADD ./alembic ./alembic
ADD ./instance ./instance
ADD ./oct_storage ./oct_storage
ADD ./alembic.ini ./alembic.ini
ADD ./fabfile.py ./fabfile.py
ADD ./Makefile ./Makefile
ADD ./run.py ./run.py
ADD ./setup.cfg ./setup.cfg

ENV PYTHONUNBUFFERED 1

CMD ["python", "run.py"]
