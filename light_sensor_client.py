#!/usr/bin/python

#by Jonathan Williams, October 2020
#Sends request for light sensor data
#saves data to csv file
import socket
import time
import datetime
import struct
#import StringIO
from threading import Thread
import sys

#source of the light sensor readings
UDP_OPT_PORT = 3000 
#listens for light sensor readings
UDP_PORT = 3001

isRunning = True
rcvd_packets = 0
csv_filename = "record-bright.csv"
opt_data = []

#listen for sensor readings from udp-server.c
def udpListenThread():
 # listen on UDP socket port UDP_PORT
  recvSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
  recvSocket.bind(("aaaa::1", UDP_PORT))
  recvSocket.settimeout(0.5)
  global isRunning, rcvd_packets
  #stop listening when 600 packets are received
  while isRunning and rcvd_packets <= 600:
    try:
      data, addr = recvSocket.recvfrom(1024)
      rcvd_packets+=1
      opt_value = int((str(data).split('\'')[1]))
      print("{} :: {}".format(rcvd_packets, opt_value))
      opt_data.append(opt_value)
    except socket.timeout:
      pass
  isRunning = False
   
# start UDP listen thread
t1 = Thread(target=udpListenThread)
t1.start()
print("Listening for incoming packets on UDP port", UDP_PORT)

time.sleep(1)

print("Exit application by pressing (CTRL-C)")

try:
  while True:
    # wait for application to finish (ctrl-c)
    time.sleep(1)
    if not isRunning:
      pass
except KeyboardInterrupt:
  print("Keyboard interrupt received. Exiting.")
  isRunning = False

#write opt_data to csv file
f = open(csv_filename, 'a')
f.write("Brightness\n")
for item in opt_data:
   f.write("{}\n".format(str(item)))
f.close()



