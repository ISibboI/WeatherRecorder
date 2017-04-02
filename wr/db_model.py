import peewee as pw

db = pw.SqliteDatabase('weather.sqlite')


class WeatherData(pw.Model):
    timestamp = pw.IntegerField(primary_key=True)
    temperature = pw.FloatField(null=True)
    humidity = pw.FloatField(null=True)
    pressure = pw.FloatField(null=True)

    class Meta:
        database = db


class DWDWeatherData(WeatherData):
    source = pw.FixedCharField(max_length=4, default='DWD')


class RDMWeatherData(WeatherData):
    source = pw.FixedCharField(max_length=4, default='RDM')


class FMIWeatherData(WeatherData):
    source = pw.FixedCharField(max_length=4, default='FMI')


class EgainWeatherData(WeatherData):
    source = pw.FixedCharField(max_length=4, default='EGSE')


db.connect()
db.create_tables([DWDWeatherData, RDMWeatherData, FMIWeatherData, EgainWeatherData], safe=True)
