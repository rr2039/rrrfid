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

 
global tagsList
tagsList=list()
with open(tags) as f:
    tagsList = f.read().splitlines()

#Create an RFID object
try:
    rfid = RFID()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)
                     
def login(name)
    #TODO login by name
    t = e.tag
    if t == "Guest1":
        reboot()
    print(t)

    try:
        for idx in range(0,len(tagsList)):
	    assignee=tagsList[idx].split('=')
	    if assignee[0]==e.tag:
	        name=assignee[1]
		break
	    else:
		name='Guest_' + t
        now = datetime.datetime.now()
        time_card = logpath + name + '.log'
        timeCardExists = os.path.isfile(time_card)
        overwriteCard = not timeCardExists

        printToLog(name, now)

        if timeCardExists:
            in_count=0
            out_count=0
            times= list()
            with open(time_card) as ts:
                line = ts.read()
                in_count+=line.count("In")
                out_count+=line.count("Out")
                
            with open(time_card) as ts:
                times = ts.read().splitlines()
            
            time_line = times[len(times)-1]
            time_ary = time_line.split(",")

            print(times[len(times)-1])
            print(times[len(times)-1].count(":"))

            while(len(time_ary) < 5):
                time_ary.append("")

            for idx in range(0, 4):
                print(time_ary[idx])
            
            if times[len(times)-1].count(":") >= 4:
                time_msg = "\n{}".format( now.strftime('%m/%d/%y,%H:%M:%S,'))
                printToFile(time_card, time_msg, False)
                printToFile("/var/www/html/message.txt", "Welcome, " + name, True)
            else:
                time_line= times[len(times)-1]
                time_msg = "{}".format( now.strftime('%m/%d/%y,%H:%M:%S,'))
                date_time = time_msg.split(",")
                timeIn = time_ary[1]
                timeOut = date_time[1]
                delta = getDelta(timeIn, timeOut)
                print("Time logged: " + delta)
                print(time_msg)
                printToFile(time_card, time_msg + delta, False)
                printToFile("/var/www/html/message.txt", "Goodbye, " + name + " (" + delta + ")", True)
        else:
            time_msg = "{}".format( now.strftime('%m/%d/%y,%H:%M:%S,'))
            printToFile(time_card, time_msg, True)
            printToFile("/var/www/html/message.txt", "Welcome, " + name, True)
        playSound('ding')
    except ValueError:
        print("Error unknown tag %s" % (t))

def logout(name)
    #TODO logout by name
    t = e.tag
    if t == "Guest1":
        reboot()
    print(t)

    try:
        for idx in range(0,len(tagsList)):
	    assignee=tagsList[idx].split('=')
	    if assignee[0]==e.tag:
	        name=assignee[1]
		break
	    else:
		name='Guest_' + t
        now = datetime.datetime.now()
        time_card = logpath + name + '.log'
        timeCardExists = os.path.isfile(time_card)
        overwriteCard = not timeCardExists

        printToLog(name, now)

        if timeCardExists:
            in_count=0
            out_count=0
            times= list()
            with open(time_card) as ts:
                line = ts.read()
                in_count+=line.count("In")
                out_count+=line.count("Out")
                
            with open(time_card) as ts:
                times = ts.read().splitlines()
            
            time_line = times[len(times)-1]
            time_ary = time_line.split(",")

            print(times[len(times)-1])
            print(times[len(times)-1].count(":"))

            while(len(time_ary) < 5):
                time_ary.append("")

            for idx in range(0, 4):
                print(time_ary[idx])
            
            if times[len(times)-1].count(":") >= 4:
                time_msg = "\n{}".format( now.strftime('%m/%d/%y,%H:%M:%S,'))
                printToFile(time_card, time_msg, False)
                printToFile("/var/www/html/message.txt", "Welcome, " + name, True)
            else:
                time_line= times[len(times)-1]
                time_msg = "{}".format( now.strftime('%m/%d/%y,%H:%M:%S,'))
                date_time = time_msg.split(",")
                timeIn = time_ary[1]
                timeOut = date_time[1]
                delta = getDelta(timeIn, timeOut)
                print("Time logged: " + delta)
                print(time_msg)
                printToFile(time_card, time_msg + delta, False)
                printToFile("/var/www/html/message.txt", "Goodbye, " + name + " (" + delta + ")", True)
        else:
            time_msg = "{}".format( now.strftime('%m/%d/%y,%H:%M:%S,'))
            printToFile(time_card, time_msg, True)
            printToFile("/var/www/html/message.txt", "Welcome, " + name, True)
        playSound('ding')
    except ValueError:
        print("Error unknown tag %s" % (t))

def getName(tag)
    #TODO get name of student by tag


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

    print(in_time)
    print(out_time)
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
    printToFile('/home/pi/Desktop/Sign-In Script/log/log.log', time_msg, False)


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
        print("Error unknown tag %s" % (e.tag))

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
    if t == "Guest1":
        reboot()
    print(t)

def tagIsCommand(tag):
    flag = False
   for idx in range(0,len(commandsList)):
	    command = commandsList[idx].split('=')
	    if command[0]==tag:
	        flag = True
	        break
	now = datetime.datetime.now()
        time_card = logpath + name + '.log'
        timeCardExists = os.path.isfile(time_card)
        overwriteCard = not timeCardExists


def rfidTagLost(e):
    rfid.setLEDOn(0)
    time.sleep(1)

def openDevice():
    try:
        rfid.openPhidget()
    except PhidgetException as e:
    	print("Phidget Exception %i: %s" % (e.code, e.details))
    	print("Exiting....")
    	exit(1)
            
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
    print("Exiting....")
    exit(1)
         

openDevice()
try:
    rfid.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        rfid.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

rfid.setAntennaOn(True)
chr = sys.stdin.read(1)
                 
try:
    lastTag = rfid.getLastTag()
    print("Last Tag: %s" % (lastTag))
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    printToFile("/var/www/html/message.txt", "", True)     
print("Closing...")
         
try:
    rfid.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)
         
print("Done.")
exit(0)
