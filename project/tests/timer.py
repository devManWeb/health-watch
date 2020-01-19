import unittest
from time import sleep

from project.src.timer import OnlyForThisFile

private = OnlyForThisFile()

class TestTimerMethods(unittest.TestCase):
    
    #this methods should always start with "test"

    def testBetweenTwoHours(self):

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
            self.assertTrue(private.compareTime(start,actual,end))    
        
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
            self.assertFalse(private.compareTime(start,actual,end))    
        
        valueErrorConditions = [
            [[22,22],[22,22],[22,22]]
        ]

        for index in valueErrorConditions:
            start = index[0]
            actual = index[1]
            end = index[2]
            with self.assertRaises(ValueError):
                private.compareTime(start,actual,end)
        

    def testTimeTo(self):

        arguments = [
            #same day
            [[8,59],[9,34],2100],
            [[7,25],[12,0],16500],
            [[0,2],[9,7],32700],
            [[23,7],[23,34],1620],
            [[1,2],[3,4],7320],
            [[0,0],[0,34],2040],
            #diffent days
            [[9,34],[8,59],84300],
            [[10,0],[7,25],77100],
            [[9,7],[0,2],53700],
            [[23,34],[23,7],84780],
            [[3,4],[1,2],79080],
            [[0,34],[0,0],84360]
        ]

        for index in arguments:
            actual = index[0]
            endValue = index[1]
            result = index[2]
            self.assertEqual(private.timeTo(actual,endValue),result)
        
                
    def testIntervals(self):

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
            self.assertTrue(private.isInPause(startPause,actual,pauseDuration))    
          
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
            self.assertFalse(private.isInPause(startPause,actual,pauseDuration))    


    def testMinToSeconds(self):

        intValues = [
            [56,3360],
            [3,180],
            [73,4380]
        ]

        for index in intValues:
            self.assertEqual(private.minToSeconds(index[0]),index[1])

        typeErrorConditions = [
            [[8,55],5],
            ["12",9]           
        ]

        for index in typeErrorConditions:
            with self.assertRaises(TypeError):
                private.minToSeconds(index[0])

        
    def testGetActualStart(self):

        listValues = [
            [[23,57],[22,12],[23,12]],
            [[23,11],[22,12],[22,12]],
            [[3,47],[15,36],[3,36]],
            [[3,35],[15,36],[2,36]],
            [[0,59],[11,59],[0,59]],
            [[2,0],[1,0],[2,0]],
            [[21,00],[14,0],[21,0]],
            [[0,27],[23,59],[23,59]],
            [[15,57],[16,0],[15,0]]
        ]
        
        for index in listValues:
            actual = index[0]
            startPoint = index[1]
            result = index[2]

            self.assertEqual(private.getActualStart(actual,startPoint),result)         

    def testGetIdleTime(self):
        #we only check the type here - one every second
        print("Testing getIdleTime...")
        for i in range (0,10):
            self.assertTrue(type(private.getIdleTime()) is float) 
            sleep(1)

#class ClockManager is not tested

if __name__ == '__main__':
    unittest.main()