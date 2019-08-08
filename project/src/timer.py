'''
This is the main timer. Based on the current hour and minute, 
we determine if it's time to take a break, to work or it is lunch time.
'''	
from threading import Timer

from project.src.config import ConfigIO
from project.src.common import CommonMethods
from project.src.notification import UserNotification	

cfg = ConfigIO()
comm = CommonMethods()
notify = UserNotification()

class HealthTimer():

	def compareTime(self,start,actual,end):
		'''
		is actual between start and end?
		actual,start and end must be lists of integers (hours and minutes)
		this function returns True or False when with no error
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

	def clock(self):

		workStart = cfg.readTime("workstart")
		workEnd = cfg.readTime("workend")
		lunchStart = cfg.readTime("lunchstart")
		lunchEnd = cfg.readTime("lunchend")
		isPartTime = cfg.readProp("isparttime")
		pauseLength = int(cfg.readProp("pauseLength"))
		workLenght = 60 - pauseLength

		actualTime = comm.getActualTime()

		def timeChecker():

			def minToSec(mins):
				return mins * 60

			timerValue = 0
		
			if isPartTime == "yes":

				if self.compareTime(workStart,actualTime,workEnd):
					if self.isInPause(workStart,actualTime,pauseLength):
						timerValue = minToSec(pauseLength)
						Timer(timerValue, timeChecker).start()

						notify.message("Time to take a break!")
						notify.setInterval(workStart,pauseLength,workLenght)
						notify.showProgressBar()
					else:
						#FIXME:stop work at endWork
						timerValue = minToSec(workLenght)
						Timer(timerValue, timeChecker).start()

						notify.message("Time to work now!")
						notify.setInterval(workStart,workLenght,0)
						notify.showProgressBar()

				else:
					notify.message("Now it's not time to work!","exit")

			elif isPartTime == "no":

				if self.compareTime(workStart,actualTime,lunchStart):
					if self.isInPause(workStart,actualTime,pauseLength):
						timerValue = minToSec(pauseLength)
						Timer(timerValue, timeChecker).start()

						notify.message("Time to take a break!")
						notify.setInterval(workStart,pauseLength,workLenght)
						notify.showProgressBar()
					else:
						timerValue = minToSec(workLenght)
						Timer(timerValue, timeChecker).start()

						notify.message("Time to work now!")
						notify.setInterval(workStart,workLenght,0)
						notify.showProgressBar()

				elif self.compareTime(lunchStart,actualTime,lunchEnd):
					timerValue = self.timeTo(actualTime,lunchEnd)
					Timer(timerValue, timeChecker).start()

					notify.message("Time to go eating!")
					notify.setStartEnd(lunchStart,lunchEnd)
					notify.showProgressBar()

				elif self.compareTime(lunchEnd,actualTime,workEnd):
					if self.isInPause(lunchEnd,actualTime,pauseLength):
						timerValue = minToSec(pauseLength)
						Timer(timerValue, timeChecker).start()
						#FIXME:pause not starting
						notify.message("Time to take a break!")
						notify.setInterval(lunchEnd,pauseLength,workLenght)
						notify.showProgressBar()
					else:
						#FIXME:stop work at endWork
						timerValue = minToSec(workLenght)
						Timer(timerValue, timeChecker).start()

						notify.message("Time to work now!")
						notify.setInterval(lunchEnd,workLenght,0)
						notify.showProgressBar()

				else:
					notify.message("Now it's not time to work!","exit")

		timeChecker() #first timer initialization