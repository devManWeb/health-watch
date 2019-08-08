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
        '''
        read a generic prop from the config file
        the read index must be a string
        '''
        if type(toRead) is str:
            return self.config['DEFAULT'][toRead]
        else:
            raise TypeError

    def readTime(self,toRead):
        '''
        reads the data from the configuration file
        we prepare a list of integers (hours and minutes)
        the read index must be a string
        '''
        if type(toRead) is str:
            fromCfg =  self.config["DEFAULT"][toRead]
            newArr = fromCfg.split(":")
            intValues = [int(x) for x in newArr]
            return intValues
        else:
            raise TypeError

    def writeProp(self,toWrite,newValue):
        '''
        reads the data from the ini file
        the write index and the value must be strings
        '''
        if type(toWrite) is str and type(newValue):
            self.config['DEFAULT'][toWrite] = newValue
            #actual writing on config.ini
            with open("config_file.ini", "w") as newParams:    
                self.config.write(newParams)
            return True
        else:
            raise TypeError