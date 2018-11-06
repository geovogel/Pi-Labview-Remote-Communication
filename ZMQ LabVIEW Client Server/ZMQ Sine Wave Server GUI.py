#!/usr/bin/python
import zmq
import math

from tkinter.ttk import *
from tkinter import *
from PIL import Image
from PIL import ImageTk

print('ZMQ Version: ', (zmq.pyzmq_version()))
context = zmq.Context()
#  Socket for ZMQ server
socket = context.socket(zmq.REQ)
socket.bind("tcp://*:5556")

# Initialize Variables 
n=0             # loop counter and base for frequency steps
xAmp = 1
yAmp = 1
yStep = 0
zStep = 0

class App:
    def __init__(self, master):
        # Initialize Python Variables
        btn_led_color='grey'
        deg = u'\N{DEGREE SIGN}'

        def GenSineWave(yAmp, zAmp, yStep, zStep):
            y = (math.sin(math.radians(yStep))) * yAmp
            z = (math.sin(math.radians(zStep))) * zAmp
            y='{:4.3f}'.format(y)
            z='{:4.3f}'.format(z)
            return y, z

        def updateDisplay():
            global n
            global yStep
            global zStep
            
            # Read GUI button state and send to Labview LED
            btn_state = btn_var.get()

            yAmp = yAmp_var.get()
            zAmp = zAmp_var.get()
            yFreq= yFreq_var.get()
            zFreq= zFreq_var.get()
                       
            y = GenSineWave(yAmp, zAmp, yStep, zStep)[0]
            z = GenSineWave(yAmp, zAmp, yStep, zStep)[1]
             
            n = n +1
            if n > 360:
                n=0
            yStep = yStep +yFreq
            zStep = zStep +zFreq

            # Send and receive  data to LabVIEW through ZeroMQ messaging (TCP) 
            socket.send_string(str(n) +"/" + y + "/" + z + "/" + btn_state)     
            message = socket.recv()

            # Set the LED color according to the LabVIEW button
            LVbtnState = message
            LVbtnState = LVbtnState.decode("utf-8") 
            if LVbtnState == 'T':
                canvas1.itemconfig(btn_led, fill="lime")
            elif LVbtnState == 'F':
                canvas1.itemconfig(btn_led, fill="darkgreen")

            # End of update loop function, update display and repeat after xxx ms
            root.update_idletasks()
            root.after(0,updateDisplay)
#_________________________________________________________________________________
#______________________________TKINTER GUI________________________________________

        #check_var = StringVar()
        frame = ttk.Frame(master,style="My.TFrame",relief= FLAT, borderwidth=3, padding=4)
        frame.pack()       

        # Tkinter Styles
        s= ttk.Style()
        s.configure('.', font=('Arial', '11','bold'))
        s.configure("My.TLabel"    ,background='#c3dbee', font=('Arial', '11','bold'))
        s.configure("sm.TLabel"    ,background='#c3dbee', font=('Arial', '9'))
        s.configure("My.TSeparator", background='#004bff', width=4)
        s.configure("My.TFrame"    ,borderwidth= 2,background='#c3dbee',padx=5, pady=5)

        # Borders
        s1=ttk.Separator(frame, orient= HORIZONTAL, style="My.TSeparator")      .grid(row=0, column=0, columnspan=8,sticky=E+W, padx=0)
        s2=ttk.Separator(frame, orient= VERTICAL,   style="My.TSeparator")      .grid(row=0, column=0, rowspan=10,  sticky=N+S, padx=0)
        s3=ttk.Separator(frame, orient= VERTICAL,   style="My.TSeparator")      .grid(row=0, column=8, rowspan=10,  sticky=N+S, padx=0)
        s4=ttk.Separator(frame, orient= VERTICAL,   style="My.TSeparator")      .grid(row=1, column=4, rowspan=5,   sticky=N+S, padx=0)
        s5=ttk.Separator(frame, orient= HORIZONTAL, style="My.TSeparator")      .grid(row=5, column=1, columnspan=8,sticky=E+W, padx=0)
        s6=ttk.Separator(frame, orient= HORIZONTAL, style="My.TSeparator")      .grid(row=10,column=1, columnspan=8,sticky=E+W, padx=0)
                
        label_6 = ttk.Label(frame, text='Y waveform',style="My.TLabel") .grid(row=1, column=1, sticky=W, padx=3, pady=3, columnspan=2)
        label_7 = ttk.Label(frame, text='Z waveform',style="My.TLabel") .grid(row=1, column=5, sticky=W, padx=3, pady=3, columnspan=2)
        
       # Y Amp Control Widget
        label_2 = ttk.Label(frame, text='Amp',style="sm.TLabel")                .grid(row=2, column=1, sticky=E, padx=0, pady=3)
        yAmp_var = IntVar()
        Scale(frame, from_=10, to=1, orient=VERTICAL,troughcolor="black",\
        variable= yAmp_var,background='#c3dbee',highlightthickness=0)           .grid(row=2, column=2, sticky=W, padx=0, pady=3)

        # Y Freq Control Widget
        label_3 = ttk.Label(frame, text='Freq',style="sm.TLabel")               .grid(row=4, column=3, sticky=W, padx=2, pady=1,columnspan=2)
        yFreq_var = IntVar()
        Scale(frame, from_=1, to=10, orient=HORIZONTAL,troughcolor="black", \
        variable= yFreq_var,background='#c3dbee',highlightthickness=0)          .grid(row=3, column=2, sticky=E, padx=8, pady=1,columnspan=2)

        # Image1 Display
        image1= "YelSine.jpg"                         
        canvas3 = Canvas (frame, height =75, width=85,\
        background='#c3dbee',highlightthickness=0)
        canvas3                                                                 .grid(row =2, column=3, sticky=W, pady=6)
        image1= Image.open(image1).resize((75,75), Image.ANTIALIAS)
        canvas3.image = ImageTk.PhotoImage(image1)
        item1= canvas3.create_image(0,0, image=canvas3.image, anchor='nw')

        # Z Amp Control Widget
        label_4 = ttk.Label(frame, text='Amp',style="sm.TLabel")                .grid(row=2, column=5, sticky=E, padx=0, pady=3)
        zAmp_var = IntVar()
        Scale(frame, from_=10, to=1, orient=VERTICAL,troughcolor="black", \
        variable= zAmp_var,background='#c3dbee',highlightthickness=0)           .grid(row=2, column=6, sticky=W, padx=0, pady=3)

        # Z Freq Control Widget
        label_5 = ttk.Label(frame, text='Freq',style="sm.TLabel")               .grid(row=4, column=7, sticky=W, padx=2, pady=1)
        zFreq_var = IntVar()
        Scale(frame, from_=1, to=10, orient=HORIZONTAL,troughcolor="black", \
        variable= zFreq_var,background='#c3dbee',highlightthickness=0)          .grid(row=3, column=6, sticky=E, padx=8, pady=1, columnspan=2)

        # Image2 Display
        image2= "RedSine.jpg"                          
        canvas4 = Canvas (frame, height =75, width=85,\
        background='#c3dbee',highlightthickness=0)
        canvas4                                                                 .grid(row =2, column=7, sticky=W, pady=6)
        image2= Image.open(image2).resize((75,75), Image.ANTIALIAS)
        canvas4.image = ImageTk.PhotoImage(image2)
        item2= canvas4.create_image(0,0, image=canvas4.image, anchor='nw')
     
        # LED Indicator Widgt
        label_6= ttk.Label(frame, text='LV Button',style="My.TLabel")           .grid(row=7, column=1, sticky=W, padx=3, pady=6, columnspan=2)
        canvas1 = Canvas(frame, height =28, width=28,background='#c3dbee', \
        highlightthickness=0)
        btn_led=canvas1.create_oval(5,5,25,25, fill= btn_led_color,)
        canvas1                                                                 .grid(row=7, column=3, sticky=E+W, padx=25, pady=6)

        #Button Control Widget
        label_1 = ttk.Label(frame, text='LV LED',style="My.TLabel")             .grid(row=8, column=1, sticky=W, padx=3, pady=6, columnspan=2)        
        btn_var= StringVar()
        Button=Checkbutton(frame,text='LED Ctrl',indicatoron=0,variable=btn_var,\
        onvalue='T',offvalue='F',padx=3,\
        pady=4,borderwidth=4,relief=RAISED,selectcolor='green')                 .grid(row=8, column=3, sticky=W, padx=10, pady=6)

#---Main Execution Code---
        updateDisplay()  # After building the GUI, call the main function and repeat it.

root = Tk()
root.wm_title('Sine Wave GUI for ZMQ Labview')
app = App(root)
root.mainloop()
