FROM python:3.12

COPY ./src/. /code
COPY ./requirements.txt /code/requirements.txt

WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENV PYTHONPATH=/code
ENV HOST=0.0.0.0

RUN ls

CMD ["fastapi", "run", "main.py", "--port", "8000"]