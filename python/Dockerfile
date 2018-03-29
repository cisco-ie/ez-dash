FROM python:jessie

ENV SHELL="/bin/bash"

EXPOSE 9091

WORKDIR /app
COPY . /app

RUN pip install pipenv
RUN pipenv install

CMD ["pipenv", "run", "python", "main.py"]