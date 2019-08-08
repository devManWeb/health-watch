import unittest
from project.src.common import CommonMethods

toTest = CommonMethods()

class TestCommonMethods(unittest.TestCase):

    #this methods should always start with "test"

    def testActualTime(self):
        self.assertTrue(type(toTest.getActualTime()) is list)
        self.assertTrue(type(toTest.getActualTime()[0]) is int)
        self.assertTrue(type(toTest.getActualTime()[1]) is int)

    def testConvertSec(self):
        self.assertEqual(toTest.convertToSeconds([8,59]),32340, "Should be 32340")
        self.assertEqual(toTest.convertToSeconds([11,12]),40320, "Should be 40320")
        self.assertEqual(toTest.convertToSeconds([3,0]),10800, "Should be 10800")
        with self.assertRaises(TypeError):
            toTest.convertToSeconds(["3","0"])
            toTest.convertToSeconds([3,"08"])
        with self.assertRaises(ValueError):
            toTest.convertToSeconds([27,400])
            toTest.convertToSeconds([3,61])
            toTest.convertToSeconds([25,59])

    def testFormatMin(self):

        self.assertEqual(toTest.formatMinute(59),59, "Should be 59")
        self.assertEqual(toTest.formatMinute(115),55, "Should be 55")
        self.assertEqual(toTest.formatMinute(75),15, "Should be 15")      
        self.assertEqual(toTest.formatMinute(0),0, "Should be 0") 
        with self.assertRaises(TypeError):
            toTest.formatMinute(-3)
            toTest.formatMinute("3")
            toTest.formatMinute(10000)

if __name__ == '__main__':
    unittest.main()