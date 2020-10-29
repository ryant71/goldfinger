FROM python:3.8

ENV DASH_DEBUG_MODE True

RUN mkdir -p /app

WORKDIR /app
COPY . .

RUN ls -l && pwd && echo $PATH
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

RUN poetry install

EXPOSE 8050
CMD ["python", "app.py"]
