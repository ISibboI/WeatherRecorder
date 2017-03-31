from wr.adapters.Adapter import Adapter
from wr.db_model import WeatherData, FMIWeatherData, db
from wr.text_processing import *
import urllib.request
from datetime import datetime
import pytz
import json


class FMIAdapter(Adapter):
    """
    Adapter that reads weather data from the Finnish Meteorological Institute
    """

    # Station 874863 is Espoo Tapiola.
    url = 'http://en.ilmatieteenlaitos.fi/observation-data?station=874863'

    def __init__(self, name):
        super().__init__(name)

    def _receive_data_(self):
        rawjson = str(urllib.request.urlopen(self.url).read()).strip()[2:-5]
        jdata = json.loads(rawjson)
        data_points = []
        timezone = pytz.timezone(jdata['timeZoneId'])

        for temperature, humidity, pressure in zip(jdata['t2m'], jdata['Humidity'], jdata['Pressure']):
            point = WeatherData()

            if temperature[0] != humidity[0] or humidity[0] != pressure[0]:
                raise RuntimeError('Timestamp got messed up!')

            dt = datetime.fromtimestamp(int(temperature[0]) // 1000, timezone)
            point.timestamp = dt.timestamp()
            point.temperature = temperature[1]
            point.humidity = humidity[1]
            point.pressure = pressure[1]

            data_points.append(point)

        return data_points

    def _save_data_(self, data):
        try:
            newest_data = FMIWeatherData.select().order_by(FMIWeatherData.timestamp.desc()).limit(1).get()
        except FMIWeatherData.DoesNotExist:
            newest_data = None

        with db.atomic():
            for point in data:
                if newest_data is not None:
                    if point.timestamp <= newest_data.timestamp:
                        continue

                query = FMIWeatherData.insert(timestamp=point.timestamp,
                                              temperature=point.temperature,
                                              humidity=point.humidity,
                                              pressure=point.pressure,
                                              source=self.name)
                query.execute()
