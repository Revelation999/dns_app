FROM python:3.9-slim

WORKDIR /app

COPY fibonacci_server.py /app

RUN pip install flask

EXPOSE 9090

CMD ["python", "fibonacci_server.py"]
