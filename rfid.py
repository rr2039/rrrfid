#!/usr/bin/env python

#Basic imports
from ctypes import *
import os
import signal
import subprocess
import sys
import time
import datetime
import urllib2
import urllib
import signal
import math

#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, OutputChangeEventArgs, TagEventArgs
from Phidgets.Devices.RFID import RFID, RFIDTagProtocol
from Phidgets.Phidget import PhidgetLogLevel

#Home path
homepath ='/home/pi/Desktop/Sign-In Script/'
audlib = homepath + 'aud/'
logpath = homepath + 'log/'


hiddenpath = '/var/www/html/'
display= hiddenpath + 'message.txt'
tags= hiddenpath + 'tag.txt'
commands= hiddenpath + 'commands.txt'


global tagsList
global commandsList

tagsList=list()
commandsList=list()

with open(tags) as f:
	tagsList = f.read().splitlines()

with open(commands) as f:
	commandsList = f.read().splitlines()

#Create an RFID object
try:
	rfid = RFID()
except RuntimeError as e:
	print("Runtime Exception: %s" % e.details)
    	reboot()
                     
def login(name)
	#TODO login by name
    	time_card = logpath + name + '.log'
	timeCardExists = False
	try:
        	timeCardExists = os.path.isfile(time_card)             
	except ValueError:
        	print("Error")

def logout(name)
    	#TODO logout by name
	now = datetime.datetime.now()
        time_card = logpath + name + '.log'
        timeCardExists = False
	
	try:
        	timeCardExists = os.path.isfile(time_card)
        except ValueError:
		print("Error")
	
        time_line= times[len(times)-1]
        time_msg = "{}".format( now.strftime('%m/%d/%y,%H:%M:%S,'))
        date_time = time_msg.split(",")
        timeIn = time_ary[1]
        timeOut = date_time[1]
        delta = getDelta(timeIn, timeOut)
        print("Time logged: " + delta)
        print(time_msg)
        printToFile(time_card, time_msg + delta, False)
        printToFile(display, "Goodbye, " + name + " (" + delta + ")", True)

def getName(tag)
    #TODO get name of student by tag
    name = "None"
    for idx in range(0,len(tagsList)):
	    assignee=tagsList[idx].split('=')
	    if assignee[0]==tag:
	        name=assignee[1]
		break
	    else:
		name='Guest_' + tag
    return name

def reboot():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
    

def playSound(snd_file):
    snd_file = audlib + snd_file + '.mp3'
    snd = subprocess.Popen(['omxplayer', '-o', 'hdmi', snd_file])
    time.sleep(1)
    snd.terminate()
    
def getDelta(in_time, out_time):
    t1 = in_time.split(":")
    t2 = out_time.split(":")
    h1 = int(t1[0])
    h2 = int(t2[0])
    m1 = int(t1[1])
    m2 = int(t2[1])
    s1 = int(t1[2])
    s2 = int(t2[2])

    total = (3600*h2 + 60*m2 + s2) - (3600*h1 + 60*m1 + s1)
    h = int(math.floor(total/3600))
    total= total-(h*3600)
    m = int(math.floor(total/60))
    total = total - (m*60)
    s = int(total)
    
    if (h)<10:
        h = "0" + str(h)
    else:
        h = str(h)
    if (m)<10:
        m = "0" + str(m)
    else:
        m = str(m)
    if (s)<10:
        s = "0" + str(s)
    else:
        s = str(s)
    
    return(h+":"+m+":"+s)

def printToLog(name, time):
    time_msg = name + " , {};".format(time.strftime('%m/%d/%y %H:%M:%S'))
    printToFile(logpath + 'log.log', time_msg, False)


def printToFile(filename, text, overwrite):
    try:
        if overwrite:
            file = open(filename, "w+")
            file.seek(0)
	    file.truncate()
	    file.write(text)
	    file.close
        else:
            file = open(filename, "a")
            file.write(text)
	    file.close
    except ValueError:
        print("Error writing to file")
	

def rfidAttached(e):
    time.sleep(5)
    playSound('charge')
         
def rfidDetached(e):
    playSound('error')
    time.sleep(3)
    reboot()
         
def rfidError(e):
    try:
        source = e.device
        print("RFID %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
         
def rfidOutputChanged(e):
    print("")
    
def rfidTagGained(e):
	rfid.setLEDOn(1)
    	t = e.tag
    	command_text = runCommand(t)
    	if command_text == "None":
		name = getName(t)
	now = datetime.datetime.now()
    	printToLog(name, now)
	if timeCardExists:              
        	if time_line.count(":") >= 4:
			login(name)
		else:
	        	logout(name)
       	else:
            		login(name)
        
		playSound('ding')
	
	
    
def runCommand(tag):
    flag = "None"
    for idx in range(0,len(commandsList)):
        command = commandsList[idx].split('=')
	if command[0]==tag:
	    flag = command[1]
	    break
    
    #TODO run command if not none
    
    return flag

def rfidTagLost(e):
    rfid.setLEDOn(0)
    time.sleep(1)

def openDevice():
    try:
        rfid.openPhidget()
    except PhidgetException as e:
    	print("Phidget Exception %i: %s" % (e.code, e.details))
    	reboot()
            
#Main Program Code
try:
    #rfid.enableLogging(PhidgetLogLevel.PHIDGET_LOG_VERBOSE, "phidgetlog.log")
    rfid.setOnAttachHandler(rfidAttached)
    rfid.setOnDetachHandler(rfidDetached)
    rfid.setOnErrorhandler(rfidError)
    rfid.setOnTagHandler(rfidTagGained)
    rfid.setOnTagLostHandler(rfidTagLost)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    reboot()
         

openDevice()
try:
    rfid.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        rfid.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        reboot()

rfid.setAntennaOn(True)
chr = sys.stdin.read(1)
                 
try:
    lastTag = rfid.getLastTag()
    print("Last Tag: %s" % (lastTag))
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    printToFile(display, "", True)     
print("Closing...")
         
try:
    rfid.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    reboot()
         
print("Done.")
exit(0)
