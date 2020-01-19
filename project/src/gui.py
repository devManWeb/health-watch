import tkinter as t
from tkinter.ttk import Progressbar
from tkinter import ttk


class Gui():
 
    def __init__(self):
        self.currentTime = [0,0]
        self.pausesNumber = 0
        self.pausesDone = 0

    def setCurrTime(self,newVal):
        self.currentTime = newVal

    def setPausesNumber(self,newVal):
        self.pausesNumber = newVal

    def setpausesDone(self,newVal):
        self.pausesDone = newVal

    def draw(self):

        window = t.Tk()  
        window.title("Health Watch")

        principale = t.Frame(window)
        principale.pack()

        ######################################

        intestazione = t.Frame(principale)
        intestazione.pack(side = t.TOP,
            fill = t.BOTH,
            padx=10, 
            pady=10,
            expand = t.YES
        )

        lbl = t.Label(
            intestazione,
            text="Welcome to the Health Watch",
            font=("Arial Bold", 10)
        )

        lbl.pack(fill=t.X)

        
        lbl2 = t.Label(
            intestazione,
            text="Time to work now!",
            font=("Arial Bold", 10)
        )
        lbl2.pack(fill=t.X)

        ######################################

        barraProgress = t.Frame(principale)
        barraProgress.pack(
            fill = t.BOTH,
            padx=10, 
            pady=5,
            expand = t.YES
        )

        time = t.Label(
            barraProgress,
            text="11:58",
            font=("Arial Bold", 10)
        )
        time.pack(
            side=t.LEFT,
            padx=5
        )

        style = t.ttk.Style()
        style.theme_use('default')
        style.configure(
            "black.Horizontal.TProgressbar", 
            background='black'
        )
        bar = Progressbar(
            barraProgress, 
            length = 250,
            style='black.Horizontal.TProgressbar'
        )
        bar['value'] = 70
        bar.pack(
            side=t.LEFT,
            padx=5
        )

        lbl3 = t.Label(
            barraProgress,
            text="10.0%",
            font=("Arial Bold", 10)
        )
        lbl3.pack(
            side=t.LEFT,
            padx=5
        )

        ######################################

        steps = t.Frame(principale)
        steps.pack(
            fill = t.BOTH,
            padx=10, 
            pady=5,
            expand = t.YES
        )

        chkL = t.Checkbutton(steps, text='Lounch', state=t.DISABLED, var=True)
        chk1 = t.Checkbutton(steps, text='n°1', state=t.DISABLED, var=True)
        chk2 = t.Checkbutton(steps, text='n°2', state=t.DISABLED, var=True)
        chk3 = t.Checkbutton(steps, text='n°3', state=t.DISABLED, var=True)
        chk4 = t.Checkbutton(steps, text='n°4', state=t.DISABLED, var=True)
        chk5 = t.Checkbutton(steps, text='n°5', state=t.DISABLED, var=True)
        chk6 = t.Checkbutton(steps, text='n°6', state=t.DISABLED, var=True)
        chk7 = t.Checkbutton(steps, text='n°7', state=t.DISABLED, var=True)
        
        chkL.pack(side=t.LEFT)
        chk1.pack(side=t.LEFT)
        chk2.pack(side=t.LEFT)
        chk3.pack(side=t.LEFT)
        chk4.pack(side=t.LEFT)
        chk5.pack(side=t.LEFT)
        chk6.pack(side=t.LEFT)
        chk7.pack(side=t.LEFT)

        ######################################

        punteggio = t.Frame(principale)
        punteggio.pack(
            fill = t.BOTH,
            padx=10, 
            pady=5,
            expand = t.YES
        )
        points = t.Label(
            punteggio,
            text="Health points: 43 - Maximum: 480",
            font=("Arial", 10 , "italic")
        )
        points.pack(fill=t.X)


gui = Gui()
gui.draw()