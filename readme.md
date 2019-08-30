# Health-watch

This script was created to avoid a sedentary life at the office. 
Based on the user configuration parameters and the current time, it shows when it's time to take a break or to resume working.

The first time you open the script, you can configure:

* Start and end hour
* is it a part-time job?
* lounch break start and end hours
* duration of breaks (1 to 10 minutes)
* enable alert notifications and sounds?

Health watch also shows the number of pauses to do and how many have been done during the day.

Important: the script is still in development, at the moment it does not work correctly. There are several TODOs and FIXMEs.

## Usage

To use this script, in the root folder of the project use:

```
python -m project.src.app
```

To run tests, in the root folder of the project use:

```
python -m project.tests.nameOfTheTest
```

where nameOfTheTest is the desired test.

## Dependencies

[This project use plyer, distributed with the MIT licence](https://pypi.org/project/plyer/). 
In order to use this script, you have to install it:

```
pip3 install plyer
```