'''
This is the main timer. Based on the current hour and minute, 
we determine if it's time to take a break, to work or it is lunch time.
'''	
from threading import Timer
from config import ConfigIO
from common import CommonMethods
from notification import UserNotification

cfg = ConfigIO()
comm = CommonMethods()
notify = UserNotification()

class HealthTimer():

	def __init__(self):
		self.workStart = cfg.readTime("workStart")
		self.workEnd = cfg.readTime("workEnd")
		self.lunchStart = cfg.readTime("lunchStart")
		self.lunchEnd = cfg.readTime("lunchEnd")

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

		def formatMinute(minute):
			#if we exceed 59 minutes, we start from 0
			if minute > 59:
				minute = minute - 60
			return minute

		startPauseMinute = formatMinute(self.workStart[1] + 55)
		endpauseMinute = formatMinute(startPauseMinute + 5)

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

			start = self.workStart
			end =  self.workEnd
			lunchStart = self.lunchStart
			lunchEnd = self.lunchEnd

			def minToSec(mins):
				return mins * 60

			timerValue = 0

			if self.compareTime(start,lunchStart) or self.compareTime(lunchEnd,end):
				if self.isInPause():
					timerValue = minToSec(5)
					Timer(timerValue, timeChecker).start()
					notify.message("Time to take a break!")
					notify.setInterval(start,5)
					notify.timeBar()
				else:
					timerValue = minToSec(55)
					Timer(timerValue, timeChecker).start()
					notify.message("Time to work now!")
					notify.setInterval(start,55)
					notify.timeBar()

			elif self.compareTime(lunchStart,lunchEnd):
				timerValue = self.timeTo(lunchEnd)
				Timer(timerValue, timeChecker).start()
				notify.message("Time to go eating!")
				notify.setStartEnd(lunchStart,lunchEnd)
				notify.timeBar()

			else:
				notify.message("Now it's not time to work!")
				input("Press any key to exit...")

		timeChecker() #first timer initialization