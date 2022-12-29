import sys
from logs import Logs


class PC():
   
    # mudei bue cenas
    def __init__(self, filename):
        self.nomeficheiro = str(filename)
        self.dominio = ""
        self.db = ""
        self.sp = ""
        self.ss = []
        self.dd = ""
        self.lgs = {}
        self.lg = None
        self.st = ""
        self.sp = ""
        # self.logs = Logs(self.lg, sys.argv[2])
        # self.logs.ST(str(11111), str(sys.argv[2]))
        # self.logs.EV("Ficheiro config lido!!")
        

    def parseConfig(self):
        ficheiro = open(self.nomeficheiro, 'r')
        linhas = ficheiro.readlines()
        lido = []
            
        for linha in linhas:
            if linha[0] != "#":
                linha = linha[:-1]
                lido.append(linha)
                partes = linha.split(" ")
                if len(partes) != 3:
                    print(f'Linha "{linha}" nao tem o numero correto de argumentos.')
                    
                if len(self.dominio) == 0:  # preencher o campo dominio
                    self.dominio = partes[0]
                if partes[1] == "DB":
                    self.db = partes[2]
                elif partes[1] == "SS":
                    self.ss.append(partes[2])
                elif partes[1] == "SP": # n tinhas esta linha
                    self.sp = partes[2]
                elif partes[1] == "DD":
                    self.dd = partes[2]
                    self.dominio = partes[0]
                elif partes[1] == "LG":
                    if self.lg is None:
                        self.lg = partes[2]
                    else:
                        self.lgs[partes[0]] = partes[2]
                elif partes[1] == "ST":
                    if partes[0] != "root":
                        print("Entrada ST deve ter root como parametro")
                        
                    self.st = partes[2]
                else:
                    print(f'Tipo invalido {partes[1]}')
