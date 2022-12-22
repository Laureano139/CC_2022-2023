import socket
import sys
import re
import random


x = re.split(":", sys.argv[1]) 
ipserver = x[0]
portserver = x[1]
dom = sys.argv[2]
typeValue = sys.argv[3] 
if len(sys.argv) > 4:
    recursive = True   
    
print("Ip: " + ipserver + " porta: " + portserver)
    
query = str(random.randint(1, 65535)) + ",Q" 
if recursive:
    query += "R" 
query += ",0,0,0,0;" + dom + "," + typeValue + ";"

udpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpClientSocket.sendto(query.encode('utf-8'), (ipserver, int(portserver)))


resposta = udpClientSocket.recv(1024).decode("utf-8")


print(resposta)