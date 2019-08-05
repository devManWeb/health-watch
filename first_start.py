''' 
This moduled is used at the first time, 
when we need to configure the work time bands
'''
import re
from config import ConfigIO

cfg = ConfigIO()

class firstConfiguration():

    def __init__(self):
        print("\nFirst configuration procedure")
        print("Please enter the required hours (leave empty to confirm the default value)\n")

    def isValidHour(self,userInput):
        '''
        is the entered data is in the correct time format AA:BB or A:BB?
        is the inserted interval within the numerical limits allowed?
        '''
        userInput = str(userInput)
        if (4 <= len(userInput) <= 6) and re.match(r'(\d)?\d:\d\d',userInput):
            userArr = userInput.split(":")
            if 0 <= int(userArr[0]) <= 23 and 0 <= int(userArr[1]) <= 59:
                return True
            else:
                return False
        else:
            return False

    def collectUserInput(self,inputTxt,configIndex):
        #Collects the data in the correct format
        insertedValue = str(input(inputTxt))
        if not insertedValue:
            #if the inserted string is empty
            print("Previous value keeped!")
        elif self.isValidHour(insertedValue) == False:
            print("Invalid value, try again!")
            self.collectUserInput(inputTxt,configIndex)
        else:
            cfg.writeProp(configIndex,insertedValue)

    def askUser(self): 
        self.collectUserInput("Enter the work start time (default 08:30): ","workStart")
        self.collectUserInput("Enter the work end time (default 18:00): ","workEnd")
        self.collectUserInput("Enter the start time of the lunch break (default 12:30): ","lunchStart")
        self.collectUserInput("Enter the end time of the lunch break (default 14:00): ","lunchEnd")
        cfg.writeProp("configured","yes")