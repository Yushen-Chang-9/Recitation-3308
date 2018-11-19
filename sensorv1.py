#!/usr/bin/python


import sqlite3
import os
import time


#csci3308 milestone 4 script
#This script is used on the raspberry pi 3 B+ to get temperature data and store it
#in a sql database that is also on the raspberry pi 3 B+.
#The name of the sensor device file: #28-00000a3cdc2c
#Device File Path:  /sys/bus/w1/devices/28-00000a3cdc2c/w1_slave


#Global Variables
#sampling frequency for sensor:
sample = (5*60)-1
#database object to store at sql path: /var/wwww/templog.db
myDatabase = '/var/www/templog.db'
#devive file
#device_file = '28-00000a3cdc2c'
#Function to measure temperature from device file for DS18B20 sensor

def getData(devicefile):

    try:

        data_object = open(devicefile, 'r')
        lines = myDatabase.readlines()
        data_object.close()

    except:

        return None


    #Display status
    status = lines[0][-4:-1]

    #if sensor data reading is succesful
    if status == "Device is reading..." :

        print status
        store_data = line[1][-6:-1]


         data_value = float(store_data)/1000
        print data_value
        return data_value
    #else the device encountered an issue
    else:

        print "Error: Device has encountered an issue "
        return None

#storing the sensor data in the sql databse or any database
def storage(temp):

    #connect class is used to connect to sql database also used for socket programming
    db_connect = sqlite3.connect(myDatabase)
    #cursor class allows Python to execute PostgreSQL command in database session
    db_cursor = db_connect.cursor()
    db_cursor.execute("INSERT INTO temps values(datetime('now'), (?))", (temp,))

    #commit changes to database SQL
    db_connect.commit()
    #terminate connection to database SQL
    db_connect.close()

#display database
def display():

    db_connect = sqlite3.connect(myDatabase)
    db_cursor = db_connect.cursor()

    #iterate through contents of db
    for row in db_cursor.execute("SELECT * FROM temps"):
        print str(row[0]) + "  " + str(row[1])
        db_connect.close()



#main
def main():

    #enable kernel modules
    os.system('sudo modprobe w1-gpio')
    os.system('sudo modprobe w1-therm')

    #search for sensor device path (cd /sys/bus/w1/devices/28*) to device address
    devicelist = glob.glob('/sys/bus/w1/devices/28*')
    if devicelist == '':
        return None
    else:
        #append /w1_slave to device file path
        w1_devicefile = devicelist[0] + 'w1_slave'

    #while true
    #call getData function from devicefile
    temperature = getData(w1_devicefile)
    if temperature != None:
        print "temperature = "+str(temperature)

    #store meausured temperature into sql database
    display()
    #time.sleep(meausre)
