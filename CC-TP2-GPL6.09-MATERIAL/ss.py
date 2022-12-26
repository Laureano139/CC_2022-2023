import sys
import socket 
import threading
from cache import Cache
from logs import Logs
from parseConfig import PC
from parseDB import PDB
import re
import time
from zonetransfer import ZT

class SS:
  
    # pus no construtor
    def __init__(self):
        tokens = len(sys.argv)
        if tokens == 5:
            self.fileConfig = sys.argv[1]
            self.porta = int(sys.argv[2])
            self.timeout = int(sys.argv[3])
            self.debug_option = sys.argv[4]
        elif tokens == 4:
            self.fileConfig = sys.argv[1]
            self.porta = 53
            self.timeout = int(sys.argv[2])
            self.debug_option = sys.argv[3]
        else:
            print("Introduza o numero correto de argumentos!")
            
        self.cache = Cache()
        
        parseconfig = PC(self.fileConfig)
        parseconfig.parseConfig()
        
        self.dominio = parseconfig.dominio     
        self.servidor_primario = parseconfig.sp 
        self.logs = parseconfig.lg
        
    def getsoaretry(self):
        table = self.cache.array
        for data in table:
            if data[1] == "SOARETRY":
                self.soaretry = int(data[2])
    
    def executar_zt(self):
        # self.porta = 11111
        while 1:
            
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            sp = self.servidor_primario
            portaSP = 53

            if ":" in self.servidor_primario:
                sp, portaSP = self.servidor_primario.split(":") # adicionei isto, a porta que vais mandar para o servidor tem que ser a que tiver na BD
                portaSP = int(portaSP)

            print(self.servidor_primario, sp, portaSP)
            tcp.connect((sp,portaSP))
            
            dominio = f"Dominio: \"{self.dominio}\""
            
            tcp.send(dominio.encode('utf-8'))
            
            msg = tcp.recv(1024).decode('utf-8')
            print(msg)
            partes = msg.split(':') # mudei para : pq es tone
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
                        data = linha.split(';') # mudei para ;
                        #  print(f"{data}\n")
                        self.cache.adicionaLinhaCache(data[0], data[1], data[2], int(data[3]), int(data[4]), origin="SP", state="VALIDO")
            print("Transferencia de zona executada com exito!!")
            #  self.soaretry(self.cache) # n entendi aqui
            tcp.close()
            #Log ZT
            self.getsoaretry()
            time.sleep(self.soaretry)


def main():
    ss = SS()
    ss.executar_zt()
if __name__ == "__main__":
   main()
