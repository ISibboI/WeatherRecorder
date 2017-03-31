import peewee as pw

db = pw.SqliteDatabase('weather.sqlite')


class WeatherData(pw.Model):
    timestamp = pw.IntegerField(primary_key=True)
    temperature = pw.FloatField()
    humidity = pw.FloatField()
    pressure = pw.FloatField()

    class Meta:
        database = db


class DWDWeatherData(WeatherData):
    source = pw.FixedCharField(max_length=4, default='DWD')


class RDMWeatherData(WeatherData):
    source = pw.FixedCharField(max_length=4, default='RDM')


class FMIWeatherData(WeatherData):
    source = pw.FixedCharField(max_length=4, default='FMI')


db.connect()
db.create_tables([DWDWeatherData, RDMWeatherData, FMIWeatherData], safe=True)
