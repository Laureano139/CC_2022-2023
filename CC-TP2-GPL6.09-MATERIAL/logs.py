
import logging 

class Logs:
    
    def __init__(self, ficheiroLogs = '', modo = ''):
        
        self.ficheiroLogs = ficheiroLogs
        f = open(self.ficheiroLogs, "a")
        f.write("# Log file for DNS server/resolver")
        f.close()
        
        self.modo = modo
        
    def QR(self, recebequery, address, informacao = ''):
        logging.basicConfig(filename=self.ficheiroLogs, encoding='utf-8', level=logging.INFO, format = "%(asctime)s.%(msecs)03d %(message)s", datefmt = "%d:%m:%Y.%H:%M:%S")
        
        logging.info("Query log started...")
        msg = "QR" + address + " " + informacao
        
        
        logging.info(msg)
        if self.modo == "debug":
            print(msg)
            
    
    def QE(self, recebequery, address, informacao = ''):
        logging.basicConfig(filename=self.ficheiroLogs, encoding='utf-8', level=logging.INFO, format = "%(asctime)s.%(msecs)03d %(message)s", datefmt = "%d:%m:%Y.%H:%M:%S")
        
        logging.info("Query log started...")
        msg = "QE" + address + " " + informacao
        
        
        logging.info(msg)
        if self.modo == "debug":
            print(msg)
            
        
            
    
    def RP(self, recebequery, address, informacao = ''):
        logging.basicConfig(filename=self.ficheiroLogs, encoding='utf-8', level=logging.INFO, format = "%(asctime)s.%(msecs)03d %(message)s", datefmt = "%d:%m:%Y.%H:%M:%S")

        msg = "RP" + address + " " + informacao
        
        
        logging.info(msg)
        if self.modo == "debug":
            print(msg)
            
    def RR(self, recebequery, address, informacao = ''):
        logging.basicConfig(filename=self.ficheiroLogs, encoding='utf-8', level=logging.INFO, format = "%(asctime)s.%(msecs)03d %(message)s", datefmt = "%d:%m:%Y.%H:%M:%S")
  
        msg = "RR" + address + " " + informacao
        
        logging.info(msg)
        if self.modo == "debug":
            print(msg)
            

    def ZT(self, ip, port, role = '', time = '', bytes = ''):
        logging.basicConfig(filename = self.ficheiroLogs, filemode="a", level=logging.INFO, format = "%(asctime)s.%(msecs)03d %(message)s", datefmt='%d:%m:%Y.%H:%M:%S')
        
        if time == '' and bytes == '':
            msg = "ZT " + ip + ":" + port + " " + role
        else:
            msg = "ZT " + ip + ":" + port + " " + role + " " + time + " " + bytes

        logging.info(msg)
        if self.modo == "debug":
            print(msg)
            
    
    def EV(self, eventType, mensagem =''):
        logging.basicConfig(filename = self.ficheiroLogs, filemode="a", level=logging.INFO, format = "%(asctime)s.%(msecs)03d %(message)s", datefmt='%d:%m:%Y.%H:%M:%S')

        if mensagem:
            msg = "EV 127.0.0.1 " + eventType + " " + mensagem 
        else:
            msg = "EV 127.0.0.1 " + eventType

        logging.info(msg)
        if self.modo == "debug":
            print(msg)
            
    
    
    def ER(self, address):
        logging.basicConfig(filename = self.ficheiroLogs, filemode="a", level=logging.INFO, format = "%(asctime)s.%(msecs)03d %(message)s", datefmt='%d:%m:%Y.%H:%M:%S')
        msg = "ER " + address   

        logging.info(msg)
        if self.modo == "debug":
            print(msg)
        
        
    def EZ(self, ip, port, role):
        logging.basicConfig(filename = self.ficheiroLogs, filemode="a", level=logging.INFO, format = "%(asctime)s.%(msecs)03d %(message)s", datefmt='%d:%m:%Y.%H:%M:%S')

        msg = "EZ " + ip + ":" + port + " " + role

        logging.info(msg)
        if self.modo == "debug":
            print(msg)
            
            
    def FL(self, error_type):
        logging.basicConfig(filename = self.ficheiroLogs, filemode="a", level=logging.INFO, format = "%(asctime)s.%(msecs)03d %(message)s", datefmt='%d:%m:%Y.%H:%M:%S')
        msg = "FL 127.0.0.1 " + error_type

        logging.info(msg)
        if self.modo == "debug":
            print(msg)
    
    
    def TO(self, timeout_type):
        logging.basicConfig(filename = self.ficheiroLogs, filemode="a", level=logging.INFO, format = "%(asctime)s.%(msecs)03d %(message)s", datefmt='%d:%m:%Y.%H:%M:%S')
        msg = "TO " + timeout_type

        logging.info(msg)
        if self.modo == "debug":
            print(msg)
            
            
    def SP(self, reason):
        logging.basicConfig(filename = self.ficheiroLogs, filemode="a", level=logging.INFO, format = "%(asctime)s.%(msecs)03d %(message)s", datefmt='%d:%m:%Y.%H:%M:%S')
        msg = "SP 127.0.0.1 " + reason

        logging.info(msg)
        if self.modo == "debug":
            print(msg)
            
            
    def ST(self, port,  mode):
        logging.basicConfig(filename = self.ficheiroLogs, filemode="a", level=logging.INFO, format = "%(asctime)s.%(msecs)03d %(message)s", datefmt='%d:%m:%Y.%H:%M:%S')
        msg = "ST 127.0.0.1 " + port + " " + mode
        
        logging.info(msg)
        if self.modo == "debug":
            print(msg)


    
    
    