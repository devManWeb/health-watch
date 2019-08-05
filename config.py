'''
This module takes care of reading config_file.ini,
as well as writing the parameters when needed
'''

import configparser

class ConfigIO():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config_file.ini")

    def readProp(self,toRead):    
        return self.config['DEFAULT'][toRead]

    def readTime(self,toRead):
        '''
        reads the data from the configuration file
        pepares an array with hours and minutes as integers
        '''
        fromCfg =  self.config["DEFAULT"][toRead]
        newArr = fromCfg.split(":")
        intValues = [int(x) for x in newArr]
        return intValues

    def writeProp(self,toWrite,newValue):
        self.config['DEFAULT'][toWrite] = newValue
        #actual writing on config.ini
        with open("config_file.ini", "w") as newParams:    
            self.config.write(newParams)