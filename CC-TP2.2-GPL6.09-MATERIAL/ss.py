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

    def __init__(self, fileConfig, porta, timeout, debug_option):
        self.fileConfig = fileConfig
        self.porta = porta
        self.timeout = timeout
        self.debug_option = debug_option

        self.cache = Cache()

        parseconfig = PC(self.fileConfig)
        parseconfig.parseConfig()

        self.dominio = parseconfig.dominio
        self.servidor_primario = parseconfig.sp
        self.logs = parseconfig.lg
        self.st = parseconfig.st

        self.allLogs = Logs(self.logs, self.debug_option)
        self.allLogs.ST(str(11111), str(self.porta))
        self.allLogs.EV("Ficheiro config lido!!")

        self.allLogs.EV("Ficheiro de base de dados lido!!")

        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.bind(("0.0.0.0", self.porta))

    def getsoaretry(self):
        table = self.cache.array
        for data in table:
            if data[1] == "SOARETRY":
                self.soaretry = int(data[2])

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
            if extra is not None:
                if len(extra) > 4:
                    resposta += extra[0] + " " + extra[1] + " " + extra[2] + " " + extra[3] + " " +  extra[4]
                else:
                    resposta += extra[0] + " " + extra[1] + " " + extra[2] + " " + extra[3]

        self.udp.sendto(resposta.encode('utf-8'), add)

    def executar_zt(self):
        sp = self.servidor_primario
        portaSP = 53

        if ":" in self.servidor_primario:
            sp, portaSP = self.servidor_primario.split(":") # a porta que vais mandar para o servidor tem que ser a que tiver na BD
            portaSP = int(portaSP)
        while 1:

            start = time.time()

            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


            tcp.connect((sp,portaSP))

            dominio = f"Dominio: \"{self.dominio}\""

            tcp.send(dominio.encode('utf-8'))

            msg = tcp.recv(1024).decode('utf-8')
            partes = msg.split(':')

            data = msg.split(' ')
            rep = "ok: " + str(data[1])
            tcp.send(rep.encode('utf-8'))

            receivedBytes = 0
            while msg:
                msg = tcp.recv(1024)
                linha = msg.decode('utf-8')
                if (linha != ''):
                    receivedBytes += len(linha)
                    data = linha.split(';')
                    self.cache.adicionaLinhaCache(data[0], data[1], data[2], int(data[3]), int(data[4]), origin="SP", state="VALIDO")
            #  print("Transferencia de zona executada com exito!!")
            tcp.close()
            end = time.time()
            self.allLogs.ZT(sp, str(portaSP), "SS", str(receivedBytes), str((end-start)*1000))
            self.getsoaretry()
            time.sleep(self.soaretry)

    def run(self):
        zoneTransferThread = threading.Thread(target=self.executar_zt)
        zoneTransferThread.start()

        self.recebeNovasQuerys()

def main():
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
        print("<Usage> configFile *portNumber timeout *D\n* not mandatory.")
        return

    ss = SS(fileConfig, porta, timeout, debug_option)
    ss.run()

if __name__ == "__main__":
   main()
