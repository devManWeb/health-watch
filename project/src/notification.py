#notify the user and to show a progress bar

import os

from project.src.common import CommonMethods

comm = CommonMethods()

class OnlyForThisFile():
    #specific methods to be used only in this file

	def getDateStr(self):
		#used to make the date for the terminal messages
		def formatValue(intNum):
			'''
			if it is necessary, add an initial 0
			converts the int value to string
			'''
			if intNum <= 9:
				return "0" + str(intNum)
			else:
				return str(intNum)

		hours = formatValue(comm.getActualTime()[0])
		minutes = formatValue(comm.getActualTime()[1])
		dateStr = hours + ":" + minutes

		return dateStr

	def drawBar(self,count):
		#draws the progress bar on the terminal
		barLength = 30
		value = int(round(barLength * count / 100))
		percentual = round(100.0 * count / 100, 1)
		barTxt = '#' * value + '-' * (barLength - value)
		print(self.getDateStr() + ' [%s] %s%s%s\r' % (barTxt, percentual, '%', ""))


private = OnlyForThisFile()


class UserNotification():

	def __self__(self):
		self.startTimeArr = ["0","0"]
		self.endTimeArr = ["0","0"]

	def message(self,msgText,*exitVal):
		'''
		textual message in the terminal,
		the first thing this fx does is clearing the terminal
		if exitVal is "exit", we display "press any key to exit"
		'''
		os.system('cls||clear')
		print("Welcome to the Health Watch")
		print("\n" + msgText)
		if exitVal == "exit":
			input("Press any key to exit...")

	def setStartEnd(self,newStart,newEnd):
		'''
		used for intervals from a specific time to another
		from AA:BB to CC
		'''
		self.startTimeArr = newStart
		self.endTimeArr = newEnd

	def setInterval(self,newStart,minutes,delay):
		'''
		used for a set time interval in minutes
		newStart is is the start time of the work,
		minutes is the duration of the interval in minutes, 
		delay is the delay in minutes
		'''

		self.startTimeArr = comm.addMinutesToHour(newStart,delay)
		self.endTimeArr = comm.addMinutesToHour(self.startTimeArr,minutes)

	def getBarLength(self,actual):
		'''
		returns the percentage value fort the progress bar
		only if it is between 0 and 100
		otherwise, we raise a ValueError
		08/08/2019: actual is added as a param for testing purpouse
		actual is a list of integers (hours and minutes) with the actual time
		'''

		positionBar = 0
		actualSeconds = comm.convertToSeconds(actual)	

		def correctDiffDays(endSeconds,startSeconds):
			'''
			if end and start are in two diffent days
			we add an entire day in seconds
			otherwise, we do nothing
			'''
			if endSeconds < startSeconds:
				return endSeconds + (24 * 60 * 60)
			else:
				return endSeconds

		'''
		if we have an interval between AA:BB and CC:DD
		(endSeconds - startSeconds) : (actualSeconds - startSeconds) = 100 : positionBar
		'''
		startSeconds = comm.convertToSeconds(self.startTimeArr)
		endSeconds = comm.convertToSeconds(self.endTimeArr)

		actualSeconds = correctDiffDays(actualSeconds,startSeconds)
		endSeconds = correctDiffDays(endSeconds,startSeconds)

		deltaSec = endSeconds - startSeconds
		fixActualSec = actualSeconds - startSeconds
		positionBar = fixActualSec * 100 / deltaSec

		if positionBar < 0 or positionBar > 100:
			raise ValueError("Bar value is not between 0 and 100%")
		else:
			return positionBar	
			
	def showProgressBar(self):
		#draws the bar with the current time
		actualTime = comm.getActualTime()
		length = self.getBarLength(actualTime)
		private.drawBar(length)
