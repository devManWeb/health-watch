import unittest

from project.src.timer import HealthTimer

toTest = HealthTimer()

class TestTimerMethods(unittest.TestCase):
    
    #this methods should always start with "test"

    def testCompareTime(self):

        trueConditions = [
            #same day
            [[1,0],[6,0],[7,9]],
            [[5,22],[8,23],[19,45]],
            [[0,0],[2,58],[22,6]],
            [[22,1],[23,34],[23,35]],
            [[23,57],[23,58],[23,59]],
            #in two different days
            [[19,22],[8,23],[9,45]],
            [[23,58],[6,0],[7,9]],
            [[23,16],[2,58],[22,6]],
            [[20,1],[23,58],[4,35]],
            [[23,58],[23,59],[0,0]],
        ]

        for index in trueConditions:
            start = index[0]
            actual = index[1]
            end = index[2]
            self.assertTrue(toTest.compareTime(start,actual,end))    
        
        falseConditions = [
            #same day
            [[1,0],[0,3],[7,9]],
            [[5,22],[4,23],[19,45]],
            [[0,0],[23,58],[22,6]],
            [[22,1],[11,34],[23,35]],
            [[23,57],[0,58],[23,59]],
            #in two different days
            [[19,22],[10,23],[9,45]],
            [[23,58],[22,0],[7,9]],
            [[23,16],[23,0],[22,6]],
            [[20,1],[19,4],[4,35]],
            [[23,58],[11,19],[0,0]]
        ]

        for index in falseConditions:
            start = index[0]
            actual = index[1]
            end = index[2]
            self.assertFalse(toTest.compareTime(start,actual,end))    
        
        valueErrorConditions = [
            [[22,22],[22,22],[22,22]]
        ]

        for index in valueErrorConditions:
            start = index[0]
            actual = index[1]
            end = index[2]
            with self.assertRaises(ValueError):
                toTest.compareTime(start,actual,end)
        

    def testTimeTo(self):

        arguments = [
            [[8,59],[9,34],2100],
            [[7,25],[12,0],16500],
            [[0,2],[9,7],32700],
            [[23,7],[23,34],1620],
            [[1,2],[3,4],7320],
            [[0,0],[0,34],2040]
        ]

        for index in arguments:
            actual = index[0]
            endValue = index[1]
            result = index[2]
            self.assertEqual(toTest.timeTo(actual,endValue),result)
     
        valueErrorConditions = [
            [[12,59],[0,34]],
            [[15,25],[12,0]],
            [[0,2],[0,0]]
        ]

        for index in valueErrorConditions:
            actual = index[0]
            endValue = index[1]
            with self.assertRaises(ValueError):
                toTest.timeTo(actual,endValue)
        
                
    def testIsInPause(self):

        trueConditions = [
            [[8,55],[9,52],5],
            [[9,12],[10,7],9],
            [[10,56],[11,55],1],
            [[23,58],[0,56],4],
            [[0,0],[0,57],7],
            [[23,59],[0,57],5]
        ]

        for index in trueConditions:
            startPause = index[0]
            actual = index[1]
            pauseDuration = index[2]
            self.assertTrue(toTest.isInPause(startPause,actual,pauseDuration))    
    
        
        falseConditions = [
            [[8,55],[9,0],5],
            [[9,12],[10,12],9],
            [[10,56],[11,59],1],
            [[23,58],[0,5],4],
            [[0,0],[1,12],7],
            [[23,59],[0,13],5]
        ]

        for index in falseConditions:
            startPause = index[0]
            actual = index[1]
            pauseDuration = index[2]
            self.assertFalse(toTest.isInPause(startPause,actual,pauseDuration))    
        

    #clock is not tested


if __name__ == '__main__':
    unittest.main()