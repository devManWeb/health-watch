'''
Based on the set parameters (start and end time of work and of the lunch break),
this app shows how much we have to work, if it is time for a little break
or if we have to start working again. Breaks are from 1 minute, up to 10 minutes.
The rest of the hour is for working.
This script can be run at computer startup or opened during the working day.
'''

from project.src.timer import clockManager
from project.src.config import ConfigIO	

if __name__ == '__main__':

	cfg = ConfigIO()
	if cfg.readProp("isconfigured") == "no":
		'''
		if the first configuration was not made,
		we import the module and we do it
		'''
		from project.src.first_start import FirstConfiguration
		guide = FirstConfiguration()
		guide.askUser()
		
	clockManager()