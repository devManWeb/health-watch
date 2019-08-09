import unittest

from project.src.notification import UserNotification

toTest = UserNotification()

class TestNotificationMethods(unittest.TestCase):
    
    '''
    this methods should always start with "test"
    message() not tested
    setStartEnd() setInterval() are used in testGetBarLength1/2
    '''

    def testGetBarLength1(self):

        #test of getBarLength with setStartEnd()

        startEndValues = [
            #same day
            [[8,55],[8,56],[8,57],50.0],
            [[7,33],[10,5],[11,40],61.5],
            [[15,9],[17,23],[20,56],38.6],
            [[12,0],[12,56],[13,0],93.3],
            [[7,8],[8,56],[9,59],63.1],
            [[1,2],[2,5],[3,4],51.6],
            #different days
            [[23,0],[0,0],[1,0],50.0],
            [[22,30],[0,1],[0,30],75.8],
            [[15,27],[1,20],[3,34],81.6],
            [[23,59],[0,55],[0,56],98.2],
            [[21,15],[3,22],[4,0],90.6],
            [[22,51],[4,4],[5,55],73.8]
        ]

        for index in startEndValues:
           
            newStart = index[0]
            actual = index[1]
            newEnd = index[2] 
            expectedBarValue = index[3]
            
            toTest.setStartEnd(newStart,newEnd)
            self.assertAlmostEqual(
                toTest.getBarLength(actual),
                expectedBarValue,
                delta = 0.5
            )
        
        startEndExceptions = [
            #same day
            [[8,55],[9,56],[8,57],33.3],
            [[7,8],[11,12],[9,59],53.3],
            #different days
            [[23,59],[13,12],[0,56],13.3],
            [[21,15],[20,5],[4,0],73.0],
        ]

        for index in startEndExceptions:
            with self.assertRaises(ValueError):
                newStart = index[0]
                actual = index[1]
                newEnd = index[2] 
                toTest.setStartEnd(newStart,newEnd)
                toTest.getBarLength(actual)
    
    def testGetBarLength2(self):

        #test of getBarLength with setInterval

        setIntervalValue = [
            #same day
            [[8,55],[9,57],59,10,88.1],
            [[7,33],[8,30],55,5,94.5],
            [[13,9],[14,0],50,10,82.0],
            [[21,50],[22,45],10,50,50.0],
            [[7,8],[8,5],5,55,40.0],
            [[2,2],[3,7],10,59,60.0],
            #different days
            [[23,50],[0,20],50,10,40.0],
            [[22,59],[0,15],60,60,26.7],
            [[23,40],[0,15],50,20,30.0],
            [[23,1],[0,5],55,15,89.0],
            [[23,40],[0,0],50,10,20.0],
            [[23,10],[0,7],45,15,93.3]
        ]

        for index in setIntervalValue: 
            
            newStart = index[0]
            actual = index[1] 
            minutes = index[2]
            delay = index[3]
            expectedBarValue = index[4]

            toTest.setInterval(newStart,minutes,delay)
            self.assertAlmostEqual(
                toTest.getBarLength(actual),
                expectedBarValue,
                delta = 0.5
            )

        intervalExceptions = [
            #same day
            [[8,55],[10,57],59,10,88.1],
            [[7,33],[14,30],55,5,94.5],
            #different days
            [[23,40],[7,0],50,10,20.0],
            [[22,10],[0,7],45,15,93.3]
        ]

        for index in intervalExceptions:

            newStart = index[0]
            actual = index[1] 
            minutes = index[2]
            delay = index[3]
            expectedBarValue = index[4]

            with self.assertRaises(ValueError):
                toTest.setInterval(newStart,minutes,delay)
                toTest.getBarLength(actual)           

#drawBar and showProgressBar in the class OnlyForThisFile are not tested

if __name__ == '__main__':
    unittest.main()