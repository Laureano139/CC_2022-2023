import socket
import sys
from cache import Cache

class SR:

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 53))

    dns_table = {
        # "www.example.com": "192.0.2.1",
        # "www.example.org": "198.51.100.1",
        # "www.example.net": "203.0.113.1",
    }

    while True:

        data, addr = sock.recvfrom(1024)
        
        domain_name = data[12:]
        
        ip_address = dns_table.get(domain_name)

        response = f"Dominio: " + domain_name + f"IP address: " + ip_address.encode("utf-8")
        
        sock.sendto(response, addr)