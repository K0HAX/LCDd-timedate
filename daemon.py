#!/usr/bin/env python3
import time
import datetime
import json
import asyncio
from noaa_sdk import NOAA

from lcdproc.server import Server, Screen

async def get_observation(stationID):
    n = NOAA()
    startTime = (datetime.datetime.now() - datetime.timedelta(hours = 24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    endTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    retval = n.stations_observations(station_id=stationID, start=startTime, end=endTime)
    #Fahrenheit=(Celsius∗1.8)+32
    #"unitCode": "wmoUnit:degC"
    valTry = 0
    valWorked = False
    thisTemp = None
    while valWorked == False:
        tempDict = retval[valTry].get('properties').get('temperature')
        #print(json.dumps(retval[valTry], indent=2))
        if tempDict == None:
            return None
        if tempDict.get('unitCode') == None:
            return None
        unit = tempDict.get('unitCode')

        thisTemp = tempDict.get('value')
        if thisTemp == None:
            valTry += 1
            continue
        if thisTemp != None:
            valWorked = True
        if unit == "wmoUnit:degC":
            thisTemp = ((tempDict.get('value')*1.8)+32)

    return round(thisTemp, 1)

async def get_time():
    curTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    return curTime

async def run_obs_timer(widget, stationID):
    while True:
        thisObservation = await get_observation(stationID)
        widget.set_text(f"{thisObservation} degrees")
        print(f"{thisObservation} degrees")
        await asyncio.sleep(3600)

async def run_time_timer(widget):
    while True:
        thisTime = await get_time()
        widget.set_text(f"{thisTime}")
        await asyncio.sleep(0.1)

def main():
    lcd = Server("127.0.0.1", debug=False)
    lcd.start_session()

    screen1 = lcd.add_screen("Screen1")
    screen1.set_heartbeat("off")
    screen1.set_duration(10)
    screen1.set_height(2)
    screen1.set_width(20)

    #num1_widget = screen1.add_number_widget("MyNumber1Widget", x=1, value=0)
    #num2_widget = screen1.add_number_widget("MyNumber2Widget", x=5, value=0)

    #string_widget = screen1.add_string_widget("MyStringWidget", text=f"{get_observation('KANE')}", x=1, y=1)
    time_widget = screen1.add_string_widget("MyStringWidget", text=f"TIME", x=1, y=1)
    temperature_widget = screen1.add_string_widget("MyStringWidget2", text=f"TEMPERATURE", x=1, y=2)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(run_time_timer(time_widget))
    loop.create_task(run_obs_timer(temperature_widget, "KANE"))
    loop.run_forever()

if __name__ == "__main__":
    main()

