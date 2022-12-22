import sys
import socket 
import threading
from cache import Cache
from logs import Logs
from parseConfig import PC
from parseDB import PDB
import re
import datetime
from zonetransfer import ZT

class SS:
    
    tokens = len(sys.argv)
    if tokens == 5:
        fileConfig = sys.argv[1]
        porta = int(sys.argv[2])
        timeout = int(sys.argv[3])
        debug_option = sys.argv[4]
    elif tokens == 4:
        fileConfig = sys.argv[1]
        porta = 11111
        timeout = int(sys.argv[2])
        debug_option = sys.argv[3]
    else:
        print("Introduza o numero correto de argumentos!")
        
    cache = Cache()
    
    parseconfig = PC(fileConfig)
    parseconfig.parseConfig()
    
    dominio = parseconfig.dominio     
    servidor_primario = parseconfig.sp 
    logs = parseconfig.lg
    
    def getsoaretry(self, cache):
        table = Cache.array
        for data in table:
            if data[1] == "SOARETRY":
                self.soaretry = int(data[2])
    
    def executar_zt(self):
        self.porta = 11111
        while 1:
            
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            tcp.connect(("127.0.0.1",self.porta))
            
            dominio = f"Dominio: \"{self.dominio}\""
            
            tcp.send(dominio.encode('utf-8'))
            
            msg = tcp.recv(1024).decode('utf-8')
            print(msg)
            partes = msg.split(' ')
            entradas = int(partes[1])
            cacheMem = int(self.cache.size)
            
            data = msg.split(' ')
            rep = "Enviado: " + str(data[1])
            tcp.send(rep.encode('utf-8'))
            
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
    ss = SS()
    ss.executar_zt()
if __name__ == "__main__":
   main()