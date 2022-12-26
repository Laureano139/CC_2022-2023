import sys
import datetime

class Cache:

    def __init__(self):
        self.size  = 0
        self.index = 0
        self.array = []

    def adicionaLinhaCache(self, name, type, value, ttl=0, prio=0, origin="FILE", time=datetime.datetime.now(), state="VALIDO"):

        print(name, type, ttl, prio, origin, time, self.index, state)
        new = (name, type, value, str(ttl), str(prio), origin, time, str(self.index), state)
        self.array.append(new)
        self.index += 1
        self.size += 1


    #  def cacheFill(self, DB):
        #  for l in DB : ## aqui tens que mudar em baixo pq a adicionaLinhaCache recebe os argumentos e nao uma linha
            #  self.adicionaLinhaCache(l)

    def verifica(self, dom, typeValue):

        for i in range(self.index):
            if dom == self.array[i][0] and typeValue == self.array[i][1]:
                return i

        return -1

    def checkNumberOfValues (self, dom, typeValue):
        c=0
        for i in range(self.index):
            if dom == self.array[i][0] and typeValue == self.array[i][1]:
                c += 1

        return c

    def devolveAuthoritiesValues (self, dom):
        arrayAV = []
        for i in range(self.index):
            if dom == self.array[i][0] and self.array[i][1] == "NS":
                arrayAV.append(self.array[i])
        return arrayAV

    def devolveValues (self, dom, typeValue):
        arrayV = []
        for i in range(self.index):
            if dom == self.array[i][0] and self.array[i][1] == typeValue:
                arrayV.append(self.array[i])
        return arrayV

    def extraValue(self, dom, comp):

        for i in range(self.index):
            if comp == self.array[i][0] and self.array[i][1] == "A":
               return self.array[i]

        return None



