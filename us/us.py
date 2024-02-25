from flask import Flask, request
import requests
import socket

app = Flask(__name__)

def send_dns_query(hostname):
    dns_query = f"TYPE=A\nNAME={hostname}\n"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        as_address = (AS_IP, AS_PORT)
        udp_socket.sendto(dns_query.encode(), as_address)

        # Wait for DNS response from Authoritative Server (AS)
        response, _ = udp_socket.recvfrom(1024)
        return response.decode('utf-8').strip()

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return 'Bad Request', 400

    response = send_dns_query(hostname)
    if response == '':
        return 'Failed to get IP address from AS', 500
    fs_ip = None
    for line in response.split('\n'):
        if line.startwith('VALUE='):
            fs_ip = line.split('=')[1]
            break

    fs_url = f'http://{fs_ip}:{fs_port}/fibonacci?number={number}'
    response = requests.get(fs_url)
    if response.status_code != 200:
        return 'Failed to get Fibonacci number from FS', 500
    fibonacci_number = response.text.strip()

    return fibonacci_number, 200

if __name__ == '__main__':
    app.run(port=8080)
