#!/usr/bin/env python3
import time
import datetime
import json
import asyncio
from meNOAA import NOAA

from lcdproc.server import Server, Screen

async def get_observation(stationID, roundPlaces = 0):
    n = NOAA(station_id=stationID)
    startTime = (datetime.datetime.now() - datetime.timedelta(hours = 24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    endTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    retval = n.latest_observation()
    #Fahrenheit=(Celsius∗1.8)+32
    #"unitCode": "wmoUnit:degC"
    thisTemp = None
    tempDict = retval.get('properties').get('temperature')
    if tempDict == None:
        return None
    if tempDict.get('unitCode') == None:
        return None
    unit = tempDict.get('unitCode')

    thisTemp = tempDict.get('value')
    if unit == "wmoUnit:degC":
        thisTemp = ((tempDict.get('value')*1.8)+32)

    if roundPlaces == 0:
        return int(round(thisTemp, roundPlaces))
    else:
        return round(thisTemp, roundPlaces)

async def get_time():
    curTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return curTime

async def run_obs_timer(widget, stationID, roundPlaces = 0):
    while True:
        thisObservation = await get_observation(stationID, roundPlaces)
        widget.set_text(f"Temperature: {thisObservation} F")
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

