import socket
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register(): 
    data = request.json
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if not all([hostname, ip, as_ip, as_port]):
        return 'Bad Request', 400

    dns_message = {
        'TYPE': 'A',
        'NAME': hostname,
        'VALUE': ip,
        'TTL': 10 
    }

    dns_message_str = '\n'.join([f'{key}={value}' for key, value in dns_message.items()]) + '\n'

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        as_address = (as_ip, as_port)
        udp_socket.sendto(dns_message_str.encode(), as_address)

    return 'Registered successfully', 201

@app.route('/fibonacci', methods=['GET'])
def calculate_fibonacci():
    number = request.args.get('number')

    try:
        number = int(number)
    except ValueError:
        return 'Bad Format', 400

    fibonacci_number = calculate_fibonacci_number(number)

    return str(fibonacci_number), 200

def calculate_fibonacci_number(n):
    if n <= 1:
        return n
    else:
        return calculate_fibonacci_number(n-1) + calculate_fibonacci_number(n-2)

if __name__ == '__main__':
    app.run(port=9090)
