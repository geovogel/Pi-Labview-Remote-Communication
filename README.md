# Pi-Labview-Remote-Communication
## Overview
The purpose of this project was to explore the use of ZMQ as a cross platform data transfer tool. The project is devided into two parts. The first part establishes the basic methodology to create an internet communication channel between a Raspberry Pi with a LINUX operation system and a desktop PC running Windows. A modified version of the Python "Hello World" program from the ZMQ documentation is adapted and used to work out the bugs. Notes on getting things to work can be found [here](DOC/ZeroMQ_Pi-PC_Client-Server_Python.pdf).
## Sine Wave GUI
Building on the basics, a data tranfer scheme was built and tested. For this application roles are reversed for the Pi and PC with the Pi serving waveform data to client PC. Additionlly biderectional boolean data is exchanged to control LED indicators on both ends. All of the data is packaged as a string using simplr delimeters that caan be used to decipher the data on the receiving end. As with the basic testing a port needed to be opened on the router for the Pi server. The Pi GUI is based on Tkinter and also requires the PIL image processing library. The labVIEW client on the PC is based on a [ZMQ VI library](http://labview-zmq.sourceforge.net) that has all of the same functionality as the Python library on the Pi. The following screenshots show the controls and indicator layout and the demo shows it all in action.  

![Screenshot](IMG/ScreenShot.png)*Pi/Python and LabVIEW/PC GUI Screenshots*
      
![Demo](IMG/ZMQ_Pi-PC_Demo.gif)
