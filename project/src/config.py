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

        arguments
            toRead: property string name
        return
            value of the property
        raise
            TypeError if toRead is not a string
        '''
        if type(toRead) is str:
            return self.config['DEFAULT'][toRead]
        else:
            raise TypeError

    def readTime(self,toRead):
        '''
        read a generic prop from the config file

        arguments
            toRead: property string name
        return
            list of integers (hours and minutes)
        raise
            TypeError if toRead is not a string
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
        write the data on the ini file

        arguments
            toWrite: property string name
            newValue: new value to write
        return
            True if the operation was successful
        raise
            TypeError if toWrite or newValue are not strings
        '''
        if type(toWrite) is str and type(newValue) is str:
            self.config['DEFAULT'][toWrite] = newValue
            #actual writing on config.ini
            with open("config_file.ini", "w") as newParams:    
                self.config.write(newParams)
            return True
        else:
            raise TypeError