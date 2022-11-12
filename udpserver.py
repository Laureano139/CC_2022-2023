
import socket 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #AF_INET -> Internet     |     #SOCK_DGRAM -> UDP
sock.bind(('127.0.0.1',2001)) #Associa um IP e uma porta a uma instância socket

while True:
    data, addr = sock.recvfrom(1024) #1024 bytes | recebe uma data de um endereço 
    print(str(data)) #print da data
    message=bytes(" Hello I am the UDP Server ", encoding='utf-8') 
    sock.sendto(message,addr) #envia a mensagem acima para o endereço (cliente)
    

