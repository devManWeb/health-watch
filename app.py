'''
Based on the set parameters (start and end time of work and of the lunch break),
this app shows how much we have to work, if it is time for a little break
or if we have to start working again. Breaks are from 1 minute, up to 10 minutes.
The rest of the hour is for working.
This script can be run at computer startup or opened during the working day.
TODO:run extensive tests
'''
from timer import HealthTimer
from config import ConfigIO

print("Welcome to the Health Watch!")

try:
	cfg = ConfigIO()
	if cfg.readProp("isconfigured") == "no":
		'''
		if the first configuration was not made,
		we import the module and we do it
		'''
		from first_start import firstConfiguration
		guide = firstConfiguration()
		guide.askUser()
		
	app = HealthTimer()
	app.clock()

except Exception as gen_error:
	print("\nAttention, " + str(gen_error))
	input("Press any key to exit..")
