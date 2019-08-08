''' 
This moduled is used at the first time, 
when we need to configure the work time bands
'''
import re

from project.src.config import ConfigIO  

cfg = ConfigIO()

class FirstConfiguration():

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
        return False #if the other cases are not valid

    def isYesNo(self,userInput):
        #checks if the input is "yes" or "no"
        userInput = str(userInput).lower()
        if userInput == "yes" or userInput == "no":
            return True
        else:
            return False

    def isValidPause(self,userInput):
        #the pause must be between 1 and 10 minutes
        userInput = int(userInput)
        if 0 < userInput <= 10:
            return True
        else:
            return False

    def collectUserInput(self,inputTxt,configIndex,typeInput):
        '''
        Collects the data in the correct format
        inputTxt is the user data to be checked
        configIndex is the name in the .ini configuration file
        typeInput is the type to be inserted (hour/yesNo/pause)
        '''

        def controlInput(test,param):
            '''
            control the inserted data with the right test
            we pass param to controlInput
            '''
            if test == False:
                print("Invalid value, try again!")
                self.collectUserInput(inputTxt,configIndex,param)
                return False
            else:
                cfg.writeProp(configIndex,insertedValue)     
                return True 

        insertedValue = str(input(inputTxt))            

        if not insertedValue:
            #if the inserted string is empty
            print("Previous value keeped!")

        elif typeInput == "hour":
            controlInput(self.isValidHour(insertedValue),"hour")

        elif typeInput == "yesNo":
            controlInput(self.isYesNo(insertedValue),"yesNo")

        elif typeInput == "pause":
            controlInput(self.isValidPause(insertedValue),"pause")

        else:
            print("Invalid input, try again!")
            cfg.writeProp(configIndex,insertedValue)
            return False

    def askUser(self): 
        print("\nFirst configuration procedure")
        print("Please enter the required hours (leave empty to confirm the default value)\n")
        self.collectUserInput("Enter the work start time (default 08:30): ","workstart","hour")
        self.collectUserInput("Enter the work end time (default 18:00): ","workend","hour")
        self.collectUserInput("Is the work part-time? (default no): ","isparttime","yesNo")
        if cfg.readProp("isparttime") == "no":
            #only if there is a full time job
            self.collectUserInput("Enter the start time of the lunch break (default 12:30): ","lunchstart","hour")
            self.collectUserInput("Enter the end time of the lunch break (default 14:00): ","lunchend","hour")
        self.collectUserInput("Enter the length of the pause (1-10 minutes, default 5): ","pauselength","pause")
        cfg.writeProp("isconfigured","yes")