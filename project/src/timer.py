'''
This is the main timer. Based on the current hour and minute, 
we determine if it's time to take a break, to work or it is lunch time.
'''	
from threading import Timer
from pynput import keyboard, mouse

from project.src.config import ConfigIO
from project.src.common import CommonMethods
from project.src.notification import UserNotification	
from project.src.track_usage import TrackUsage	

cfg = ConfigIO()
comm = CommonMethods()
notify = UserNotification()
usageStat = TrackUsage()

class OnlyForThisFile():
    #specific methods to be used only in this file

	def compareTime(self,start,actual,end):
		'''
		is actual between start and end?

		arguments
			actual,start and end: lists of integers (hours and minutes)
		return
			True or False when there is no error
		raise
			ValueError if the interval is equal to 0 seconds
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
		14/08/2019: fix for hours in different days

		arguments
			actual and toConfront: lists of integers (hours and minutes)
		return 
			seconds value between actual and end		
		'''
		actualSec = comm.convertToSeconds(actual)
		endValueSec = comm.convertToSeconds(endValue)

		if endValueSec < actualSec:
			endValueSec = endValueSec + (24 * 60 * 60) #we add an entire day
		
		return endValueSec - actualSec

	def isInPause(self, startPause, actual, pauseDuration):
		'''
		If we're working, is it time to take a break? 

		arguments
			startPause and actual are lists of integers (hours and minutes)
			pauseDuration is an integer in minutes
		return
			True or False
		'''
		actualMinute = actual[1]
		workDuration = 60 - pauseDuration
		startPauseMinute = comm.formatMinute(startPause[1] + workDuration)
		endpauseMinute = comm.formatMinute(startPauseMinute + pauseDuration)

		if startPauseMinute > endpauseMinute:
			#if the end minutes are in the next hour
			if (startPauseMinute <= actualMinute <= 59) or (0 <= actualMinute < endpauseMinute):
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
		arguments
			actual,startPoint: list of integers (hours and minutes)
		return
			list of integers with the actual start
		'''
		if startPoint[1] > actual[1]:	
			
			'''
			if startPoint minutes are bigger than actual minutes,
			we reduce the return value hours by one
			'''
			realStartHour = actual[0] - 1
			if realStartHour < 0:
				realStartHour = 23
		else:
			realStartHour = actual[0]
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
		self.pastMousePosition = [0,0]	
		self.healthPoints = 0
		self.lockPoints = True

	def timeChecker(self):
		'''
		This function checks the current time and confronts it the timetables
		calls the notification methods with the correct arguments
		'''
		actualTime = comm.getActualTime()

		def calculatePausesDone(suppliedActualTime):	
			'''
			arguments
				suppliedActualTime: actual time (list of integers [HH,MM])
			return
				total number of pauses
				those already done by the user
			#FIXME:possible bug here with different timebands
			'''
			totalWorkTime = private.timeTo(self.workStart,self.workEnd)
			timePassed = private.timeTo(self.workStart,suppliedActualTime)

			if self.isPartTime == "no":
				lunchTimeSeconds = private.timeTo(self.lunchStart,self.lunchEnd)
				totalWorkTime = totalWorkTime - lunchTimeSeconds

				if private.compareTime(self.lunchEnd,suppliedActualTime,self.workEnd):
					'''
					subtract the lunchtime only if the lunch is already ended
					'''
					timePassed = timePassed - lunchTimeSeconds

			totalPauses = totalWorkTime // 3600
			alreadyDone = timePassed // 3600

			return [totalPauses,alreadyDone]	

		def calculateTimer(end,minutes,delay):
			'''
			this function calculates the values to pass to notify.setInterval
			if we are in the last hour, we send the correct remaining time
			
			arguments
				end: end value (in minutes) of the last working hour
				minutes and delay: refer to notify.setInterval
			'''
			timeToNextEvent = int(private.timeTo(self.actualStart,end) / 60)
			if timeToNextEvent < minutes:
				notify.setInterval(self.actualStart,timeToNextEvent,delay)
			else:
				notify.setInterval(self.actualStart,minutes,delay)

		def fireNextTimer(showInfo = True):
			'''
			show the progress bar and start the update timer
			arguments
				arguments: show pauses already done, ecc.. (default True)
			'''
			timerValue = 10 #update frequency in seconds
			if showInfo:
				pausesData = calculatePausesDone(actualTime)
				notify.setPausesData(pausesData)
				notify.showData()
			Timer(timerValue, self.timeChecker).start()

		def checkHealthPoints(deltaVar=1):
			'''
			function for calculating the health points
			we increase or lower the score (no negative numbers)
			if self.lockPoints is False, points are not changed
			arguments
				deltaVar: positive or negative int to add
			'''
			if not self.lockPoints and self.healthPoints >= 0:
				self.healthPoints = self.healthPoints + deltaVar
				self.healthPoints = round(self.healthPoints,1)	


		#################### Main logic of the cycle ####################

		notify.setLunchStatus(False) #False as default

		#we monitor the mouse and the keyboard for the health points 
		usageStat.setCallBack(checkHealthPoints(0.1))
		usageStat.run()
	
		if self.isPartTime == "yes":

			if private.compareTime(self.workStart,actualTime,self.workEnd):
				
				self.actualStart = private.getActualStart(actualTime,self.workStart)
				
				if private.isInPause(self.workStart,actualTime,self.pauseLength):
					notify.message("Time to take a break!")
					calculateTimer(self.workEnd,self.pauseLength,self.workLenght)
					self.lockPoints = False
					checkHealthPoints()
				else:
					notify.message("Time to work now!")
					calculateTimer(self.workEnd,self.workLenght,0)
					self.lockPoints = True

				fireNextTimer()

			else:
				notify.message("Now it's not time to work!")
				fireNextTimer(False)
				self.lockPoints = True
				self.healthPoints = 0

		elif self.isPartTime == "no":

			if private.compareTime(self.workStart,actualTime,self.lunchStart):

				self.actualStart = private.getActualStart(actualTime,self.workStart)

				if private.isInPause(self.workStart,actualTime,self.pauseLength):
					notify.message("Time to take a break!")
					calculateTimer(self.lunchStart,self.pauseLength,self.workLenght)
					self.lockPoints = False
					checkHealthPoints()
				else:
					notify.message("Time to work now!")
					calculateTimer(self.lunchStart,self.workLenght,0)
					self.lockPoints = True

				fireNextTimer()

			elif private.compareTime(self.lunchStart,actualTime,self.lunchEnd):
				notify.message("Time to go eating!")
				notify.setStartEnd(self.lunchStart,self.lunchEnd)
				self.lockPoints = True
				fireNextTimer()

			elif private.compareTime(self.lunchEnd,actualTime,self.workEnd):

				notify.setLunchStatus(True)
				self.actualStart = private.getActualStart(actualTime,self.lunchEnd)
				
				if private.isInPause(self.lunchEnd,actualTime,self.pauseLength):
					notify.message("Time to take a break!")
					calculateTimer(self.workEnd,self.pauseLength,self.workLenght)
					self.lockPoints = False
					checkHealthPoints()
				else:
					notify.message("Time to work now!")
					calculateTimer(self.workEnd,self.workLenght,0)
					self.lockPoints = True

				fireNextTimer()

			else:
				notify.message("Now it's not time to work!")
				fireNextTimer(False)
				self.healthPoints = 0
				self.lockPoints = True	

		notify.showHealthPoints(self.healthPoints)