FROM python:3.9-slim

WORKDIR /app

COPY authoritative_server.py /app

EXPOSE 53533/udp

CMD ["python", "authoritative_server.py"]
