#no bluetooth, keyboard control, ultrasonic connected to arduino
from __future__ import division
import RPi.GPIO as GPIO
import serial
import signal
import argparse
import sys
import logging
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

global flag
global rly1
global rly2
global rly3
global rlynz1
global active
global camerasig
global onind

camerasig=1
onind=0
active=24
rly1=17
rly2=27
rly3=22
rlynz1=6


global line
global lineleft
global lineright
global diff
global k
global max1
global sig
sig=1
flag=5
k=5
line=0
lineleft=18
lineright=18
max1=30



GPIO.setup(rly1, GPIO.OUT)
GPIO.setup(rly2, GPIO.OUT)
GPIO.setup(rly3, GPIO.OUT)
GPIO.setup(rlynz1, GPIO.OUT)
ser = serial.Serial('/dev/ttyACM0',9600)






def rfrecv():
    global active
    global k
    global line
    global lineleft
    global lineright
    global sig
    global s
    global s2
    global s3
    global camerasig
    global onind
    global s4
    sig=1
    
   
    s=1
    s2=1
    s3=1
    s4=1
     
    def master():
        global s
        global active
        if s==1:
            print("Master ON")
            active=2
            s=0
        elif s==0:                       
            print("Master OFF")
            active=3
            s=1
            
        
    def nozflag():
       ''' global k
        global line
        global lineleft
        global lineright
        global sig
        global s4
        if active==2:
            pass
        elif active==3:
            if s4==1:
                GPIO.output(rlynz1, GPIO.LOW)
                sig=0
                s4=0
            elif s4==0:
                GPIO.output(rlynz1, GPIO.HIGH)
                sig=1
                s4=1'''
    while True:
        #from TF_PiCamera_OD import camerasig, onind
        a = input("Enter Command");
        if (a=='1'):
            master();
        elif(a=='2'):
            nozflag();
        else:
            print("Invalid Input")
            

def ultrasonic():
    #global active
    global line
    #global lineleft
    #global lineright    
    while True:
        read_serial=ser.readline()
        line = int(read_serial[1:4])
        #lineleft = int(read_serial[5:8])
        #lineright = int(read_serial[9:12])
        
        
           

def nozcontrol():
    global flag
    global k
    global sig
    while True:
            k=flag
            if k==1:
                GPIO.output(rlynz1,GPIO.HIGH)
                GPIO.output(rly1,GPIO.HIGH)
                GPIO.output(rly2,GPIO.HIGH)
                GPIO.output(rly3,GPIO.LOW)
                sig=1

            if k==2:
                GPIO.output(rlynz1, GPIO.HIGH)
                GPIO.output(rly1,GPIO.LOW)
                GPIO.output(rly2,GPIO.LOW)
                GPIO.output(rly3,GPIO.LOW)
                sig=1
            if k==3:
                GPIO.output(rly1,GPIO.HIGH)
                GPIO.output(rly2,GPIO.HIGH)
                GPIO.output(rly3,GPIO.HIGH)
                GPIO.output(rlynz1, GPIO.LOW)
                sig=0
            if k==4:
                GPIO.output(rly1,GPIO.HIGH)
                GPIO.output(rly2,GPIO.HIGH)
                GPIO.output(rly3,GPIO.HIGH)
                GPIO.output(rlynz1, GPIO.HIGH)
                sig=1
            if k==5:
                GPIO.output(rly1,GPIO.HIGH)
                GPIO.output(rly2,GPIO.HIGH)
                GPIO.output(rly3,GPIO.HIGH)
                GPIO.output(rlynz1, GPIO.HIGH)
                sig=1
            time.sleep(0.5)

def statuscro():
    global active
    global line
    #global lineleft
    #global lineright
    global diff
    global flag
    global camerasig
    global onind
    global max1
    while True:
        #from TF_PiCamera_OD import onind,camerasig
        #from full_semi_camera import camerasig, onind
        if active==2:
            line1=ser.readline().decode().strip()
            line=int(line1)
            #time.sleep(0.5)
            if line<27:
                flag=1
                diff=max1-line
                print ("shaft will move backwards for ",diff," cm")    
                print ("shaft on left ",lineleft," cm")
                print ("shaft on right ",lineright," cm")
            elif line>35:
                 flag=2
                 diff=line-max1
                 print ("shaft will move forward for ",diff," cm")
                 print ("shaft on left ",lineleft," cm")
                 print ("shaft on right ",lineright," cm")
            else:
                if lineleft>15 and lineright>15:
                    if camerasig==1:
                         flag=3
                         print ("spraying allowed")
                         print ("shaft on left ",lineleft," cm")
                         print ("shaft on right ",lineright," cm")
                    elif camerasig==0:
                         flag=4
                         print("No wall to spray")
            
               #elif lineleft<15:
                #   flag=4
                 #  print ("spraying not allowed - check left side")
                 #  print ("shaft on left ",lineleft," cm")
                 #  print ("shaft on right ",lineright," cm")
                   
              # elif lineright<15:
               #    flag=4
                 #  print ("spraying not allowed - check right side")
                 #  print ("shaft on left ",lineleft," cm")
                  # print ("shaft on right ",lineright," cm")
                  #        
            if active==3:
                #time.sleep(0.5)
                flag=5
                k=5
                #print("stopped")

    


