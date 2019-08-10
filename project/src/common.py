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

    def addMinutesToHour(self,hour,minutesToAdd):
        '''
        TODO:write tests for this
        this method is used for adding minutesToAdd to hour
        hour is a list of integers (hours,minutes)
        minutesToAdd is an integer in minutes
        if we get an hour over 23:59, we fix it
        if minutesToAdd > 60, we get a ValueError
        '''

        if minutesToAdd > 60:
            raise ValueError("Adding more than 60 minutes")

        addHours = int(minutesToAdd // 60)
        addMinutes = minutesToAdd - (addHours * 60)
        
        resultHours = hour[0] + addHours
        resultMinutes = hour[1] + addMinutes

        extraMin = 0
        extraHour = 0

        if resultMinutes > 59:
            extraMin = resultMinutes - 60
            resultMinutes = extraMin
            resultHours = resultHours + 1

        if resultHours > 23:
            extraHour = resultHours - 24
            resultHours = extraHour

        return [resultHours,resultMinutes]