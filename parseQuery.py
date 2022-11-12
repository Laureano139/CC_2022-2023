
import re

class Query:
    
    def __init__ (self, msg):
        self.m_msg = str(msg)
        line = re.split(";|,|", msg)
        self.messageID = line[0]  
        self.flags = line[1]
        self.responseCode = line[2]
        self.N_Values = line[3]
        self.N_Authorities = line[4]
        self.N_ExtraValues = line[5]
        self.name = line[6]
        self.type = line[7]
        

       