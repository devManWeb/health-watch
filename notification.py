'''
This modules is used to notify the user in the terminal 
and to show a progress bar
'''
from sys import stdout
from threading import Timer
from common import CommonMethods

comm = CommonMethods()

class UserNotification():

	def __self__(self):
		self.startTimeArr = ["0","0"]
		self.endTimeArr = ["0","0"]
		self.intervalAmount = 0
		self.isInterval = False

	def message(self,msgText):

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
		print("\n" + dateStr + " - " + msgText)

	def setStartEnd(self,newStart,newEnd):
		self.startTimeArr = newStart
		self.endTimeArr = newEnd
		self.intervalAmount = 0
		self.isInterval = False

	def setInterval(self,newStart,minutes):
		self.startTimeArr = newStart
		self.endTimeArr = ["0","0"]
		self.intervalAmount = minutes * 60
		self.isInterval = True

	def timeBar(self):
	
		def progressBar():
			'''
			draws the bar every second, for the whole interval in which it is needed
			function performed every second, when we are in the desired interval
			'''
			refreshSec = 1
			positionBar = 0
			actualTime = comm.convertToSeconds(comm.getActualTime())

			if self.isInterval:
				'''
				if we only have a fixed duration in seconds
				we also consider when we open the app and the pause is already started
				from the start inserted in the cfg file and the actual time,
				we calculate the lenght of the bar
				eventSeconds : actualTime = 100 : positionBar
				'''
				actualHour = comm.getActualTime()[0]
				pauseMinute = self.startTimeArr[1]
				#we calculate the hour and the minute start of the event (AA:BB)
				eventStart = [actualHour,pauseMinute]
				eventSeconds = comm.convertToSeconds(eventStart)
				positionBar = actualTime * 100 / eventSeconds				
			else:
				'''
				if we have an interval between AA:BB and CC:DD
				(endTime - startTime) : actualTime = 100 : positionBar
				'''
				endIntSec = comm.convertToSeconds(self.startTimeArr)
				startIntSec = comm.convertToSeconds(self.endTimeArr)
				deltaSec = endIntSec - startIntSec
				positionBar = actualTime * 100 / deltaSec

			if positionBar < 100:
				Timer(refreshSec, drawBar(positionBar)).start()


		def drawBar(count):
			print(count)
		'''
		def drawBar(count):
			#draw the progress bar on the terminal
			barLength = 30
			value = int(round(barLength * count / 100))
			percentual = round(100.0 * count / 100, 1)
			barTxt = '#' * value + '-' * (barLength - value)
			stdout.write('[%s] %s%s%s\r' % (barTxt, percentual, '%', ""))
			stdout.flush()
			progressBar()		
		'''		
				
		progressBar() #first start