FROM python:3.6-slim

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python"]

CMD ["main.py"]