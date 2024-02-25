import socket

DATABASE_FILE = 'dns_database.txt'

def handle_registration_request(data):
    # Parse data and store hostname and IP address
    registration_data = parse_registration_data(data)
    save_registration_data(registration_data)

def handle_dns_query(data):
    # Parse data and retrieve IP address for hostname
    query_data = parse_dns_query_data(data)
    ip_address = lookup_ip_address(query_data['NAME'])
    send_dns_response(ip_address, query_data)

def parse_registration_data(data):
    registration_data = {}
    lines = data.split('\n')
    for line in lines:
        key, value = line.split('=')
        registration_data[key.strip()] = value.strip()
    return registration_data

def save_registration_data(registration_data):
    with open(DATABASE_FILE, 'a') as file:
        file.write(json.dumps(registration_data) + '\n')

def parse_dns_query_data(data):
    query_data = {}
    lines = data.split('\n')
    for line in lines:
        key, value = line.split('=')
        query_data[key.strip()] = value.strip()
    return query_data

def lookup_ip_address(hostname):
    with open(DATABASE_FILE, 'r') as file:
        for line in file:
            registration_data = json.loads(line.strip())
            if registration_data['NAME'] == hostname:
                return registration_data['VALUE']
    return None

def send_dns_response(ip_address, query_data):
    if ip_address:
        dns_response = f"TYPE=A\nNAME={query_data['NAME']}\nVALUE={ip_address}\nTTL=10\n"
    else:
        dns_response = ''  # Empty response if hostname not found
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        client_address = (query_data['IP'], int(query_data['PORT']))
        udp_socket.sendto(dns_response.encode(), client_address)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 53533))

    while True:
        data, address = server_socket.recvfrom(1024)
        data = data.decode('utf-8').strip()

        if 'VALUE=' in data:  # Registration request
            handle_registration_request(data)
        else:  # DNS query
            handle_dns_query(data)

if __name__ == '__main__':
    main()
