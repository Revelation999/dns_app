FROM python:3.9-slim

WORKDIR /app

COPY user_server.py /app

RUN pip install flask requests

EXPOSE 8080

CMD ["python", "user_server.py"]
