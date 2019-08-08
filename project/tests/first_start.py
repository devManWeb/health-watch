import unittest
from project.src.first_start import FirstConfiguration

toTest = FirstConfiguration()

class TestConfigMethods(unittest.TestCase):
    
    '''
    this methods should always start with "test"
    True is for success
    False is for failure
    '''
    def testIsValidHour(self):
        self.assertTrue(toTest.isValidHour("04:59"))
        self.assertTrue(toTest.isValidHour("3:59"))
        self.assertTrue(toTest.isValidHour("12:02"))

        self.assertFalse(toTest.isValidHour("12222:2"))
        self.assertFalse(toTest.isValidHour("2343"))
        self.assertFalse(toTest.isValidHour(2))
    
        
    def testIsYesNo(self):
        self.assertTrue(toTest.isYesNo("yes"))
        self.assertTrue(toTest.isYesNo("no"))

        self.assertFalse(toTest.isYesNo("3:59"))
        self.assertFalse(toTest.isYesNo(1))

    
    def testIsValidPause(self):
        for i in range(1,11):
            self.assertTrue(toTest.isValidPause(i))

        self.assertFalse(toTest.isValidPause(-11))
        self.assertFalse(toTest.isValidPause(40))

    #collectUserInput and askUser are not tested

if __name__ == '__main__':
    unittest.main()