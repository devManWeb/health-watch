#notify the user and to show a progress bar

import os
if os.name == "nt":
	from winsound import Beep
from plyer import notification

from project.src.common import CommonMethods
from project.src.config import ConfigIO

comm = CommonMethods()
cfg = ConfigIO()

class OnlyForThisFile():
    #specific methods to be used only in this file

	def __init__(self):
		self.lastMessage = ""

	def showPopup(self,msgToDisplay):
		'''
		If the last message was different
		show a popup (if configured)
		and play a beep (if configured)

		parameters
			msgToDisplay: message to display
		'''
		if self.lastMessage != msgToDisplay:
			self.lastMessage = msgToDisplay

			if cfg.readProp("showPopup") == "yes":
				popupMessage = private.getDateStr() + " - " + msgToDisplay
				notification.notify(
					"Health watch info",
					popupMessage,
					"Health watch"
				)

			if cfg.readProp("playBeep") == "yes":
				self.playBeep()

	def getDateStr(self):
		#used to make the date for the terminal messages
		def formatValue(intNum):
			'''
			if it is necessary, add an initial 0

			arguments
				intNum: integer value to check
			return
				formatted intNum string value
			'''
			if intNum <= 9:
				return "0" + str(intNum)
			else:
				return str(intNum)

		hours = formatValue(comm.getActualTime()[0])
		minutes = formatValue(comm.getActualTime()[1])
		dateStr = hours + ":" + minutes

		return dateStr

	def addMinutesToHour(self,hour,minutesToAdd):
		'''
		this method is used for adding minutesToAdd to hour,
		if we get an hour over 23:59, we fix it

		arguments
			hour: list of integers (hours,minutes)
			minutesToAdd:integer in minutes
		return
			list of hours and minutes
		raise
			ValueError if minutesToAdd > 60
		'''
		if type(hour) != list or type(minutesToAdd) != int:
			raise TypeError("Wrong types given to this function")

		if not 0 <= minutesToAdd <= 60:
			raise ValueError("Adding more than 60 or less than 0 minutes")

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

	def drawBar(self,count):
		'''
		draws the progress bar on the terminal

		arguments
			count: value for the bar
		'''
		barLength = 30
		value = int(round(barLength * count / 100))
		percentual = round(100.0 * count / 100, 1)
		barTxt = '#' * value + '-' * (barLength - value)
		print(self.getDateStr() + ' [%s] %s%s%s\r' % (barTxt, percentual, '%', ""))

	def playBeep(self):
		'''
		generate a beep
		different methods if windows or mac/linux
		'''
		FREQUENCY_VAL = 500
		DURATION_MS = 300
		if os.name == "nt":
			Beep(FREQUENCY_VAL, DURATION_MS)
		else:
			os.system('play -nq -t alsa synth {} sine {}'.format(DURATION_MS, FREQUENCY_VAL))

	def drawPausesChecks(self,total,done,lunchDone):
		'''
		draws the boxes of the pauses with the numbers

		arguments
			total: calculated total pauses
			done: pauses already done
			lunchDone: boolean, is lunch already done?
		'''
		lunchEnabled = False
		addLunch = 0

		if cfg.readProp("isPartTime") == "no":
			lunchEnabled = True
			addLunch = 1
		
		#empty list (total + addLunch) x (total + addLunch)
		rowsData = [
			[None] * (total + addLunch + 1),
			[None] * (total + addLunch + 1)
		]

		if lunchEnabled:  
			#add the indication of the lunch if necessary
			rowsData[0][0] = "-L- "
			if lunchDone:
				rowsData[1][0] = "[X] "
			else:
				rowsData[1][0] = "[ ] "		

		for i in range (addLunch, total + addLunch + 1):

			if lunchEnabled:
				rowsData[0][i] = " -" + str(i) + "- "
			else:
				rowsData[0][i] = " -" + str(i + 1) + "- "
			if i <= done:
				rowsData[1][i] = " [X] "
			else:
				rowsData[1][i] = " [ ] "

		print("\nPauses already done:")

		numberOfItems = total
		if lunchEnabled:
			numberOfItems + 1

		row1 = ""
		row2 = ""
		for l in range(0,total + 1):
			row1 = row1 + str(rowsData[0][l])
			row2 = row2 + str(rowsData[1][l])
		print(row1)
		print(row2)

private = OnlyForThisFile()


class UserNotification():

	def __self__(self):
		self.startTimeArr = ["0","0"]
		self.endTimeArr = ["0","0"]
		self.totalPauses = 0
		self.pausesDone = 0
		self.lunchEnded = False

	def message(self,msgText):
		'''
		clears and display a textual message in the terminal 

		arguments
			msgText: string text to display
		'''
		os.system('cls||clear')
		print("Welcome to the Health Watch")
		print("\n" + msgText)
		private.showPopup(msgText)

	def setStartEnd(self,newStart,newEnd):
		'''
		setterfor intervals from AA:BB to CC:DD
		arguments
			newStart,newEnd: lists of integers
		'''
		self.startTimeArr = newStart
		self.endTimeArr = newEnd

	def setInterval(self,newStart,minutes,delay):
		'''
		setter for interval in minutes

		arguments
			newStart: list of integers, start time of the work,
			minutes: int, duration of the interval in minutes, 
			delay: int, the delay in minutes
		'''
		self.startTimeArr = private.addMinutesToHour(newStart,delay)
		self.endTimeArr = private.addMinutesToHour(self.startTimeArr,minutes)

	def setPausesData(self,arrayData):
		'''
		setter used by endFunction() in timer.py

		arguments
			arrayData: list of integers (total and end pauses)
		'''
		self.totalPauses = arrayData[0]
		self.pausesDone = arrayData[1]

	def setLunchStatus(self,boolean):
		'''simple setter, is the lunch finished?
		
		arguments
			boolean: boolean status for the lunch to ser
		'''
		self.lunchEnded = boolean

	def getBarLength(self,actual):
		'''
		arguments
			actual: list of integers (hours and minutes) with the actual time
		return
			percentage value fort the progress bar only if between 0 and 100
		raise
			ValueError if bar value is not between 0 and 100		
		'''
		positionBar = 0
		actualSeconds = comm.convertToSeconds(actual)	

		def correctDiffDays(endSeconds,startSeconds):
			'''
			if end and start are in two diffent days
			we add an entire day in seconds

			arguments
				endSeconds, startSeconds: int of seconds
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
			
	def showData(self):
		'''
		draws the bar with the current time
		shows the info about the pauses
		'''
		actualTime = comm.getActualTime()
		length = self.getBarLength(actualTime)
		private.drawBar(length)
		private.drawPausesChecks(self.totalPauses,self.pausesDone,self.lunchEnded)