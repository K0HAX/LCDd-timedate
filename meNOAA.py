#!/usr/bin/env python3
import urllib.request
import json

class NOAA:
    def latest_observation(self):
        url = f"{self._url_base}/stations/{self.station_id}/observations/latest"
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read())

    def __init__(self, station_id):
        #self.url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
        self._url_base = "https://api.weather.gov/"
        self.station_id = station_id
