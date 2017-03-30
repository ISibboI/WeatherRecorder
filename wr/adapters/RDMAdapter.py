from wr.adapters.Adapter import Adapter
from wr.db_model import WeatherData, RDMWeatherData, db
from wr.text_processing import *
import urllib.request
from datetime import datetime
import pytz


class RDMAdapter(Adapter):
    """
    Adapter that reads weather data from http://www.rodima.de/rdmwetter/
    """

    url = 'http://www.rodima.de/rdmwetter/aktuell.htm'

    def __init__(self, name):
        super().__init__(name)

    def _receive_data_(self):
        rawhtml = str(urllib.request.urlopen(self.url).read())
        rawhtml = retain_after(rawhtml, '<table border="1" cellspacing="0" cellpadding="4">\\r\\n')
        rawhtml = retain_before(rawhtml, '</table>\\r\\n</body>\\r\\n</html>\\r\\n')
        rawtable = rawhtml.replace('\\r\\n', '')
        rawtable = rawtable.replace('<nobr>', '')
        rawtable = rawtable.replace('</nobr>', '')
        rows = rawtable.split('</tr><tr>')

        data_points = []

        for row in rows:
            if row.startswith('<th>') or row.startswith('<tr><th>'):
                continue

            columns = row.split('</td><td>')

            date = columns[0][4:]
            time = columns[1]
            temperature = columns[3]
            humidity = columns[7]
            pressure = columns[8]

            point = WeatherData()
            timezone = pytz.timezone('Europe/Berlin')
            dt = datetime.strptime(date + ' ' + time, '%d.%m.%Y %H:%M')
            dt = timezone.localize(dt)
            point.timestamp = int(dt.timestamp())

            point.temperature = float(retain_before(temperature, ' ').replace(',', '.'))
            point.humidity = float(retain_before(humidity, ' ').replace(',', '.'))
            point.pressure = float(retain_before(pressure, ' ').replace(',', '.'))
            point.source = self.name

            data_points.append(point)

        return data_points

    def _save_data_(self, data):
        try:
            newest_data = RDMWeatherData.select().order_by(RDMWeatherData.timestamp.desc()).limit(1).get()
        except RDMWeatherData.DoesNotExist:
            newest_data = None

        with db.atomic():
            for point in data:
                if newest_data is not None:
                    if point.timestamp <= newest_data.timestamp:
                        continue

                query = RDMWeatherData.insert(timestamp=point.timestamp,
                                              temperature=point.temperature,
                                              humidity=point.humidity,
                                              pressure=point.pressure,
                                              source=self.name)
                query.execute()
