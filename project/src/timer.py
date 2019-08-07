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

	def __init__(self):
		self.workStart = cfg.readTime("workstart")
		self.workEnd = cfg.readTime("workend")
		self.lunchStart = cfg.readTime("lunchstart")
		self.lunchEnd = cfg.readTime("lunchend")
		self.isPartTime = cfg.readProp("isparttime")
		self.pauseLength = int(cfg.readProp("pauseLength"))
		self.workLenght = 60 - self.pauseLength

	def isInSingleDay(self):
		#are the start and end times on the same day?
		if self.workEnd[0] > self.workStart[0]:
			return True
		else:
			return False

	def compareTime(self,start,end):
		#is the current time between start and end?
		def inSeconds(array):
			return (array[0] * 3600) + (array[1] * 60)

		actual = comm.getActualTime()
		actualSec = inSeconds(actual)
		startSec = inSeconds(start)
		endSec = inSeconds(end)

		if self.isInSingleDay():	
			return startSec < actualSec < endSec
		else:
			if end[0] <= actual[0] <= 23:
				return startSec < actualSec < (24 * 3600)
			else:
				return 0 < actualSec < endSec

	def timeTo(self,secondValue):
		#how much time is left (in seconds) from now to secondValue?
		actual = comm.getActualTime()
		convertedHours = (secondValue[0] - actual[0]) * 3600
		convertedMinutes = (secondValue[0] - actual[0]) * 60
		result = convertedHours + convertedMinutes
		if(result > 0):
			return result
		else:
			raise Exception("Negative interval!")

	def isInPause(self):
		'''
		If we're working, is it time to take a break?
		To calculate this, we take the starting minutes and add the work minutes
		'''
		actualMinute = comm.getActualTime()[1]
		startPauseMinute = comm.formatMinute(self.workStart[1] + 55)
		endpauseMinute = comm.formatMinute(startPauseMinute + 5)

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

		def timeChecker():

			def minToSec(mins):
				return mins * 60

			timerValue = 0
		
			if self.isPartTime == "yes":

				if self.compareTime(self.workStart,self.workEnd):
					if self.isInPause():
						timerValue = minToSec(self.pauseLength)
						Timer(timerValue, timeChecker).start()

						notify.message("Time to take a break!")
						notify.setInterval(self.workStart,self.pauseLength,self.workLenght)
						notify.showProgressBar()
					else:
						#FIXME:stop work at endWork
						timerValue = minToSec(self.workLenght)
						Timer(timerValue, timeChecker).start()

						notify.message("Time to work now!")
						notify.setInterval(self.workStart,self.workLenght,0)
						notify.showProgressBar()

				else:
					notify.message("Now it's not time to work!","exit")

			elif self.isPartTime == "no":

				if self.compareTime(self.workStart,self.lunchStart):
					if self.isInPause():
						timerValue = minToSec(self.pauseLength)
						Timer(timerValue, timeChecker).start()

						notify.message("Time to take a break!")
						notify.setInterval(self.workStart,self.pauseLength,self.workLenght)
						notify.showProgressBar()
					else:
						timerValue = minToSec(self.workLenght)
						Timer(timerValue, timeChecker).start()

						notify.message("Time to work now!")
						notify.setInterval(self.workStart,self.workLenght,0)
						notify.showProgressBar()

				elif self.compareTime(self.lunchStart,self.lunchEnd):
					timerValue = self.timeTo(self.lunchEnd)
					Timer(timerValue, timeChecker).start()

					notify.message("Time to go eating!")
					notify.setStartEnd(self.lunchStart,self.lunchEnd)
					notify.showProgressBar()

				elif self.compareTime(self.lunchEnd,self.workEnd):
					if self.isInPause():
						timerValue = minToSec(self.pauseLength)
						Timer(timerValue, timeChecker).start()
						#FIXME:pause not starting
						notify.message("Time to take a break!")
						notify.setInterval(self.lunchEnd,self.pauseLength,self.workLenght)
						notify.showProgressBar()
					else:
						#FIXME:stop work at endWork
						timerValue = minToSec(self.workLenght)
						Timer(timerValue, timeChecker).start()

						notify.message("Time to work now!")
						notify.setInterval(self.lunchEnd,self.workLenght,0)
						notify.showProgressBar()

				else:
					notify.message("Now it's not time to work!","exit")

		timeChecker() #first timer initialization