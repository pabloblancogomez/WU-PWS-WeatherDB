#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function

import datetime
import os
import sys
import time
import requests
import MySQLdb
import json
import mysql.connector
import ast
import commands
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails
def read_template(filename):
    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)
names, emails = get_contacts('mycontacts.txt')  # read contacts
message_template = read_template('message.txt')

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

print( "Connecting to mysql database")

#connect to the database. Enter your host, username and password
cnx = mysql.connector.connect(user='root', password='papelote', host='localhost', database='weatherdb')

cursor = cnx.cursor()

# ============================================================================
# Constants
# ============================================================================
# specifies how often to measure values from the Sense HAT (in minutes)
MEASUREMENT_INTERVAL = 5  # minutes
# Set to False when testing the code and/or hardware
# Set to True to enable download of weather data to Weather Underground
WEATHER_DOWNLOAD = True
# some string constants
SINGLE_HASH = "#"
HASHES = "########################################"
SLASH_N = "\n"


def main():
    aNivel = 'VERDE'
    HUMEDADant = 99
    NIVELnuevo = "VERDE"    
    # initialize the lastMinute variable to the current time to start
    last_minute = datetime.datetime.now().minute
    # on startup, just use the previous minute as lastMinute
    last_minute -= 1
    if last_minute == 0:
        last_minute = 59

    # infinite loop to continuously check weather values
    while 1:        
        current_second = datetime.datetime.now().second
        # are we at the top of the minute or at a 5 second interval?
        if (current_second == 0) or ((current_second % 5) == 0):
            # get the current minute
            current_minute = datetime.datetime.now().minute
            # is it the same minute as the last time we checked?
            if current_minute != last_minute:
                # reset last_minute to the current_minute
                last_minute = current_minute
                # is minute zero, or divisible by 10?
                # we're only going to take measurements every MEASUREMENT_INTERVAL minutes
                if (current_minute == 0) or ((current_minute % MEASUREMENT_INTERVAL) == 0):
                    # get the reading timestamp
                    now = datetime.datetime.now()
                    print("\n%d minute mark (%d @ %s)" % (MEASUREMENT_INTERVAL, current_minute, str(now)))
                    # ========================================================
                    # Download the weather data from Weather Underground
                    # ========================================================
                    # is weather download enabled (True)?
                    if WEATHER_DOWNLOAD:
                        # From http://wiki.wunderground.com/index.php/PWS_-_Upload_Protocol
                        print("Downloading data from Weather Underground")
                        url = requests.get('https://api.weather.com/v2/pws/observations/current?stationId=IBENAV1&format=json&units=m&apiKey=898d00e499d042e28d00e499d0d2e25b&numericPrecision=decimal')
                        print("Inserting data to mysql database")                        
                        #try:
                        json_data = json.loads(url.text)
                        observe = format(json.dumps(json_data))
                        insert_weather_data = """INSERT INTO weather_data(stationID,obsTimeLocal,neighborhood,softwareType,country,solarRadiation,lon,realtimeFrequency,epoch,lat,uv,winddir,humidity,qcStatus,temp,heatIndex,dewpt,windChill,windSpeed,windGust,pressure,precipRate,precipTotal,elev)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                        insert_Consulta = """INSERT INTO Consulta(obsTimeLocal,temp_dewpt,humidity,precipRate) VALUES (%s, %s, %s, %s)"""
                        y = json.loads(observe)
                        j = y['observations']
                        weather = format(json.dumps(j))
                        k = json_loads_byteified(weather)
                        l = k[0]
                        t = l['metric']
                        weather2 = format(json.dumps(t))
                        u = json_loads_byteified(weather2)
                        v = u
                        valores = (l['stationID'], l["obsTimeLocal"], l["neighborhood"], l["softwareType"], l["country"], l["solarRadiation"], l["lon"], l["realtimeFrequency"], l["epoch"], l["lat"], l["uv"], l["winddir"], l["humidity"], l["qcStatus"], v["temp"], v["heatIndex"], v["dewpt"], v["windChill"], v["windSpeed"], v["windGust"], v["pressure"], v["precipRate"], v["precipTotal"], v["elev"])
                        val2 = (l["obsTimeLocal"], v["temp"] - v["dewpt"], l["humidity"],v["precipRate"])
                        cursor.execute(insert_weather_data, valores)
                        cursor.execute(insert_Consulta, val2)                        
                        cnx.commit()
                        
                        atemp_dewpt = v["temp"] - v["dewpt"]
                        ahumedad = l["humidity"]
                        if l["humidity"] > 93:
                            NIVELnuevo = 'ROJA'
                            print('Alerta', NIVELnuevo)
                            atemp = v["temp"]
                            ahumedad = l["humidity"]
                            apresion = v["pressure"]
                            Delta_humedad = l["humidity"] - HUMEDADant
                            if NIVELnuevo != aNivel and NIVELnuevo != "VERDE":
                                for name, email in zip(names, emails):
                                    message = message_template.substitute(PERSON_NAME=name.title(), NIVEL=NIVELnuevo, temp=atemp, humedad=ahumedad, presion=apresion, Dhumedad=Delta_humedad)
                                    #print(message)
                                    #The mail addresses and password
                                    sender_address = 'pableras84@hotmail.com'
                                    sender_pass = 'Ra2013bL'
                                    receiver_address = email
                                    #Setup the MIME
                                    msg = MIMEMultipart()
                                    msg['From'] = sender_address
                                    msg['To'] = receiver_address
                                    msg['Subject'] = 'Alerta ROJA de precipitación'   #The subject line
                                    #The body and the attachments for the mail
                                    msg.attach(MIMEText(message, 'plain'))
                                    #Create SMTP session for sending the mail
                                    session = smtplib.SMTP('smtp.live.com', 587) #use gmail with port
                                    session.starttls() #enable security
                                    session.login(sender_address, sender_pass) #login with mail_id and password
                                    text = msg.as_string()
                                    session.sendmail(sender_address, receiver_address, text)
                                    session.quit()
                                    print('Mail Sent')
                        elif l["humidity"] > 87:
                            NIVELnuevo = 'NARANJA'
                            print('Alerta', NIVELnuevo)
                            atemp = v["temp"]
                            ahumedad = l["humidity"]
                            apresion = v["pressure"]
                            Delta_humedad = l["humidity"] - HUMEDADant
                            if NIVELnuevo != aNivel and NIVELnuevo != "VERDE":
                                for name, email in zip(names, emails):
                                    message = message_template.substitute(PERSON_NAME=name.title(), NIVEL=NIVELnuevo, temp=atemp, humedad=ahumedad, presion=apresion, Dhumedad=Delta_humedad)
                                    #print(message)
                                    #The mail addresses and password
                                    sender_address = 'pableras84@hotmail.com'
                                    sender_pass = 'Ra2013bL'
                                    receiver_address = email
                                    #Setup the MIME
                                    msg = MIMEMultipart()
                                    msg['From'] = sender_address
                                    msg['To'] = receiver_address
                                    msg['Subject'] = 'Alerta NARANJA de precipitación'   #The subject line
                                    #The body and the attachments for the mail
                                    msg.attach(MIMEText(message, 'plain'))
                                    #Create SMTP session for sending the mail
                                    session = smtplib.SMTP('smtp.live.com', 587) #use gmail with port
                                    session.starttls() #enable security
                                    session.login(sender_address, sender_pass) #login with mail_id and password
                                    text = msg.as_string()
                                    session.sendmail(sender_address, receiver_address, text)
                                    session.quit()
                                    print('Mail Sent') 
                        elif l["humidity"] > 80:
                            NIVELnuevo = 'AMARILLA'
                            print('Alerta', NIVELnuevo)
                            atemp = v["temp"]
                            ahumedad = l["humidity"]
                            apresion = v["pressure"]
                            Delta_humedad = l["humidity"] - HUMEDADant
                            if NIVELnuevo != aNivel and NIVELnuevo != "VERDE":
                                for name, email in zip(names, emails):
                                    message = message_template.substitute(PERSON_NAME=name.title(), NIVEL=NIVELnuevo, temp=atemp, humedad=ahumedad, presion=apresion, Dhumedad=Delta_humedad)
                                    #print(message)
                                    #The mail addresses and password
                                    sender_address = 'pableras84@hotmail.com'
                                    sender_pass = 'Ra2013bL'
                                    receiver_address = email
                                    #Setup the MIME
                                    msg = MIMEMultipart()
                                    msg['From'] = sender_address
                                    msg['To'] = receiver_address
                                    msg['Subject'] = 'Alerta AMARILLA de precipitación'   #The subject line
                                    #The body and the attachments for the mail
                                    msg.attach(MIMEText(message, 'plain'))
                                    #Create SMTP session for sending the mail
                                    session = smtplib.SMTP('smtp.live.com', 587) #use gmail with port
                                    session.starttls() #enable security
                                    session.login(sender_address, sender_pass) #login with mail_id and password
                                    text = msg.as_string()
                                    session.sendmail(sender_address, receiver_address, text)
                                    session.quit()
                                    print('Mail Sent') 
                        elif l["humidity"] - HUMEDADant > 3 and l["humidity"] > 65 and v["pressure"] < 1008:
                            NIVELnuevo = 'ROJA'
                            print('Alerta', NIVELnuevo)
                            atemp = v["temp"]
                            ahumedad = l["humidity"]
                            apresion = v["pressure"]
                            Delta_humedad = l["humidity"] - HUMEDADant
                            if NIVELnuevo != aNivel and NIVELnuevo != "VERDE":
                                for name, email in zip(names, emails):
                                    message = message_template.substitute(PERSON_NAME=name.title(), NIVEL=NIVELnuevo, temp=atemp, humedad=ahumedad, presion=apresion, Dhumedad=Delta_humedad)
                                    #print(message)
                                    #The mail addresses and password
                                    sender_address = 'pableras84@hotmail.com'
                                    sender_pass = 'Ra2013bL'
                                    receiver_address = email
                                    #Setup the MIME
                                    msg = MIMEMultipart()
                                    msg['From'] = sender_address
                                    msg['To'] = receiver_address
                                    msg['Subject'] = 'Alerta ROJA de precipitación'   #The subject line
                                    #The body and the attachments for the mail
                                    msg.attach(MIMEText(message, 'plain'))
                                    #Create SMTP session for sending the mail
                                    session = smtplib.SMTP('smtp.live.com', 587) #use gmail with port
                                    session.starttls() #enable security
                                    session.login(sender_address, sender_pass) #login with mail_id and password
                                    text = msg.as_string()
                                    session.sendmail(sender_address, receiver_address, text)
                                    session.quit()
                                    print('Mail Sent')
                        elif l["humidity"] - HUMEDADant > 3 and l["humidity"] > 55 and v["pressure"] < 1015:
                            NIVELnuevo = 'NARANJA'
                            print('Alerta', NIVELnuevo)
                            atemp = v["temp"]
                            ahumedad = l["humidity"]
                            apresion = v["pressure"]
                            Delta_humedad = l["humidity"] - HUMEDADant
                            if NIVELnuevo != aNivel and NIVELnuevo != "VERDE":
                                for name, email in zip(names, emails):
                                    message = message_template.substitute(PERSON_NAME=name.title(), NIVEL=NIVELnuevo, temp=atemp, humedad=ahumedad, presion=apresion, Dhumedad=Delta_humedad)
                                    #print(message)
                                    #The mail addresses and password
                                    sender_address = 'pableras84@hotmail.com'
                                    sender_pass = 'Ra2013bL'
                                    receiver_address = email
                                    #Setup the MIME
                                    msg = MIMEMultipart()
                                    msg['From'] = sender_address
                                    msg['To'] = receiver_address
                                    msg['Subject'] = 'Alerta NARANJA de precipitación'   #The subject line
                                    #The body and the attachments for the mail
                                    msg.attach(MIMEText(message, 'plain'))
                                    #Create SMTP session for sending the mail
                                    session = smtplib.SMTP('smtp.live.com', 587) #use gmail with port
                                    session.starttls() #enable security
                                    session.login(sender_address, sender_pass) #login with mail_id and password
                                    text = msg.as_string()
                                    session.sendmail(sender_address, receiver_address, text)
                                    session.quit()
                                    print('Mail Sent')
                        elif l["humidity"] <= 80:
                            NIVELnuevo = 'VERDE'
                            print('Sin Alerta')   
                        print(valores, "INSERTADOS EN weatherdb.")
                        time.sleep(290)
                        aNivel = NIVELnuevo
                        HUMEDADant = ahumedad
                        # do something
                        # response.close()  # best practice to close the file
                        #except:
                        #   print("Exception:", sys.exc_info()[0], SLASH_N)
                    else:
                        print("Skipping Weather Underground download")

         # wait a second then check again
        # You can always increase the sleep value below to check less often
        time.sleep(1)  # this should never happen since the above is an infinite loop
    
    print("Leaving main()")


# ============================================================================
# here's where we start doing stuff
# ============================================================================
print(SLASH_N + HASHES)
print(SINGLE_HASH, "Get My PWS Data          ", SINGLE_HASH)
print(SINGLE_HASH, "By Pablo Blanco-Gomez    ", SINGLE_HASH)
print(HASHES)

# make sure we don't have a MEASUREMENT_INTERVAL > 60
if (MEASUREMENT_INTERVAL is None) or (MEASUREMENT_INTERVAL > 60):
    print("The application's 'MEASUREMENT_INTERVAL' cannot be empty or greater than 60")
    sys.exit(1)

# Now see what we're supposed to do next
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
       print("\nExiting application\n")
       sys.exit(0)



