import unittest
from project.src.first_start import OnlyForThisFile

private = OnlyForThisFile()

class TestConfigMethods(unittest.TestCase):
    
    '''
    this methods should always start with "test"
    True is for success
    False is for failure
    '''
    def testIsValidHour(self):
        self.assertTrue(private.isValidHour("04:59"))
        self.assertTrue(private.isValidHour("3:59"))
        self.assertTrue(private.isValidHour("12:02"))

        self.assertFalse(private.isValidHour("12222:2"))
        self.assertFalse(private.isValidHour("2343"))
        self.assertFalse(private.isValidHour(2))
    
        
    def testIsYesNo(self):
        self.assertTrue(private.isYesNo("yes"))
        self.assertTrue(private.isYesNo("no"))

        self.assertFalse(private.isYesNo("3:59"))
        self.assertFalse(private.isYesNo(1))

    
    def testIsValidPause(self):
        for i in range(1,11):
            self.assertTrue(private.isValidPause(i))

        self.assertFalse(private.isValidPause(-11))
        self.assertFalse(private.isValidPause(40))

#collectUserInput and askUser in the FirstConfiguration class are not tested

if __name__ == '__main__':
    unittest.main()