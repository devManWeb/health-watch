import unittest
from project.src.config import ConfigIO

toTest = ConfigIO()

class TestConfigMethods(unittest.TestCase):

    #this methods should always start with "test"

    def testReadProp(self):
        indexList = ["isconfigured","isparttime","workstart","lunchstart","lunchend","workend","pauselength"]
        for prop in indexList:
            #loop in all the prop of indexList
            self.assertTrue(type(toTest.readProp(prop)) is str) 
        with self.assertRaises(TypeError):
            toTest.readProp(123)

    def testReadTime(self):  
        timeTables = ["workstart","lunchstart","lunchend","workend"]
        for prop in timeTables:
            self.assertTrue(type(toTest.readTime(prop)) is list) 
            self.assertTrue(type(toTest.readTime(prop)[0]) is int) 
            self.assertTrue(type(toTest.readTime(prop)[1]) is int) 

        with self.assertRaises(TypeError):
            toTest.readTime(123)

    def testWriteProp(self):  
        print("\n\nDefault values setted!")
        indexList = ["isconfigured","isparttime","workstart","lunchstart","lunchend","workend","pauselength"]
        defaultValues = ["yes","no","8:30","12:30","14:00","18:00","5"]
        
        counter = 0

        for prop in indexList:
            #if the writing is ok, returns true
            self.assertTrue(toTest.writeProp(prop,defaultValues[counter]))
            counter = counter + 1

        with self.assertRaises(TypeError):
            toTest.writeProp(123,123)


if __name__ == '__main__':
    unittest.main()