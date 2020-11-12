FROM python:3.8

ENV DASH_DEBUG_MODE True

ADD https://github.com/Droplr/aws-env/raw/b215a696d96a5d651cf21a59c27132282d463473/bin/aws-env-linux-amd64 /usr/local/bin/aws-env
RUN chmod a+x /usr/local/bin/aws-env

RUN mkdir -p /app

WORKDIR /app
COPY . .

RUN ls -l && pwd && echo $PATH
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

RUN poetry install

EXPOSE 5000
CMD ["/app/entrypoint.sh"]
