import sys
import socket 
import threading
from cache import Cache
from logs import Logs
from parseConfig import PC
from parseDB import PDB
import re
import datetime

class ZT:
    def __init__(self, nome, addr, cache, dominio):
        
        addr = addr.split(':')
        self.name = nome 
        self.ip = addr[0] 
        self.porta = addr[1]
        self.cache = Cache() 
        self.dominio = dominio 
        self.soaretry = 0
        # self.logs = ficheiro
        
    def soaretry(self, cache):
        table = Cache.array
        for data in table:
            if data[1] == "SOARETRY":
                self.soaretry = int(data[2])
                
    def executar_zt(self):
        counter = 0
        self.porta = 11111
        while 1:
            
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            tcp.connect((self.ip,self.porta))
            
            dominio = f"Dominio: \"{self.dominio}\""
            
            tcp.send(dominio.encode('utf-8'))
            
            msg = tcp.recv(1024).decode('utf-8')
            print(msg)
            partes = msg.split(' ')
            entradas = int(partes[1])
            cacheMem = int(self.cache.size)
            
            data = msg.split(' ')
            m = "Enviado: " + str(data[1])
            tcp.send(m.encode('utf-8'))
            
            while msg:
                msg = tcp.recv(1024)
                if cacheMem != entradas:
                    linha = msg.decode('utf-8')
                    if (linha != ''):
                        data = linha[:-1].split(' ')
                        Cache.adicionaLinhaCache(data[0], data[1], data[2], data[3], data[4], "SP", data[6], "VALIDO")
            print("Transferencia de zona executada com exito!!")
            self.soaretry(self.cache)
            tcp.close()
            #Log ZT
            
            datetime.time.sleep(self.soaretry)
            
def main():
    zt = ZT()
    
if __name__ == "__main__":
   main()
            
            
            
            
            