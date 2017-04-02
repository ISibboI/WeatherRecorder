from wr.adapters.Adapter import Adapter
from wr.db_model import WeatherData, EgainWeatherData, db
from wr.text_processing import *
import urllib.request, urllib.parse
from datetime import datetime
import pytz
import private
import json


class EgainAdapter(Adapter):
    """
    Adapter that reads weather data from the egain.se webservice
    """

    url = "http://install.egain.se/Home/CheckInstalled"

    def __init__(self, name):
        super().__init__(name)

    def _receive_data_(self):
        if type(private.egain_guid) is not str or len(private.egain_guid) == 0:
            raise RuntimeError('GUID for egain.se was not set!')

        post_data = {'guid': private.egain_guid}
        post_data = urllib.parse.urlencode(post_data).encode('ascii')

        rawjson = str(urllib.request.urlopen(self.url, post_data).read().decode('utf-8')).strip()
        jdata = json.loads(rawjson)
        timezone = pytz.timezone('Europe/Stockholm')

        point = WeatherData()
        sensor_info = jdata['SensorInfo']

        dt = datetime.strptime(sensor_info['Date'], '%Y-%m-%d %H:%M')
        dt = timezone.localize(dt)
        point.timestamp = int(dt.timestamp())
        point.temperature = float(sensor_info['Temp'])
        point.humidity = float(sensor_info['Humidity'])

        return [point]

    def _save_data_(self, data):
        try:
            newest_data = EgainWeatherData.select().order_by(EgainWeatherData.timestamp.desc()).limit(1).get()
        except EgainWeatherData.DoesNotExist:
            newest_data = None

        with db.atomic():
            for point in data:
                if newest_data is not None:
                    if point.timestamp <= newest_data.timestamp:
                        continue

                query = EgainWeatherData.insert(timestamp=point.timestamp,
                                              temperature=point.temperature,
                                              humidity=point.humidity,
                                              pressure=point.pressure,
                                              source=self.name)
                query.execute()