'''
This modules is used to notify the user in the terminal 
and to show a progress bar
'''
from sys import stdout
from threading import Timer
from common import CommonMethods

comm = CommonMethods()

class UserNotification():

	def message(self,msgText):
		dateStr = str(comm.getActualTime()[0]) + ":" + str(comm.getActualTime()[1])
		print("\n" + dateStr + " - " + msgText)

	def timeBar(self,startTime,endTime):
			
		def progressBar():
			#draws the bar every second, for the whole interval in which it is needed
			#(endTime - startTime) : actualTime = 100 : positionBar
			#function performed every 10 seconds, when we are in the desired interval
			refreshSec = 10
			deltaEndStart = comm.convertToSeconds(endTime) - comm.convertToSeconds(startTime)
			actualTime = comm.convertToSeconds(comm.getActualTime)
			positionBar = actualTime * 100 / deltaEndStart
			if positionBar < 100:
				Timer(refreshSec, drawBar(positionBar,100)).start()

		def drawBar(count, total):
			#draw the progress bar on the terminal
			barLength = 30
			value = int(round(barLength * count / float(total)))
			percentual = round(100.0 * count / float(total), 1)
			barTxt = '#' * value + '-' * (barLength - value)
			stdout.write('[%s] %s%s%s\r' % (barTxt, percentual, '%', ""))
			stdout.flush()
			progressBar()				
				
		progressBar() #first start