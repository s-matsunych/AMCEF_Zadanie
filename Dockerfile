FROM python:3.8

WORKDIR /app
COPY *.py /app
COPY requirements.txt /app

RUN ls
EXPOSE 5000

RUN pip install -r requirements.txt
CMD ["python3", "server.py"]
