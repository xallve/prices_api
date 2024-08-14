FROM python:3.10-slim

WORKDIR /crypto_api

COPY requirements.txt /crypto_api
RUN pip install -r requirements.txt

COPY . /crypto_api

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]