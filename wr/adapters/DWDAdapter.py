from wr.adapters.Adapter import Adapter
from wr.db_model import WeatherData, DWDWeatherData, db
from wr.text_processing import *
import urllib.request
from datetime import datetime
import pytz


class DWDAdapter(Adapter):
    """
    Adapter that reads weather data from the DWD
    """

    url = "http://www.dwd.de/DE/leistungen/beobachtung/beobachtung.html"

    def __init__(self, name):
        super().__init__(name)

    def _receive_data_(self):
        rawhtml = str(urllib.request.urlopen(self.url).read())

        rawhtml = retain_after(rawhtml, 'Wetterbeobachtungen von ')
        time = retain_before(rawhtml, '</h4>')
        time = retain_after(time, ' ')
        time = retain_before(time, ' Uhr ')

        point = WeatherData()
        timezone = pytz.timezone('Europe/Berlin')
        dt = datetime.strptime(time, '%d.%m.%Y, %H:%M')
        dt = timezone.localize(dt)
        point.timestamp = int(dt.timestamp())

        rawhtml = retain_after(rawhtml, 'Karlsruhe-Rheinst.')
        data = retain_before(rawhtml, '</tr><tr>')
        columns = data.split('</td>\\r\\n  <td>')

        point.temperature = float(columns[3].strip())
        point.humidity = float(columns[4].strip())
        point.pressure = float(columns[2].strip())

        return [point]

    def _save_data_(self, data):
        try:
            newest_data = DWDWeatherData.select().order_by(DWDWeatherData.timestamp.desc()).limit(1).get()
        except DWDWeatherData.DoesNotExist:
            newest_data = None

        with db.atomic():
            for point in data:
                if newest_data is not None:
                    if point.timestamp <= newest_data.timestamp:
                        continue

                query = DWDWeatherData.insert(timestamp=point.timestamp,
                                              temperature=point.temperature,
                                              humidity=point.humidity,
                                              pressure=point.pressure,
                                              source=self.name)
                query.execute()