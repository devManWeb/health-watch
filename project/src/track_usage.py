import pynput.mouse, pynput.keyboard
import threading
import time

class threadMouse(threading.Thread): #ereditariety
	# Collect events until released
	def __init__(self):
		threading.Thread.__init__(self)	
		self.callback = 0

	def setCallBack(self,callBack):
		self.callBack = callBack
	
	def run(self):
		with pynput.mouse.Listener(
			on_move=self.callBack,
			on_click=self.callBack,
			on_scroll=self.callBack
		) as listener:
			listener.join()


class threadKeyboard(threading.Thread): #ereditariety
	# Collect events until released
	def __init__(self):
		threading.Thread.__init__(self)	
		self.callback = 0

	def setCallBack(self,callBack):
		self.callBack = callBack

	def run(self):
		with pynput.keyboard.Listener(
			self.callBack
		) as listener:
			listener.join()

class TrackUsage():

	def __init__(self,):
		self.callBack = 0

	def setCallBack(self,callBack):
		self.callBack = callBack


	def run(self):
		a = threadMouse()
		a.setCallBack(self.callBack)
		a.start()

		b = threadKeyboard()
		b.setCallBack(self.callBack)
		b.start()