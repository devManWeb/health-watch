#Common methods used in a lot of python files

from datetime import datetime

class CommonMethods():

    def getActualTime(self):
        #returns a list with current integer hours and minutes
        actual = datetime.now().strftime('%H:%M').split(":")
        actual = [int(x) for x in actual]
        return actual

    def convertToSeconds(self,arrToConvert):
        '''
        converts a list of integers (hours and minutes) to seconds
        performs a check if hours and minutes are valid
        '''
        hours = arrToConvert[0]
        minutes = arrToConvert[1]

        if isinstance(hours, int) and isinstance(minutes, int):
            if 0 <= hours <= 23 and  0 <= minutes <= 59:
                return int(hours) * 3600 + (int(minutes) * 60)
            else:
                raise ValueError("Hours and/or minutes too big")
        else:
            raise TypeError("Hours or minutes are not integers")

    def formatMinute(self,minute):
        #if we exceed 59 minutes, we start from 0
        if isinstance(minute, int):
            if 0 <= minute <= 59:
                return minute
            elif minute >= 60:
                minute = minute - 60
                return minute 
            elif minute >= 120:
                raise ValueError("Number too big")
            else:
                raise TypeError("Negative number")
        else:
            raise TypeError("Minute is not an integer")