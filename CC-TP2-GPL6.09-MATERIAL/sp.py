import sys
import socket 
import threading
from cache import Cache
from logs import Logs
from parseConfig import PC
from parseDB import PDB
import re
from datetime import datetime
from zonetransfer import ZT



class SP:



    def __init__(self):
        self.dominio = ""
        self.basededados = ""
        self.secundarios = []
        self.dd = ""
        self.logs = {}
        self.st = ""
        self.allLogs = Logs(self.logs, sys.argv[2])
        self.allLogs.ST(str(11111), str(sys.argv[2]))
        self.allLogs.EV("Ficheiro config lido!!")
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.bind(("127.0.0.1", 11111))

    tokens = len(sys.argv)
    if tokens == 4:
        fileConfig = sys.argv[1]
        porta = int(sys.argv[2])
        debug_option = sys.argv[4]
    elif tokens == 3:
        fileConfig = sys.argv[1]
        porta = 53
        debug_option = sys.argv[2]
    else:
        print("Introduza o numero correto de argumentos!")
        
    bfsize = 1024
    
    parseconfig = PC(fileConfig)
    parseconfig.parseConfig()
    
    dominio = parseconfig.dominio
    basededados = parseconfig.db
    secundarios = parseconfig.ss
    dd = parseconfig.dd
    logs = parseconfig.lg
    st = parseconfig.st
    
    # allLogs = Logs(logs, sys.argv[2])
    # allLogs.ST(str(11111), str(sys.argv[2]))
    # allLogs.EV("Ficheiro config lido!!")
    
    # udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # udp.bind(("127.0.0.1", 11111))
    
    
 # ---------------------------------------------------------------------------------------------------------------------------------------------#    
    
    cache = Cache()
    parse = PDB(basededados,cache)
    parse.parseDB()
    
    # allLogs.EV("Ficheiro de base de dados lido!!")
 # ---------------------------------------------------------------------------------------------------------------------------------------------#
        
    def geraResposta(self, msgStr, add):
        flags = ''
        response_code = "0"
        
        
        x = re.split(";", msgStr)
        primeira = x[0]
        segunda = x[1]
        lista1 = re.split(",", primeira)
        lista2 = re.split(",", segunda)
        message_id = lista1[0]
        if "R" in lista1[1]:
            flags += "R+"
        flags += "A"
        if self.cache.verifica(lista2[0], lista2[1]) == -1:
            response_code = "1"
        numberOfValues = str(self.cache.checkNumberOfValues(lista2[0], lista2[1]))
        values = self.cache.devolveValues(lista2[0], lista2[1])
        authorities = self.cache.devolveAuthoritiesValues(lista2[0])
        numberOfAuthoritiesValues = str(len(authorities))
        
        extraValues = []
        for entrada in values:
            comp = entrada[2]
            extraValues.append(self.cache.extraValue(lista2[0], comp))
            
        for entrada in authorities:
            comp = entrada[2]
            extraValues.append(self.cache.extraValue(lista2[0], comp))
        
        nrExtraValues = str(len(extraValues))
        resposta = message_id + "," + flags + "," + response_code + "," + numberOfValues + "," + numberOfAuthoritiesValues + "," + nrExtraValues + ";"
        resposta += segunda + ";"
        for value in values:
            if len(value) > 4:
                resposta += value[0] + " " + value[1] + " " + value[2] + " " + value[3] + " " +  value[4] 
            else:
                resposta += value[0] + " " + value[1] + " " + value[2] + " " + value[3]
        for authoritie in authorities:
            if len(authoritie) > 4:
                resposta += authoritie[0] + " " + authoritie[1] + " " + authoritie[2] + " " + authoritie[3] + " " +  authoritie[4]
            else:
                resposta += authoritie[0] + " " + authoritie[1] + " " + authoritie[2] + " " + authoritie[3]
        for extra in extraValues:
            if extra != None:  
                if len(extra) > 4:
                    resposta += extra[0] + " " + extra[1] + " " + extra[2] + " " + extra[3] + " " +  extra[4]
                else:
                    resposta += extra[0] + " " + extra[1] + " " + extra[2] + " " + extra[3]
        
        self.udp.sendto(resposta.encode('utf-8'), add)
        
    def recebeNovasQuerys(self):
        while True:
            msg, add = self.udp.recvfrom(1024)
            self.allLogs.QR(True , str(add), msg.decode("utf-8"))
            self.allLogs.QE(True , str(add), msg.decode("utf-8"))
            print(f"Recebi uma mensagem do cliente {add}")
            msgStr = msg.decode("utf-8")
            threading.Thread(target=self.geraResposta,args=(msgStr, add)).start()
            self.allLogs.RP(True, str(add), msg.decode("utf-8"))
            self.allLogs.RR(True, str(add), msg.decode("utf-8"))


        
    def putlineCache(self, array):
        str = ""
        for l in array:
            str += str(l) + ' '
        return str
    
    def zt(self):
        
        porta = 11111
        entries = "Numero de entradas:\n " + str(self.cache.size)

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp.bind(('',porta))
        while 1:
            
            tcp.listen()
        
            tcpSocket, add = tcp.accept()
            print("Conexao obtida (Servidor Secundario): ", str(add))
            requestmsg = tcpSocket.recv(1024).decode('utf-8')
            print(requestmsg)
            tcpSocket.send(entries.encode('utf-8'))
            msg = tcpSocket.recv(1024).decode('utf-8')
            print(msg)
            address = re.split(':', add)
            
            
            for line in self.cache.array:
                l = self.putlineCache(line)
                tcpSocket.send(l.encode('utf-8'))
                datetime.time.sleep(0.05)

            tcpSocket.close()
            date = datetime.now()
            atmtime = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]
            self.allLogs.ZT(f"IP: " + address[0], f"Porta: " + address[1], "ZT", "SS", atmtime)


        
def main():
    
    sp = SP()
    sp.zt()
    sp.recebeNovasQuerys()
    
    
    
if __name__ == "__main__":
    main()