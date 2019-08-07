'''
This modules is used to notify the user in the terminal 
and to show a progress bar
'''
from sys import stdout
from time import sleep

from project.src.common import CommonMethods

comm = CommonMethods()

class UserNotification():

	def __self__(self):
		self.startTimeArr = ["0","0"]
		self.endTimeArr = ["0","0"]
		self.intervalAmount = 0
		self.intervalDelay = 0
		self.isInterval = False

	def getDateStr(self):
		
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

	def message(self,msgText,*exitVal):
		'''
		textual message in the terminal
		if exit is "exit", we display "press any key to exit"
		'''
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
		self.intervalAmount = 0
		self.intervalDelay = 0
		self.isInterval = False

	def setInterval(self,newStart,minutes,delay):
		'''
		used for a set time interval in minutes
		newStart is is the start time
		minutes is the duration of the interval in minutes, 
		delay is the delay in minutes
		'''
		self.startTimeArr = newStart
		self.endTimeArr = ["0","0"]
		self.intervalAmount = minutes * 60
		self.intervalDelay = delay * 60
		self.isInterval = True

	def drawBar(self,count):
		#draw the progress bar on the terminal
		barLength = 30
		value = int(round(barLength * count / 100))
		percentual = round(100.0 * count / 100, 1)
		barTxt = '#' * value + '-' * (barLength - value)
		stdout.write(self.getDateStr() + ' [%s] %s%s%s\r' % (barTxt, percentual, '%', ""))
		stdout.flush()	

	def getBarLength(self):
		#calculates the percentage length to be shown in the progress bar
		positionBar = 0
		actualTime = comm.convertToSeconds(comm.getActualTime())

		if self.isInterval:
			'''
			if we have the start time AA:BB, the duration of the interval and the delay
			we also consider when we open the app and if the pause is already started
			we add the delay (to know what is the start hour, go to timer.py)
			positionBar = actualSeconds * 100 / endSeconds
			'''
			
			hoursFromDelay = self.intervalDelay // 3600
			minutesFromDelay = self.intervalDelay - hoursFromDelay

			realHourStart = comm.getActualTime()[0] + hoursFromDelay
			tempMinutesStart = self.startTimeArr[1] + minutesFromDelay
			realMinutesStart = comm.formatMinute(tempMinutesStart)

			if tempMinutesStart != realMinutesStart:
				#when the minutes are over 59, we fix the hours
				realHourStart = realHourStart + 1

			realStart = [realHourStart,realMinutesStart]
			startSeconds = comm.convertToSeconds(realStart)
			actualSeconds = comm.convertToSeconds(comm.getActualTime())		
			actualFixed = actualSeconds - startSeconds

			positionBar = actualFixed * 100 / self.intervalAmount

		else:
			'''
			if we have an interval between AA:BB and CC:DD
			(endTime - startTime) : actualTime = 100 : positionBar
			'''
			endIntSec = comm.convertToSeconds(self.startTimeArr)
			startIntSec = comm.convertToSeconds(self.endTimeArr)
			if endIntSec >= startIntSec:
				'''
				if endIntSec and startIntSec are in two diffent days
				we add 24 * 3600 seconds to the end
				'''
				endIntSec = endIntSec + (24 * 3600)
			deltaSec = endIntSec - startIntSec	
			positionBar = actualTime * 100 / deltaSec

		return positionBar
			
	def showProgressBar(self):
		'''
		draws the bar every second, for the whole interval in which it is needed
		function performed every second, when we are in the desired interval
		'''
		length = self.getBarLength()
		self.drawBar(length)
		if length < 100:
			sleep(60)
			self.showProgressBar()
