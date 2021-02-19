
#!/usr/bin/env python
import requests
import MySQLdb
import json
import mysql.connector

print( "Connecting to mysql database")

#connect to the database. Enter your host, username and password
cnx = mysql.connector.connect(user='root',password='papelote', database='weatherdb')

cursor = cnx.cursor()
insert_weather_data = ("INSERT INTO `weatherdb`.`weather_data`"
                            "(`stationID`,`obsTimeUtc`,`obsTimeLocal`,`neighborhood`,`softwareType`,`country`,`solarRadiation`,`lon`,`realtimeFrequency`,`epoch`,`lat`,`uv`,`winddir`,`humidity`,`qcStatus`,`metric`,`temp`,`heatIndex`,`dewpt`,`windChill`,`windSpeed`,`windGust`,`pressure`,`precipRate`,`precipTotal`,`elev`)"
                            "VALUES (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)")







print( "Getting My PWS weather information")
#url=requests.get('https://api.weather.com/v2/pws/observations/current?stationId=IBENAV1&format=json&units=m&apiKey=898d00e499d042e28d00e499d0d2e25b&numericPrecision=decimal')

print( "Inserting data to mysql database")
weather=json.loads(url.text)
print(weather)

#insert_weather_data = ("INSERT INTO `weatherdb`.`weather_data`"
                "(`stationID`,`obsTimeUtc`,`obsTimeLocal`,`neighborhood`,`softwareType`,`country`,`solarRadiation`,`lon`,`realtimeFrequency`,`epoch`,`lat`,`uv`,`winddir`,`humidity`,`qcStatus`,`metric`,`temp`,`heatIndex`,`dewpt`,`windChill`,`windSpeed`,`windGust`,`pressure`,`precipRate`,`precipTotal`,`elev`)"
                "VALUES (%(stationID)s, %(obsTimeUtc)s, %(obsTimeLocal)s, %(neighborhood)s, %(softwareType)s,%(country)s, %(solarRadiation)s, %(lon)s, %(realtimeFrequency)s, %(epoch)s, %(lat)s, %(uv)s, %(winddir)s, %(humidity)s, %(qcStatus)s, %(metric)s, %(temp)s, %(heatIndex)s, %(dewpt)s, %(windChill)s, %(windSpeed)s, %(windGust)s, %(pressure)s, %(precipRate)s, %(precipTotal)s, %(elev)s)")

from mysql.connector import Error

try:
    sql_select_Query = "select * from weatherdb"
    cursor = cnx.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    print("Total number of rows in weatherdb is: ", cursor.rowcount)

    print("\nPrinting each weatherdb record")
    for row in records:
        print("humidity = ", row[14], )
        print("temp = ", row[17])
        print("dewpt  = ", row[19])
        print("WindChill  = ", row[20])

except Error as e:
    print("Error reading data from MySQL table", e)
finally:
    if (cnx.is_connected()):
        cnx.close()
        cursor.close()
        print("MySQL connection is closed")






# Iterate through the locations
#locations=weather["locations"]
#for locationid in locations:  
#    location=locations[locationid]
    # Iterate through the values (values are the time periods in the weather data)
#    for value in location["values"]:
#        data_wx = {
#        'stationID': location["stationID"],
#        'obsTimeUtc': datetime.utcfromtimestamp(value["latitude"]/1000.),
#        'obsTimeLocal': value["obsTimeLocal"],
#        'neighborhood':  location["neighborhood"],
#        'softwareType': location["softwareType"],
#        'country': location["country"],
#        'solarRadiation': value["solarRadiation"],
#        'lon': value["lon"],
#        'realtimeFrequency': value["realtimeFrequency"],
#        'epoch': value["epoch"],
#        'lat': value["lat"],
#        'uv': value["uv"],
#        'winddir': value["winddir"],
#        'humidity': value["humidity"],
#        'qcStatus': value["qcStatus"],
#        'metric': value["metric"],
#        'temp': value["temp"],
#        'heatIndex': value["heatIndex"],
#        'dewpt': value["dewpt"],
#        'windChill': value["windChill"],
#        'windSpeed': value["windSpeed"],
#        'windGust': value["windGust"],
#        'pressure': value["pressure"],
#        'precipRate': value["precipRate"],
#        'precipTotal': value["precipTotal"],
#        'elev': value["elev"]
#        }
#        cursor.execute(insert_weather_data, data_wx)
#        cnx.commit()
               
cursor.close() 
cnx.close()
print( "Database connection closed")

print( "Done")


# try:
#    curs.execute (""INSERT INTO weather_data values (weather)"")
# db.commit()
#    print "Data committed"

# except:
#    print "Error: the database is being rolled back"
#    db.rollback()

# url = 'https://api.weather.com/v2/pws/observations/current?stationId=IBENAV1&format=json&units=m&apiKey=898d00e499d042e28d00e499d0d2e25b'
# resp = requests.get(url=url)
# data = resp.json()
# print (data)
