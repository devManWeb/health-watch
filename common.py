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
        return (int(arrToConvert[0]) * 3600) + (int(arrToConvert[1]) * 60)