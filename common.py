#metodi comuni usati nei vari file python
from datetime import datetime

class CommonMethods():

    def getActualTime(self):
        #returns an array with current integer hours and minutes
        actual = datetime.now().strftime('%H:%M').split(":")
        actual = [int(x) for x in actual]
        return actual

    def convertToSeconds(self,arrToConvert):
        #converts an array of strings into an int of seconds
        hours = arrToConvert[0]
        minutes = arrToConvert[1]
        return int(hours) * 3600 + (int(minutes) * 60)

    def formatMinute(self,minute):
        #if we exceed 59 minutes, we start from 0
        if minute > 59:
            minute = minute - 60
        return minute