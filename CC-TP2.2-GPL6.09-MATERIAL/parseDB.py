from cache import Cache
from time import perf_counter
import re

class PDB():


    def __init__(self,filename,cache):
        self.fName = filename
        self.name = "/-/"
        self.type = "/-/"
        self.value = "/-/"
        self.ttl = "/-/"
        self.priority = "/-/"
        self.origin = "FICHEIRO"
        self.timestamp = 0.0
        self.index = 0
        self.status = "VALIDO"
        self.cache = cache

    def parseDB(self):
        macros = {}
        names = {}
        start = perf_counter()

        with open(self.fName, "r") as file:
            lines = file.read().split("\n")

            for line in lines:
                if len(line) == 0 or line[0] == "#":
                    continue
                partes = line.split(" ")

                if partes[1] == "DEFAULT":
                    if len(partes) != 3:
                        print("Demasiados argumentos!")
                    macros[partes[0]] = partes[2]
                    # n precisas de nada disto
                    #  self.name = partes[0]
                    #  self.type = partes[1]
                    #  self.value = partes[2][:-1]
                    #  stopCounter = perf_counter()
                    #  self.timestamp = (stopCounter - start)
                    self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],origin="FILE")

                    continue
                
                for i in range(len(partes)):
                    if partes[i] in macros.keys():
                        partes[i] = macros[partes[i]]

                if partes[1] == "CNAME":
                    if len(partes) != 4:
                        print("A entrada do CNAME deve ter 4 argumentos")
                    if (partes[-1] != "."):
                        partes[0] = macros["@"]

                    if (partes[2] in names.keys()):
                        print("Um nome nao devera apontar para outro nome")

                    if (partes[0] in names.keys()):
                        print("O mesmo nome nao deve ser dado a 2 parametros diferentes")

                    self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],int(partes[3]),origin="FILE")
                    continue
                if (partes[-1] != "."):
                    partes[0] = macros["@"]

                if partes[1] == "SOASP":
                    if len(partes) != 4:
                        print("Demasiados argumentos")
                    self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],int(partes[3]),origin="FILE")

                elif partes[1] == "SOAADMIN":
                    if len(partes) != 4:
                        print("Demasiados argumentos")
                    self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],int(partes[3]),origin="FILE")

                elif partes[1] == "SOASERIAL":
                    if len(partes) != 4:
                        print("Erro")
                    self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],int(partes[3]),origin="FILE")

                elif partes[1] == "SOAREFRESH":
                    if len(partes) != 4:
                        print("Erro")
                    self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],int(partes[3]),origin="FILE")
                elif partes[1] == "SOAEXPIRE":
                    if len(partes) != 4:
                        print("Erro")
                    self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],int(partes[3]),origin="FILE")
                elif partes[1] == "SOARETRY":
                    if len(partes) != 4:
                        print("Erro")
                    self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],int(partes[3]),origin="FILE")

                elif partes[1] == "NS":
                    if len(partes) < 3:
                        print("Erro, sao necessarios 3, 4 ou 5 argumentos!")
                    self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],origin="FILE")

                    if len(partes) == 3:
                        self.cache.adicionaLinhaCache(partes[0], partes[1], partes[2], origin="FILE")
                    if len(partes) == 4:
                        self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],int(partes[3]),origin="FILE")
                    if len(partes) == 5:
                        self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],int(partes[3]),int(partes[4]),origin="FILE")

                elif partes[1] == "MX":
                    if len(partes) < 4:
                        print("Erro")
                    if len(partes) == 4:
                        self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],int(partes[3]),origin="FILE")
                    else:
                        self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],int(partes[3]),int(partes[4]),origin="FILE")

                elif partes[1] == "A":
                    if len(partes) < 4:
                        print("Erro")
                    if len(partes) == 4:
                        x = re.split(" " ,line)
                        partes[0] = x[0]
                        self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],int(partes[3]),origin="FILE")
                    else:
                        x = re.split(" " ,line)
                        partes[0] = x[0]
                        self.cache.adicionaLinhaCache(partes[0],partes[1],partes[2],int(partes[3]),int(partes[4]),origin="FILE")

                else: print(partes[1] + " e invalido")


def main():
    cache = Cache()
    parse = PDB("db.txt",cache)
    parse.parseDB()


if __name__ == "__main__":
    main()




