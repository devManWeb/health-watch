'''
This is the main timer. Based on the current hour and minute, 
we determine if it's time to take a break, to work or it is lunch time.
#FIXME:this script still crashes when we are in pause
'''	
from threading import Timer

from project.src.config import ConfigIO
from project.src.common import CommonMethods
from project.src.notification import UserNotification	

cfg = ConfigIO()
comm = CommonMethods()
notify = UserNotification()

class OnlyForThisFile():
    #specific methods to be used only in this file

	def compareTime(self,start,actual,end):
		'''
		is actual between start and end?
		actual,start and end must be lists of integers (hours and minutes)
		this function returns True or False when there is no error
		08/08/2019: actual was added to the params for testing purpose
		'''
		startSec = comm.convertToSeconds(start)
		actualSec = comm.convertToSeconds(actual)
		endSec = comm.convertToSeconds(end)

		if endSec > startSec:
			#are the start and end in the same day?	
			return startSec < actualSec < endSec
		elif endSec < startSec:
			#if the start is in a day and the end in the other
			if start[0] <= actual[0] <= 23:
				return startSec < actualSec < (24 * 3600)
			else:
				return 0 <= actualSec < endSec
		else:
			raise ValueError("Interval equal to zero")

	def timeTo(self,actual,endValue):
		'''
		how much time is left (in seconds) from actual to endValue?
		actual and toConfront are lists of integers (hours and minutes)
		08/08/2019: actual was added to the params for testing purpose
		'''
		actualSec = comm.convertToSeconds(actual)
		endValueSec = comm.convertToSeconds(endValue)

		result = endValueSec - actualSec
		if(result > 0):
			return result
		else:
			raise ValueError("Negative interval!")

	def isInPause(self,startPause, actual, pauseDuration):
		'''
		If we're working, is it time to take a break? 
		To calculate this, we take the starting minutes and add the work minutes
		startPause and actual are lists of integers (hours and minutes)
		pauseDuration is an integer in minutes
		08/08/2019: actual was added to the params for testing purpose
		'''
		actualMinute = actual[1]
		workDuration = 60 - pauseDuration
		startPauseMinute = comm.formatMinute(startPause[1] + workDuration)
		endpauseMinute = comm.formatMinute(startPauseMinute + pauseDuration)

		if startPauseMinute > endpauseMinute:
			#if the end minutes are in the next hour
			if (startPauseMinute <= actualMinute <= 59) or (0 <= actualMinute <= endpauseMinute):
				return True
			else:
				return False
		else:
			#if the start and end minutes are in the same hour
			if startPauseMinute <= actualMinute < endpauseMinute:
				return True
			else:
				return False

	def minToSeconds(self,mins):
		#converts integers minutes to seconds
		if(type(mins) != int):
			raise TypeError("Must be integers")
		else:
			return mins * 60

	def getActualStart(self,actual,startPoint):
		'''
		with this app we calculate the actual start hour
		to be used for notify.setInterval()
		we take the actual hour and the minute of startPoint
		if startPoint minutes are bigger than actual minutes,
		we reduce the return value hours by one
		this is used with workStart or lunchEnd
		'''
		if startPoint[1] > actual[1]:	
			realStartHour = actual[0] - 1
			if realStartHour < 0:
				realStartHour = 23
		else:
			realStartHour = actual [0]
		return [realStartHour,startPoint[1]]


private = OnlyForThisFile()


class ClockManager():

	def __init__(self):

		self.workStart = cfg.readTime("workstart")
		self.workEnd = cfg.readTime("workend")
		self.lunchStart = cfg.readTime("lunchstart")
		self.lunchEnd = cfg.readTime("lunchend")
		self.isPartTime = cfg.readProp("isparttime")
		self.pauseLength = int(cfg.readProp("pauseLength"))
		self.workLenght = 60 - self.pauseLength
		self.actualStart = [0,0]

	def timeChecker(self):
		'''
		This function checks the current time and confronts it the timetables
		calls the notification methods with the correct arguments
		FIXME:if we are in the last working hour, we might get a wrong result
		'''
		actualTime = comm.getActualTime()
		timerValue = 20 #change this for the update frequency, now is every 20seconds
	
		if self.isPartTime == "yes":

			if private.compareTime(self.workStart,actualTime,self.workEnd):
				
				self.actualStart = private.getActualStart(actualTime,self.workStart)
				
				if private.isInPause(self.workStart,actualTime,self.pauseLength):
					notify.message("Time to take a break!")
					notify.setInterval(self.actualStart,self.pauseLength,self.workLenght)		
				else:
					notify.message("Time to work now!")
					notify.setInterval(self.actualStart,self.workLenght,0)

				notify.showProgressBar().start()
				Timer(timerValue, self.timeChecker).start()

			else:
				notify.message("Now it's not time to work!","exit")

		elif self.isPartTime == "no":

			if private.compareTime(self.workStart,actualTime,self.lunchStart):

				self.actualStart = private.getActualStart(actualTime,self.workStart)

				if private.isInPause(self.workStart,actualTime,self.pauseLength):
					notify.message("Time to take a break!")
					notify.setInterval(self.actualStart,self.pauseLength,self.workLenght)
				else:
					notify.message("Time to work now!")
					notify.setInterval(self.actualStart,self.workLenght,0)

				notify.showProgressBar()
				Timer(timerValue, self.timeChecker).start()

			elif private.compareTime(self.lunchStart,actualTime,self.lunchEnd):

				notify.message("Time to go eating!")
				notify.setStartEnd(self.lunchStart,self.lunchEnd)

				notify.showProgressBar()
				Timer(timerValue, self.timeChecker).start()

			elif private.compareTime(self.lunchEnd,actualTime,self.workEnd):

				self.actualStart = private.getActualStart(actualTime,self.lunchEnd)
				
				if private.isInPause(self.lunchEnd,actualTime,self.pauseLength):
					notify.message("Time to take a break!")
					notify.setInterval(self.actualStart,self.pauseLength,self.workLenght)
				else:
					notify.message("Time to work now!")
					notify.setInterval(self.actualStart,self.workLenght,0)

				notify.showProgressBar()
				Timer(timerValue, self.timeChecker).start()

			else:
				notify.message("Now it's not time to work!","exit")